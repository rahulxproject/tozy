'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { strategiesAPI } from '@/lib/api'
import Navigation from '@/components/Navigation'

export default function StrategiesPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuth()
  const [strategies, setStrategies] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    entry_conditions: { rules: [], logic: 'AND' },
    exit_conditions: { rules: [], logic: 'AND' },
    risk_parameters: { stop_loss_pct: 2, take_profit_pct: 3 },
    timeframe: '1D'
  })

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    loadStrategies()
  }, [isAuthenticated, router])

  const loadStrategies = async () => {
    try {
      const response = await strategiesAPI.getStrategies()
      setStrategies(response.data.strategies || [])
    } catch (error) {
      console.error('Error loading strategies:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await strategiesAPI.createStrategy(formData)
      setFormData({
        name: '',
        description: '',
        entry_conditions: { rules: [], logic: 'AND' },
        exit_conditions: { rules: [], logic: 'AND' },
        risk_parameters: { stop_loss_pct: 2, take_profit_pct: 3 },
        timeframe: '1D'
      })
      setShowForm(false)
      loadStrategies()
    } catch (error: any) {
      console.error('Error creating strategy:', error)
      alert(error.response?.data?.error || 'Failed to create strategy')
    }
  }

  const handleDelete = async (strategyId: string) => {
    try {
      await strategiesAPI.deleteStrategy(strategyId)
      loadStrategies()
    } catch (error: any) {
      console.error('Error deleting strategy:', error)
      alert(error.response?.data?.error || 'Failed to delete strategy')
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
        <div className="mb-6">
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            {showForm ? 'Cancel' : 'New Strategy'}
          </button>
        </div>

        {showForm && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Strategy Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  placeholder="e.g., RSI Reversal"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  placeholder="Describe your strategy..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Timeframe
                </label>
                <select
                  value={formData.timeframe}
                  onChange={(e) => setFormData({...formData, timeframe: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="1D">Daily</option>
                  <option value="1H">Hourly</option>
                  <option value="15m">15 Minutes</option>
                  <option value="5m">5 Minutes</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Stop Loss %
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.risk_parameters.stop_loss_pct}
                    onChange={(e) => setFormData({
                      ...formData,
                      risk_parameters: {...formData.risk_parameters, stop_loss_pct: parseFloat(e.target.value)}
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Take Profit %
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.risk_parameters.take_profit_pct}
                    onChange={(e) => setFormData({
                      ...formData,
                      risk_parameters: {...formData.risk_parameters, take_profit_pct: parseFloat(e.target.value)}
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
              >
                Save Strategy
              </button>
            </form>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {strategies.map((strategy: any) => (
            <div key={strategy.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold">{strategy.name}</h3>
                {strategy.is_system ? (
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">System</span>
                ) : (
                  <button
                    onClick={() => handleDelete(strategy.id)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Delete
                  </button>
                )}
              </div>
              <p className="text-sm text-gray-600 mb-3">{strategy.description}</p>
              <div className="text-sm text-gray-500">
                <div>Timeframe: {strategy.timeframe}</div>
                <div>SL: {strategy.risk_parameters?.stop_loss_pct}% | TP: {strategy.risk_parameters?.take_profit_pct}%</div>
              </div>
              <div className="mt-3">
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  strategy.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {strategy.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
