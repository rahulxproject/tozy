export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-50 to-white">
      <div className="text-center p-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Indian AI Trading Platform
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-powered swing trading signals and behavioral coaching for Indian retail traders
        </p>
        <div className="space-x-4">
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
            Get Started
          </button>
          <button className="border border-blue-600 text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 transition">
            Learn More
          </button>
        </div>
        <div className="mt-12 text-sm text-gray-500">
          API Status: <span className="text-green-600">Connected</span>
        </div>
      </div>
    </main>
  )
}
