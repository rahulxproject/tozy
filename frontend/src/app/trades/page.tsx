'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { tradesAPI } from '@/lib/api'
import Navigation from '@/components/Navigation'

export default function TradesPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuth()
  const [trades, setTrades] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    loadTrades()
  }, [isAuthenticated, router])

  const loadTrades = async () => {
    try {
      const response = await tradesAPI.getTrades({ limit: 100 })
      setTrades(response.data.trades || [])
    } catch (error) {
      console.error('Error loading trades:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCloseTrade = async (tradeId: string) => {
    try {
      await tradesAPI.closeTrade(tradeId)
      loadTrades()
    } catch (error: any) {
      console.error('Error closing trade:', error)
      alert(error.response?.data?.error || 'Failed to close trade')
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
      <Navigation />
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        {trades.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-6 text-center text-gray-500">
            No trades yet. Start by logging your first trade!
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow">
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b bg-gray-50">
                    <th className="text-left py-3 px-4 font-semibold">Instrument</th>
                    <th className="text-left py-3 px-4 font-semibold">Type</th>
                    <th className="text-left py-3 px-4 font-semibold">Entry Date</th>
                    <th className="text-left py-3 px-4 font-semibold">Entry Price</th>
                    <th className="text-left py-3 px-4 font-semibold">Quantity</th>
                    <th className="text-left py-3 px-4 font-semibold">Stop Loss</th>
                    <th className="text-left py-3 px-4 font-semibold">Take Profit</th>
                    <th className="text-left py-3 px-4 font-semibold">P/L</th>
                    <th className="text-left py-3 px-4 font-semibold">Status</th>
                    <th className="text-left py-3 px-4 font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {trades.map((trade: any) => (
                    <tr key={trade.id} className="border-b hover:bg-gray-50">
                      <td className="py-3 px-4 font-medium">{trade.instrument_symbol}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          trade.trade_type === 'BUY' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {trade.trade_type}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600">{trade.entry_date}</td>
                      <td className="py-3 px-4">₹{trade.entry_price}</td>
                      <td className="py-3 px-4">{trade.quantity}</td>
                      <td className="py-3 px-4 text-red-600">{trade.stop_loss ? `₹${trade.stop_loss}` : '-'}</td>
                      <td className="py-3 px-4 text-green-600">{trade.take_profit ? `₹${trade.take_profit}` : '-'}</td>
                      <td className={`py-3 px-4 font-medium ${trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {trade.status === 'closed' ? `₹${trade.pnl?.toFixed(2)}` : '-'}
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          trade.status === 'closed' 
                            ? (trade.pnl >= 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800')
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {trade.status.toUpperCase()}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        {trade.status === 'open' && (
                          <button
                            onClick={() => handleCloseTrade(trade.id)}
                            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                          >
                            Close
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
