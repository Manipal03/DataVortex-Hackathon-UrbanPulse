import Dashboard from '../components/Dashboard'

export default function Home() {
	return (
		<div className="min-h-screen bg-gray-950 text-white">
			<header className="p-6 border-b border-white/10">
				<h1 className="text-2xl font-semibold">UrbanPulse AI</h1>
				<p className="text-sm text-white/70">Empowering cities to clear the path for life-saving vehicles — intelligently and instantly.</p>
			</header>
			<main className="p-6">
				<Dashboard />
			</main>
		</div>
	)
}
