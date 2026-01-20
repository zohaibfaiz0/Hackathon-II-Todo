'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useSession } from '@/lib/auth'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const { signIn } = useSession()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      await signIn(email, password)
      router.push('/dashboard')
      router.refresh()
    } catch (err) {
      setError('Invalid email or password')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <h2 className="text-3xl font-bold text-text-primary mb-2">Welcome back</h2>
      <p className="text-text-secondary text-base mb-8">Enter your credentials to continue</p>

      {error && (
        <div className="bg-error-light border-l-4 border-error p-3 rounded mb-5 flex items-start">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-error mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <span className="text-error text-sm">{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-text-primary mb-1.5">Email address</label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={`w-full h-12 bg-background border ${error ? 'border-error focus:ring-error/20' : 'border-border focus:ring-primary/20'} border rounded-md px-4 text-base placeholder-text-muted focus:outline-none focus:ring-2 focus:border-primary transition`}
            placeholder="Enter your email"
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-text-primary mb-1.5">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={`w-full h-12 bg-background border ${error ? 'border-error focus:ring-error/20' : 'border-border focus:ring-primary/20'} border rounded-md px-4 text-base placeholder-text-muted focus:outline-none focus:ring-2 focus:border-primary transition`}
            placeholder="Enter your password"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={`w-full h-12 bg-primary text-text-inverse rounded-md text-base font-semibold hover:bg-primary-hover transition-transform active:scale-98 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            </div>
          ) : (
            'Sign in'
          )}
        </button>
      </form>

      <div className="mt-6 text-center">
        <p className="text-text-secondary text-sm">
          Don't have an account?{' '}
          <Link href="/auth/signup" className="text-primary text-sm font-medium hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </>
  )
}