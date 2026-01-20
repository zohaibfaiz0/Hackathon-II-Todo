import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Auth | TaskFlow',
  description: 'Authentication pages for TaskFlow',
}

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-background flex">
      {/* Left side - Branding (hidden on mobile) */}
      <div className="hidden md:flex md:w-1/2 bg-gradient-to-br from-primary to-violet-500 items-center justify-center p-12">
        <div className="max-w-md text-center">
          <div className="w-20 h-20 rounded-full bg-white bg-opacity-20 flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-white mb-4">TaskFlow</h1>
          <p className="text-white text-opacity-80 text-lg">Organize your life, one task at a time</p>

          {/* Decorative floating task cards */}
          <div className="absolute top-20 left-20 w-16 h-20 bg-white bg-opacity-10 rounded-lg transform rotate-6 animate-pulse"></div>
          <div className="absolute top-40 right-24 w-12 h-16 bg-white bg-opacity-10 rounded-lg transform -rotate-3 animate-pulse"></div>
          <div className="absolute bottom-20 left-1/3 w-14 h-18 bg-white bg-opacity-10 rounded-lg transform rotate-12 animate-pulse"></div>
        </div>
      </div>

      {/* Right side - Form */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-4 md:p-0">
        <div className="w-full max-w-md bg-surface rounded-xl shadow-md p-12">
          {children}
        </div>
      </div>
    </div>
  )
}