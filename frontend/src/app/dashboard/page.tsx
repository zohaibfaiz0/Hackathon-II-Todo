'use client'

import { useState, useEffect, useRef } from 'react'
import { useSession } from '@/lib/auth'
import { getTasks, createTask, updateTask, deleteTask, toggleTaskComplete } from '@/lib/api'
import { Task } from '@/types'
import { ChatWindow } from '@/components/chat'

export default function DashboardPage() {
  const { data: sessionData, status, signOut } = useSession()
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all')
  const [newTaskTitle, setNewTaskTitle] = useState('')
  const [creatingTask, setCreatingTask] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDesc, setEditDesc] = useState('')
  const [showDropdown, setShowDropdown] = useState(false)
  const [isChatOpen, setIsChatOpen] = useState(false)
  const profileRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (profileRef.current && !profileRef.current.contains(event.target as Node)) {
        setShowDropdown(false)
      }
    }

    if (showDropdown) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [showDropdown])

  useEffect(() => {
    if (status === 'authenticated') fetchTasks()
  }, [status])

  const fetchTasks = async () => {
    try {
      if (tasks.length === 0) setLoading(true)
      const data = await getTasks()
      setTasks(data)
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTaskTitle.trim()) return
    setCreatingTask(true)
    try {
      const newTask = await createTask({ title: newTaskTitle, description: '' })
      setTasks([newTask, ...tasks])
      setNewTaskTitle('')
    } catch (error) {
      console.error('Failed to create task:', error)
    } finally {
      setCreatingTask(false)
    }
  }

  const handleToggleComplete = async (taskId: number) => {
    try {
      const updatedTask = await toggleTaskComplete(taskId)
      setTasks(tasks.map(t => t.id === taskId ? updatedTask : t))
    } catch (error) {
      console.error('Failed to update task:', error)
    }
  }

  const handleDeleteTask = async (taskId: number) => {
    try {
      await deleteTask(taskId)
      setTasks(tasks.filter(t => t.id !== taskId))
    } catch (error) {
      console.error('Failed to delete task:', error)
    }
  }

  const openEdit = (task: Task) => {
    setEditingTask(task)
    setEditTitle(task.title)
    setEditDesc(task.description || '')
  }

  const handleSaveEdit = async () => {
    if (!editingTask) return
    try {
      const updated = await updateTask(editingTask.id, { title: editTitle, description: editDesc })
      setTasks(tasks.map(t => t.id === editingTask.id ? updated : t))
      setEditingTask(null)
    } catch (error) {
      console.error('Failed to update task:', error)
    }
  }

  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return !task.completed
    if (filter === 'completed') return task.completed
    return true
  })

  const pendingCount = tasks.filter(t => !t.completed).length

  const handleProfileClick = () => {
    if (!showDropdown && isChatOpen) {
      setIsChatOpen(false)
    }
    setShowDropdown(!showDropdown)
  }

  const handleSignOut = () => {
    setShowDropdown(false)
    signOut()
  }

  if (status === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (status === 'unauthenticated') {
    if (typeof window !== 'undefined') window.location.href = '/auth/login'
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Animated Background Orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none" style={{ zIndex: 0 }}>
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-400/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute top-1/2 -left-40 w-80 h-80 bg-indigo-400/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute bottom-20 right-1/3 w-60 h-60 bg-purple-400/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      {/* Header */}
      <header 
        className="sticky top-0 backdrop-blur-xl bg-white/70 border-b border-white/20 shadow-lg shadow-black/5"
        style={{ zIndex: 100 }}
      >
        <div className="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl blur opacity-75" />
              <div className="relative w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
            <div>
              <span className="font-bold text-lg bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">TaskFlow</span>
              <div className="h-1 w-full bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full" />
            </div>
          </div>

          {/* Profile Button */}
          <div ref={profileRef} className="relative">
            <button
              type="button"
              onClick={handleProfileClick}
              style={{
                width: 40,
                height: 40,
                background: 'linear-gradient(135deg, #2563eb 0%, #4f46e5 100%)',
                borderRadius: 12,
                border: 'none',
                cursor: 'pointer',
                color: 'white',
                fontWeight: 600,
                fontSize: 14,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 4px 12px rgba(37, 99, 235, 0.4)',
                transition: 'transform 0.2s, box-shadow 0.2s',
                position: 'relative',
                zIndex: 101,
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'scale(1.05)'
                e.currentTarget.style.boxShadow = '0 6px 20px rgba(37, 99, 235, 0.5)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'scale(1)'
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.4)'
              }}
            >
              {sessionData?.user?.email?.[0]?.toUpperCase() || 'U'}
            </button>

            {showDropdown && (
              <div
                style={{
                  position: 'absolute',
                  right: 0,
                  top: '100%',
                  marginTop: 12,
                  width: 240,
                  background: 'white',
                  borderRadius: 16,
                  boxShadow: '0 20px 40px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.05)',
                  zIndex: 102,
                  overflow: 'hidden',
                }}
              >
                <div style={{ padding: 16, borderBottom: '1px solid #f1f5f9' }}>
                  <p style={{ fontSize: 12, color: '#64748b', marginBottom: 4 }}>Signed in as</p>
                  <p style={{ fontSize: 14, fontWeight: 500, color: '#1e293b', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {sessionData?.user?.email}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={handleSignOut}
                  style={{
                    width: '100%',
                    padding: '14px 16px',
                    textAlign: 'left',
                    fontSize: 14,
                    fontWeight: 500,
                    color: '#ef4444',
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    transition: 'background 0.2s',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = '#fef2f2'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'transparent'
                  }}
                >
                  Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Dropdown Backdrop */}
      {showDropdown && (
        <div
          onClick={() => setShowDropdown(false)}
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 99,
            background: 'transparent',
          }}
        />
      )}

      {/* Main Content */}
      <main className="relative max-w-4xl mx-auto px-6 py-8" style={{ zIndex: 1 }}>
        {/* Hero Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            My Tasks
            <span className="inline-block ml-3 text-2xl">✨</span>
          </h1>
          <p className="text-gray-600">
            {pendingCount === 0 ? (
              <span className="flex items-center gap-2">
                All caught up! Time to relax 🎉
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-gradient-to-br from-blue-600 to-indigo-600 text-white text-xs font-bold rounded-full">{pendingCount}</span>
                {pendingCount === 1 ? 'task' : 'tasks'} waiting for you
              </span>
            )}
          </p>
        </div>

        {/* Add Task Card */}
        <form onSubmit={handleCreateTask} className="mb-6">
          <div className="group relative bg-white/60 backdrop-blur-sm rounded-2xl shadow-lg shadow-black/5 border border-white/20 p-6 hover:shadow-xl transition-all duration-300">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-600/5 to-indigo-600/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
            <div className="relative flex gap-3">
              <input
                type="text"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                placeholder="What needs to be done?"
                className="flex-1 bg-white/50 border-2 border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:bg-white transition-all duration-200"
              />
              <button
                type="submit"
                disabled={creatingTask || !newTaskTitle.trim()}
                className="relative px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 hover:scale-105 disabled:hover:scale-100 overflow-hidden group"
              >
                <span className="relative z-10">{creatingTask ? 'Adding...' : 'Add Task'}</span>
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
              </button>
            </div>
          </div>
        </form>

        {/* Filters */}
        <div className="mb-6 flex gap-3">
          {(['all', 'pending', 'completed'] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`
                relative px-6 py-2.5 rounded-xl font-medium text-sm transition-all duration-300 overflow-hidden
                ${filter === f 
                  ? 'text-white shadow-lg scale-105' 
                  : 'text-gray-600 hover:bg-white/50 hover:scale-105'
                }
              `}
            >
              {filter === f && (
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 pointer-events-none" />
              )}
              {filter !== f && (
                <div className="absolute inset-0 bg-white/40 backdrop-blur-sm pointer-events-none" />
              )}
              <span className="relative z-10 capitalize">{f}</span>
            </button>
          ))}
        </div>

        {/* Task List */}
        <div className="space-y-3">
          {loading ? (
            Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="h-20 bg-white/40 backdrop-blur-sm rounded-2xl border border-white/20 animate-pulse" />
            ))
          ) : filteredTasks.length === 0 ? (
            <div className="text-center py-20 bg-white/40 backdrop-blur-sm rounded-2xl border border-white/20">
              <div className="w-16 h-16 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="1.5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p className="text-gray-500 font-medium">No tasks here</p>
            </div>
          ) : (
            filteredTasks.map((task) => (
              <div
                key={task.id}
                className="group relative bg-white/60 backdrop-blur-sm rounded-2xl shadow-md hover:shadow-xl border border-white/20 p-4 transition-all duration-300 hover:scale-[1.02]"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-blue-600/5 to-indigo-600/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                <div className="relative flex items-center gap-4">
                  <button
                    onClick={() => handleToggleComplete(task.id)}
                    className={`
                      relative flex-shrink-0 w-6 h-6 rounded-lg border-2 transition-all duration-300
                      ${task.completed 
                        ? 'bg-gradient-to-br from-green-500 to-emerald-600 border-green-500 scale-110' 
                        : 'border-gray-300 hover:border-blue-500 hover:scale-110'
                      }
                    `}
                  >
                    {task.completed && (
                      <svg className="w-full h-full p-0.5" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </button>

                  <div className="flex-1 min-w-0">
                    <p className={`font-medium transition-all duration-300 ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900'}`}>
                      {task.title}
                    </p>
                    {task.description && (
                      <p className="text-sm text-gray-500 mt-0.5 truncate">{task.description}</p>
                    )}
                  </div>

                  <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <button
                      onClick={() => openEdit(task)}
                      className="w-9 h-9 flex items-center justify-center rounded-lg hover:bg-blue-50 transition-colors duration-200"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      onClick={() => handleDeleteTask(task.id)}
                      className="w-9 h-9 flex items-center justify-center rounded-lg hover:bg-red-50 transition-colors duration-200"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </main>

      {/* Edit Modal */}
      {editingTask && (
        <div className="fixed inset-0 flex items-center justify-center p-4" style={{ zIndex: 200 }}>
          <div onClick={() => setEditingTask(null)} className="absolute inset-0 bg-black/40 backdrop-blur-sm" />
          <div className="relative bg-white rounded-3xl w-full max-w-md shadow-2xl overflow-hidden transform transition-all">
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-indigo-600" />
            
            <div className="flex items-center justify-between p-6 border-b border-gray-100">
              <h2 className="text-xl font-bold text-gray-900">Edit Task</h2>
              <button
                onClick={() => setEditingTask(null)}
                className="w-10 h-10 flex items-center justify-center rounded-xl hover:bg-gray-100 transition-colors duration-200"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6b7280" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="p-6 space-y-5">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Title</label>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-50 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
                <textarea
                  value={editDesc}
                  onChange={(e) => setEditDesc(e.target.value)}
                  rows={3}
                  className="w-full px-4 py-3 bg-gray-50 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:bg-white resize-none transition-all duration-200"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 p-6 bg-gray-50 border-t border-gray-100">
              <button
                onClick={() => setEditingTask(null)}
                className="px-6 py-2.5 font-medium text-gray-700 bg-white border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-colors duration-200"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveEdit}
                className="relative px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 overflow-hidden group"
              >
                <span className="relative z-10">Save Changes</span>
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ============================================ */}
      {/* FIXED: Floating Chat with Responsive Height */}
      {/* ============================================ */}
      <div 
        className="fixed bottom-6 right-6 flex flex-col items-end"
        style={{ 
          zIndex: showDropdown ? 50 : 90,
          pointerEvents: 'none',
        }}
      >
        {/* Chat Window - NOW WITH RESPONSIVE HEIGHT */}
        <div 
          className={`
            transition-all duration-500 ease-out mb-4
            ${isChatOpen 
              ? 'opacity-100 scale-100 translate-y-0' 
              : 'opacity-0 scale-95 translate-y-8'
            }
          `}
          style={{ 
            pointerEvents: isChatOpen ? 'auto' : 'none',
          }}
        >
          {/* 
            KEY FIX: Using CSS clamp/min to make height responsive
            - Minimum: 400px (so it's still usable on small screens)
            - Preferred: calc(100vh - 140px) (viewport minus button + margins)
            - Maximum: 600px (original height on large screens)
          */}
          <div 
            className="w-96 max-w-[calc(100vw-48px)] bg-white rounded-3xl shadow-2xl border border-gray-200/50 overflow-hidden flex flex-col"
            style={{
              height: '450px',
            }}
          >
            {isChatOpen && <ChatWindow onTaskUpdate={fetchTasks} />}
          </div>
        </div>

        {/* Floating Toggle Button */}
        <button
          onClick={() => setIsChatOpen(!isChatOpen)}
          style={{ pointerEvents: 'auto' }}
          className={`
            relative group w-16 h-16 rounded-2xl shadow-2xl flex items-center justify-center transition-all duration-500 flex-shrink-0
            ${isChatOpen 
              ? 'bg-gray-900 rotate-90 hover:bg-black scale-95' 
              : 'bg-gradient-to-br from-blue-600 to-indigo-600 hover:scale-110'
            }
          `}
        >
          <div className={`absolute inset-0 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none ${isChatOpen ? 'hidden' : ''}`} />
          {isChatOpen ? (
            <svg className="w-7 h-7 text-white relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <div className="relative z-10">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white animate-pulse" />
            </div>
          )}
        </button>
      </div>
    </div>
  )
}