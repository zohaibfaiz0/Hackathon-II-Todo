'use client'

import { useState, useEffect } from 'react'
import { useSession } from '@/lib/auth'
import { getTasks, createTask, updateTask, deleteTask, toggleTaskComplete } from '@/lib/api'
import { Task } from '@/types'

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

  useEffect(() => {
    if (status === 'authenticated') fetchTasks()
  }, [status])

  const fetchTasks = async () => {
    try {
      setLoading(true)
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

  if (status === 'loading') {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f8fafc' }}>
        <div style={{ width: 24, height: 24, border: '2px solid #6366f1', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    )
  }

  if (status === 'unauthenticated') {
    if (typeof window !== 'undefined') window.location.href = '/auth/login'
    return null
  }

  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return !task.completed
    if (filter === 'completed') return task.completed
    return true
  })

  const pendingCount = tasks.filter(t => !t.completed).length

  return (
    <div style={{ minHeight: '100vh', background: '#f8fafc', fontFamily: 'Inter, -apple-system, sans-serif' }}>
      {/* Header */}
      <header style={{ background: '#fff', borderBottom: '1px solid #e2e8f0', position: 'sticky', top: 0, zIndex: 20 }}>
        <div style={{ maxWidth: 640, margin: '0 auto', padding: '0 16px', height: 56, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div style={{ width: 28, height: 28, background: '#6366f1', borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <span style={{ fontWeight: 600, color: '#1e293b', fontSize: 16 }}>TaskFlow</span>
          </div>
          
          <div style={{ position: 'relative' }}>
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              style={{ width: 32, height: 32, background: '#6366f1', borderRadius: '50%', border: 'none', cursor: 'pointer', color: '#fff', fontSize: 13, fontWeight: 500, display: 'flex', alignItems: 'center', justifyContent: 'center' }}
            >
              {sessionData?.user?.email?.[0]?.toUpperCase() || 'U'}
            </button>
            
            {showDropdown && (
              <>
                <div onClick={() => setShowDropdown(false)} style={{ position: 'fixed', inset: 0, zIndex: 30 }} />
                <div style={{ position: 'absolute', right: 0, marginTop: 8, width: 180, background: '#fff', borderRadius: 8, boxShadow: '0 4px 12px rgba(0,0,0,0.1)', border: '1px solid #e2e8f0', zIndex: 40, overflow: 'hidden' }}>
                  <div style={{ padding: '10px 12px', fontSize: 12, color: '#64748b', borderBottom: '1px solid #f1f5f9' }}>
                    {sessionData?.user?.email}
                  </div>
                  <button
                    onClick={() => signOut()}
                    style={{ width: '100%', padding: '10px 12px', textAlign: 'left', fontSize: 13, color: '#ef4444', background: 'none', border: 'none', cursor: 'pointer' }}
                  >
                    Sign out
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Main */}
      <main style={{ maxWidth: 640, margin: '0 auto', padding: '24px 16px' }}>
        <div style={{ marginBottom: 24 }}>
          <h1 style={{ fontSize: 20, fontWeight: 700, color: '#1e293b', margin: 0 }}>My Tasks</h1>
          <p style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>
            {pendingCount === 0 ? 'All done! 🎉' : `${pendingCount} task${pendingCount > 1 ? 's' : ''} remaining`}
          </p>
        </div>

        {/* Add Task */}
        <form onSubmit={handleCreateTask} style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
          <input
            type="text"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="Add a new task..."
            style={{ flex: 1, height: 40, padding: '0 12px', fontSize: 14, background: '#fff', border: '1px solid #e2e8f0', borderRadius: 8, outline: 'none' }}
          />
          <button
            type="submit"
            disabled={creatingTask || !newTaskTitle.trim()}
            style={{ height: 40, padding: '0 16px', background: '#6366f1', color: '#fff', fontSize: 13, fontWeight: 500, border: 'none', borderRadius: 8, cursor: 'pointer', opacity: creatingTask || !newTaskTitle.trim() ? 0.5 : 1 }}
          >
            {creatingTask ? 'Adding...' : 'Add'}
          </button>
        </form>

        {/* Filters */}
        <div style={{ display: 'inline-flex', gap: 4, padding: 4, background: '#fff', borderRadius: 8, border: '1px solid #e2e8f0', marginBottom: 20 }}>
          {(['all', 'pending', 'completed'] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={{ padding: '6px 12px', fontSize: 12, fontWeight: 500, border: 'none', borderRadius: 6, cursor: 'pointer', background: filter === f ? '#6366f1' : 'transparent', color: filter === f ? '#fff' : '#64748b' }}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>

        {/* Task List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {loading ? (
            Array.from({ length: 3 }).map((_, i) => (
              <div key={i} style={{ height: 52, background: '#fff', borderRadius: 8, border: '1px solid #e2e8f0' }} />
            ))
          ) : filteredTasks.length === 0 ? (
            <div style={{ padding: '48px 0', textAlign: 'center' }}>
              <div style={{ width: 48, height: 48, background: '#f1f5f9', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 12px' }}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" strokeWidth="1.5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p style={{ fontSize: 13, color: '#64748b' }}>No tasks</p>
            </div>
          ) : (
            filteredTasks.map((task) => (
              <div key={task.id} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: 12, background: '#fff', borderRadius: 8, border: '1px solid #e2e8f0' }}>
                <button
                  onClick={() => handleToggleComplete(task.id)}
                  style={{ width: 20, height: 20, borderRadius: 5, border: task.completed ? 'none' : '2px solid #cbd5e1', background: task.completed ? '#10b981' : 'transparent', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}
                >
                  {task.completed && (
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="3">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  )}
                </button>

                <div style={{ flex: 1, minWidth: 0 }}>
                  <p style={{ fontSize: 14, color: task.completed ? '#94a3b8' : '#1e293b', textDecoration: task.completed ? 'line-through' : 'none', margin: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {task.title}
                  </p>
                  {task.description && (
                    <p style={{ fontSize: 12, color: '#94a3b8', margin: '2px 0 0', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {task.description}
                    </p>
                  )}
                </div>

                <div style={{ display: 'flex', gap: 4 }}>
                  <button onClick={() => openEdit(task)} style={{ width: 28, height: 28, background: 'transparent', border: 'none', borderRadius: 6, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button onClick={() => handleDeleteTask(task.id)} style={{ width: 28, height: 28, background: 'transparent', border: 'none', borderRadius: 6, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </main>

      {/* Edit Modal */}
      {editingTask && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 50, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16 }}>
          <div onClick={() => setEditingTask(null)} style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.4)' }} />
          <div style={{ position: 'relative', background: '#fff', borderRadius: 12, width: '100%', maxWidth: 400, boxShadow: '0 20px 40px rgba(0,0,0,0.15)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 16, borderBottom: '1px solid #e2e8f0' }}>
              <h2 style={{ fontSize: 16, fontWeight: 600, color: '#1e293b', margin: 0 }}>Edit Task</h2>
              <button onClick={() => setEditingTask(null)} style={{ width: 28, height: 28, background: 'transparent', border: 'none', borderRadius: 6, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div style={{ padding: 16, display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div>
                <label style={{ display: 'block', fontSize: 13, fontWeight: 500, color: '#374151', marginBottom: 6 }}>Title</label>
                <input type="text" value={editTitle} onChange={(e) => setEditTitle(e.target.value)} style={{ width: '100%', height: 40, padding: '0 12px', fontSize: 14, border: '1px solid #e2e8f0', borderRadius: 8, outline: 'none', boxSizing: 'border-box' }} />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: 13, fontWeight: 500, color: '#374151', marginBottom: 6 }}>Description</label>
                <textarea value={editDesc} onChange={(e) => setEditDesc(e.target.value)} rows={3} style={{ width: '100%', padding: 12, fontSize: 14, border: '1px solid #e2e8f0', borderRadius: 8, outline: 'none', resize: 'none', boxSizing: 'border-box' }} />
              </div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8, padding: 16, borderTop: '1px solid #e2e8f0' }}>
              <button onClick={() => setEditingTask(null)} style={{ padding: '8px 16px', fontSize: 13, fontWeight: 500, color: '#64748b', background: 'transparent', border: '1px solid #e2e8f0', borderRadius: 8, cursor: 'pointer' }}>Cancel</button>
              <button onClick={handleSaveEdit} style={{ padding: '8px 16px', fontSize: 13, fontWeight: 500, color: '#fff', background: '#6366f1', border: 'none', borderRadius: 8, cursor: 'pointer' }}>Save</button>
            </div>
          </div>
        </div>
      )}

      <style>{`@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');`}</style>
    </div>
  )
}