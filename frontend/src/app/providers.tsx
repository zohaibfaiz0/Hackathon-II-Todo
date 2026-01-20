'use client'

import { SessionProvider } from '@/lib/auth'

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>
}