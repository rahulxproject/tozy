'use client'

import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'

export default function Navigation() {
  const router = useRouter()
  const { isAuthenticated, logout } = useAuth()

  if (!isAuthenticated) {
    return null
  }

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <button
              onClick={() => router.push('/dashboard')}
              className="text-gray-700 hover:text-blue-600 font-medium"
            >
              Dashboard
            </button>
            <button
              onClick={() => router.push('/signals')}
              className="text-gray-700 hover:text-blue-600 font-medium"
            >
              Signals
            </button>
            <button
              onClick={() => router.push('/trades')}
              className="text-gray-700 hover:text-blue-600 font-medium"
            >
              Trades
            </button>
            <button
              onClick={() => router.push('/strategies')}
              className="text-gray-700 hover:text-blue-600 font-medium"
            >
              Strategies
            </button>
            <button
              onClick={() => router.push('/journal')}
              className="text-gray-700 hover:text-blue-600 font-medium"
            >
              Journal
            </button>
            <button
              onClick={() => router.push('/analytics')}
              className="text-gray-700 hover:text-blue-600 font-medium"
            >
              Analytics
            </button>
          </div>
          <button
            onClick={() => {
              logout()
              router.push('/login')
            }}
            className="text-gray-600 hover:text-red-600 font-medium"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}
