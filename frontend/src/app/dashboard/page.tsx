'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { signalsAPI, tradesAPI, strategiesAPI } from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'

export default function Dashboard() {
  const router = useRouter()
  const { logout, isAuthenticated } = useAuth()
  const [signals, setSignals] = useState([])
  const [trades, setTrades] = useState([])
  const [performance, setPerformance] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    loadDashboardData()
  }, [isAuthenticated, router])

  const loadDashboardData = async () => {
    try {
      const [signalsRes, tradesRes, performanceRes] = await Promise.all([
        signalsAPI.getSignals({ limit: 5 }),
        tradesAPI.getTrades({ limit: 5 }),
        tradesAPI.getPerformance()
      ])
      
      setSignals(signalsRes.data.signals || [])
      setTrades(tradesRes.data.trades || [])
      setPerformance(performanceRes.data.performance || {})
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    router.push('/login')
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
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <button 
            onClick={handleLogout}
            className="text-gray-600 hover:text-gray-900"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Performance Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Total P/L</div>
            <div className="text-2xl font-bold">
              ₹{performance?.total_pnl?.toFixed(2) || '0.00'}
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Win Rate</div>
            <div className="text-2xl font-bold">
              {performance?.total_trades > 0 
                ? ((performance?.winning_trades / performance?.total_trades) * 100).toFixed(1) + '%'
                : 'N/A'}
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Total Trades</div>
            <div className="text-2xl font-bold">{performance?.total_trades || 0}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Active Signals</div>
            <div className="text-2xl font-bold">{signals.length}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Signals */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b">
              <h2 className="text-lg font-semibold">Recent Signals</h2>
            </div>
            <div className="p-6">
              {signals.length === 0 ? (
                <div className="text-gray-500 text-center py-8">No signals available</div>
              ) : (
                <div className="space-y-4">
                  {signals.map((signal: any) => (
                    <div key={signal.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <div className="font-semibold">{signal.instrument_symbol}</div>
                          <div className="text-sm text-gray-600">{signal.strategy_name}</div>
                        </div>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          signal.signal_type === 'BUY' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {signal.signal_type}
                        </span>
                      </div>
                      <div className="text-sm text-gray-600">
                        Entry: ₹{signal.entry_price} | SL: ₹{signal.stop_loss} | TP: ₹{signal.take_profit}
                      </div>
                      <div className="text-sm text-gray-500 mt-1">
                        Confidence: {(signal.confidence_score * 100).toFixed(0)}%
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Recent Trades */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b">
              <h2 className="text-lg font-semibold">Recent Trades</h2>
            </div>
            <div className="p-6">
              {trades.length === 0 ? (
                <div className="text-gray-500 text-center py-8">No trades yet</div>
              ) : (
                <div className="space-y-4">
                  {trades.map((trade: any) => (
                    <div key={trade.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <div className="font-semibold">{trade.instrument_symbol}</div>
                          <div className="text-sm text-gray-600">{trade.entry_date}</div>
                        </div>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          trade.status === 'closed' 
                            ? (trade.pnl >= 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800')
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {trade.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="text-sm text-gray-600">
                        Entry: ₹{trade.entry_price} | Qty: {trade.quantity}
                      </div>
                      {trade.status === 'closed' && (
                        <div className={`text-sm font-medium mt-1 ${
                          trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          P/L: ₹{trade.pnl?.toFixed(2)} ({trade.pnl_percentage?.toFixed(2)}%)
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button 
              onClick={() => router.push('/trades/new')}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Log Trade
            </button>
            <button 
              onClick={() => router.push('/signals')}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              View Signals
            </button>
            <button 
              onClick={() => router.push('/journal')}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              View Journal
            </button>
            <button 
              onClick={() => router.push('/analytics')}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Analytics
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}
