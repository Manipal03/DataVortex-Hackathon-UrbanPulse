import { useEffect, useMemo, useRef, useState } from 'react'
import { uploadDetect, getSignals, postGPS, getStats } from '../lib/api'

export default function Dashboard() {
	const [traceId, setTraceId] = useState<string | null>(null)
	const [signals, setSignals] = useState<Record<string,string>>({})
	const [stats, setStats] = useState<{detections:number, avg_response_time_ms:number, corridor_activations:number}>({detections:0, avg_response_time_ms:0, corridor_activations:0})
	const pollingRef = useRef<any>(null)

	useEffect(() => {
		const poll = async () => {
			try {
				const [s, st] = await Promise.all([
					getSignals(),
					getStats(),
				])
				setSignals(s.signals || {})
				setStats(st)
			} catch {}
		}
		poll()
		pollingRef.current = setInterval(poll, 3000)
		return () => clearInterval(pollingRef.current)
	}, [])

	const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0]
		if (!file) return
		const { json, traceId } = await uploadDetect(file)
		setTraceId(traceId || null)
	}

	const startSim = async () => {
		navigator.geolocation.getCurrentPosition(async (pos) => {
			await postGPS({ lat: pos.coords.latitude, lon: pos.coords.longitude, ts: Date.now()/1000, route_name: 'active' })
		})
	}

	return (
		<div className="grid md:grid-cols-2 gap-6">
			<section className="bg-black/40 rounded-xl p-4 border border-white/10">
				<h2 className="font-medium mb-2">Video</h2>
				<input type="file" accept="image/*" onChange={handleUpload} />
				{traceId && <p className="mt-2 text-xs text-white/60">trace_id: {traceId}</p>}
			</section>
			<section className="bg-black/40 rounded-xl p-4 border border-white/10">
				<h2 className="font-medium mb-2">Map</h2>
				<div className="h-80 bg-black/40 rounded-lg flex items-center justify-center text-white/50">Mapbox placeholder</div>
			</section>
			<section className="md:col-span-2 bg-black/40 rounded-xl p-4 border border-white/10">
				<h2 className="font-medium mb-2">Metrics</h2>
				<div className="grid grid-cols-3 gap-4 text-center">
					<div className="p-3 rounded-lg bg-white/5"><div className="text-2xl font-semibold">{stats.detections}</div><div className="text-xs text-white/60">Detections</div></div>
					<div className="p-3 rounded-lg bg-white/5"><div className="text-2xl font-semibold">{stats.corridor_activations}</div><div className="text-xs text-white/60">Corridor Active</div></div>
					<div className="p-3 rounded-lg bg-white/5"><div className="text-2xl font-semibold">{stats.avg_response_time_ms} ms</div><div className="text-xs text-white/60">Avg Response</div></div>
				</div>
				<h2 className="font-medium mt-4 mb-2">Controls</h2>
				<div className="flex gap-3">
					<label className="px-4 py-2 rounded-lg bg-emerald-600 cursor-pointer">Upload Image<input type="file" className="hidden" accept="image/*" onChange={handleUpload} /></label>
					<button className="px-4 py-2 rounded-lg bg-sky-600" onClick={startSim}>Start Simulation</button>
					<button className="px-4 py-2 rounded-lg bg-amber-600">Manual Override</button>
				</div>
				<div className="mt-4 text-sm">
					<h3 className="font-medium mb-1">Signals</h3>
					<div className="flex gap-3 flex-wrap">
						{Object.entries(signals).map(([id, status]) => (
							<div key={id} className="px-3 py-2 rounded-lg bg-white/5 border border-white/10">
								<span className="font-mono mr-2">{id}</span>
								<span className="uppercase text-xs">{status}</span>
							</div>
						))}
					</div>
				</div>
			</section>
		</div>
	)
}
