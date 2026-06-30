'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { tradesAPI } from '@/lib/api'
import Navigation from '@/components/Navigation'

export default function AnalyticsPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuth()
  const [performance, setPerformance] = useState<any>(null)
  const [trades, setTrades] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    loadAnalyticsData()
  }, [isAuthenticated, router])

  const loadAnalyticsData = async () => {
    try {
      const [performanceRes, tradesRes] = await Promise.all([
        tradesAPI.getPerformance(),
        tradesAPI.getTrades({ limit: 100 })
      ])
      
      setPerformance(performanceRes.data.performance || {})
      setTrades(tradesRes.data.trades || [])
    } catch (error) {
      console.error('Error loading analytics data:', error)
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
      <Navigation />
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Performance Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Total P/L</div>
            <div className={`text-2xl font-bold ${performance?.total_pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
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
            <div className="text-sm text-gray-600 mb-1">Profit Factor</div>
            <div className="text-2xl font-bold">
              {performance?.profit_factor === Infinity ? '∞' : performance?.profit_factor?.toFixed(2) || '0.00'}
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Max Drawdown</div>
            <div className="text-2xl font-bold text-red-600">
              {performance?.max_drawdown?.toFixed(2) || '0.00'}%
            </div>
          </div>
        </div>

        {/* Detailed Metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Trade Statistics</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Trades</span>
                <span className="font-medium">{performance?.total_trades || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Winning Trades</span>
                <span className="font-medium text-green-600">{performance?.winning_trades || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Losing Trades</span>
                <span className="font-medium text-red-600">{performance?.total_trades - performance?.winning_trades || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Average Win</span>
                <span className="font-medium text-green-600">₹{performance?.avg_win?.toFixed(2) || '0.00'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Average Loss</span>
                <span className="font-medium text-red-600">₹{performance?.avg_loss?.toFixed(2) || '0.00'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Sharpe Ratio</span>
                <span className="font-medium">{performance?.sharpe_ratio?.toFixed(2) || '0.00'}</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">P/L Breakdown</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Gross Profit</span>
                <span className="font-medium text-green-600">₹{performance?.gross_profit?.toFixed(2) || '0.00'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Gross Loss</span>
                <span className="font-medium text-red-600">₹{performance?.gross_loss?.toFixed(2) || '0.00'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Net P/L</span>
                <span className={`font-medium ${performance?.total_pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  ₹{performance?.total_pnl?.toFixed(2) || '0.00'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Return %</span>
                <span className={`font-medium ${performance?.total_return_percentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {performance?.total_return_percentage?.toFixed(2) || '0.00'}%
                </span>
              </div>
            </div>
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
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left py-2 px-4">Instrument</th>
                      <th className="text-left py-2 px-4">Type</th>
                      <th className="text-left py-2 px-4">Entry</th>
                      <th className="text-left py-2 px-4">Exit</th>
                      <th className="text-left py-2 px-4">P/L</th>
                      <th className="text-left py-2 px-4">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {trades.map((trade: any) => (
                      <tr key={trade.id} className="border-b">
                        <td className="py-2 px-4">{trade.instrument_symbol}</td>
                        <td className="py-2 px-4">{trade.trade_type}</td>
                        <td className="py-2 px-4">₹{trade.entry_price}</td>
                        <td className="py-2 px-4">{trade.exit_price ? `₹${trade.exit_price}` : '-'}</td>
                        <td className={`py-2 px-4 ${trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {trade.status === 'closed' ? `₹${trade.pnl?.toFixed(2)}` : '-'}
                        </td>
                        <td className="py-2 px-4">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            trade.status === 'closed' 
                              ? (trade.pnl >= 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800')
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {trade.status.toUpperCase()}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
