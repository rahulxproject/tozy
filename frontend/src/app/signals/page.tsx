'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { signalsAPI } from '@/lib/api'

export default function SignalsPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuth()
  const [signals, setSignals] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('active')

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    loadSignals()
  }, [isAuthenticated, router, filter])

  const loadSignals = async () => {
    try {
      const response = await signalsAPI.getSignals({ status: filter, limit: 50 })
      setSignals(response.data.signals || [])
    } catch (error) {
      console.error('Error loading signals:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Trading Signals</h1>
          <button 
            onClick={() => router.push('/dashboard')}
            className="text-gray-600 hover:text-gray-900"
          >
            Back to Dashboard
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-6 flex gap-2">
          <button
            onClick={() => setFilter('active')}
            className={`px-4 py-2 rounded-lg transition ${
              filter === 'active' 
                ? 'bg-blue-600 text-white' 
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            Active
          </button>
          <button
            onClick={() => setFilter('expired')}
            className={`px-4 py-2 rounded-lg transition ${
              filter === 'expired' 
                ? 'bg-blue-600 text-white' 
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            Expired
          </button>
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg transition ${
              filter === 'all' 
                ? 'bg-blue-600 text-white' 
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            All
          </button>
        </div>

        {signals.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-6 text-center text-gray-500">
            No signals found
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {signals.map((signal: any) => (
              <div key={signal.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold">{signal.instrument_symbol}</h3>
                    <p className="text-sm text-gray-600">{signal.strategy_name}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    signal.signal_type === 'BUY' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {signal.signal_type}
                  </span>
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Entry:</span>
                    <span className="font-medium">₹{signal.entry_price}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Stop Loss:</span>
                    <span className="font-medium text-red-600">₹{signal.stop_loss}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Take Profit:</span>
                    <span className="font-medium text-green-600">₹{signal.take_profit}</span>
                  </div>
                </div>

                <div className="mb-4">
                  <div className="text-sm text-gray-600 mb-1">Confidence</div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full" 
                      style={{ width: `${signal.confidence_score * 100}%` }}
                    ></div>
                  </div>
                  <div className="text-right text-sm text-gray-600 mt-1">
                    {(signal.confidence_score * 100).toFixed(0)}%
                  </div>
                </div>

                <div className="text-sm text-gray-500 mb-4">
                  {signal.reasoning}
                </div>

                <div className="text-xs text-gray-400">
                  Expires: {new Date(signal.expires_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
