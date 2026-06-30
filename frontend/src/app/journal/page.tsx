'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { journalAPI } from '@/lib/api'
import Navigation from '@/components/Navigation'

export default function JournalPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuth()
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    notes: '',
    entry_type: 'general',
    mood: '',
    tags: ''
  })

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    loadEntries()
  }, [isAuthenticated, router])

  const loadEntries = async () => {
    try {
      const response = await journalAPI.getEntries({ limit: 50 })
      setEntries(response.data.entries || [])
    } catch (error) {
      console.error('Error loading journal entries:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await journalAPI.createEntry(formData)
      setFormData({ notes: '', entry_type: 'general', mood: '', tags: '' })
      setShowForm(false)
      loadEntries()
    } catch (error: any) {
      console.error('Error creating entry:', error)
      alert(error.response?.data?.error || 'Failed to save journal entry')
    }
  }

  const handleDelete = async (entryId: string) => {
    try {
      await journalAPI.deleteEntry(entryId)
      loadEntries()
    } catch (error) {
      console.error('Error deleting entry:', error)
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
            {showForm ? 'Cancel' : 'New Entry'}
          </button>
        </div>

        {showForm && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Entry Type
                </label>
                <select
                  value={formData.entry_type}
                  onChange={(e) => setFormData({...formData, entry_type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="general">General</option>
                  <option value="pre_market">Pre-Market</option>
                  <option value="post_market">Post-Market</option>
                  <option value="trade_review">Trade Review</option>
                  <option value="psychology">Psychology</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notes
                </label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  required
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  placeholder="Write your journal entry..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Mood
                </label>
                <select
                  value={formData.mood}
                  onChange={(e) => setFormData({...formData, mood: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="">Select mood...</option>
                  <option value="confident">Confident</option>
                  <option value="neutral">Neutral</option>
                  <option value="anxious">Anxious</option>
                  <option value="fearful">Fearful</option>
                  <option value="excited">Excited</option>
                  <option value="frustrated">Frustrated</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tags (comma-separated)
                </label>
                <input
                  type="text"
                  value={formData.tags}
                  onChange={(e) => setFormData({...formData, tags: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  placeholder="e.g., breakout, patience, discipline"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
              >
                Save Entry
              </button>
            </form>
          </div>
        )}

        <div className="space-y-4">
          {entries.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-6 text-center text-gray-500">
              No journal entries yet. Start by creating your first entry!
            </div>
          ) : (
            entries.map((entry: any) => (
              <div key={entry.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <span className="inline-block px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded mb-2">
                      {entry.entry_type}
                    </span>
                    {entry.mood && (
                      <span className="inline-block px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded ml-2 mb-2">
                        {entry.mood}
                      </span>
                    )}
                  </div>
                  <button
                    onClick={() => handleDelete(entry.id)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Delete
                  </button>
                </div>
                <p className="text-gray-700 mb-2">{entry.notes}</p>
                <div className="text-sm text-gray-500">
                  {entry.created_at}
                  {entry.tags && (
                    <span className="ml-2">
                      Tags: {Array.isArray(entry.tags) ? entry.tags.join(', ') : entry.tags}
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  )
}
