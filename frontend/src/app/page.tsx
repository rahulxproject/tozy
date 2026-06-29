'use client'

import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'

export default function Home() {
  const router = useRouter()
  const { isAuthenticated } = useAuth()

  const handleGetStarted = () => {
    if (isAuthenticated) {
      router.push('/dashboard')
    } else {
      router.push('/register')
    }
  }

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
          <button 
            onClick={handleGetStarted}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
          >
            {isAuthenticated ? 'Go to Dashboard' : 'Get Started'}
          </button>
          <button 
            onClick={() => router.push('/login')}
            className="border border-blue-600 text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 transition"
          >
            Sign In
          </button>
        </div>
        <div className="mt-12 text-sm text-gray-500">
          Features: Real-time Signals • Trading Journal • Performance Analytics • AI Coaching
        </div>
      </div>
    </main>
  )
}
