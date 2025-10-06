export async function apiFetch(input: RequestInfo | URL, init: RequestInit = {}) {
	const traceparent = (window as any).__traceparent as string | undefined
	const headers = new Headers(init.headers as HeadersInit)
	if (traceparent) headers.set('traceparent', traceparent)
	return fetch(input, { ...init, headers })
}

export async function uploadDetect(image: File) {
	const form = new FormData()
	form.append('file', image)
	const res = await apiFetch(process.env.NEXT_PUBLIC_BACKEND_URL + '/detect/frame', { method: 'POST', body: form })
	return { json: await res.json(), traceId: res.headers.get('x-trace-id') }
}

export async function getSignals() {
	const res = await apiFetch(process.env.NEXT_PUBLIC_BACKEND_URL + '/signal/all')
	return res.json()
}

export async function updateSignal(id: string, status: 'red'|'yellow'|'green') {
	const url = new URL(process.env.NEXT_PUBLIC_BACKEND_URL + '/signal/update')
	url.searchParams.set('signal_id', id)
	url.searchParams.set('status', status)
	const res = await apiFetch(url)
	return res.json()
}

export async function postGPS(point: {lat:number, lon:number, ts:number, route_name?: string}) {
	const res = await apiFetch(process.env.NEXT_PUBLIC_BACKEND_URL + '/simulate/gps_point', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(point)
	})
	return res.json()
}

export async function getStats() {
	const res = await apiFetch(process.env.NEXT_PUBLIC_BACKEND_URL + '/stats/summary')
	return res.json()
}
