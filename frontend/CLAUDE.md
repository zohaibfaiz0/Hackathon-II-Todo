# Frontend Guidelines

## Stack
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Custom JWT Auth (not Better Auth - simplified implementation)

## Project Structure
```
frontend/src/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout with providers
│   ├── page.tsx            # Landing page
│   ├── auth/
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   └── dashboard/
│       └── page.tsx        # Main task management UI
├── components/
│   ├── ui/                 # Reusable UI components
│   ├── auth/               # Auth-related components
│   └── tasks/              # Task-related components
├── lib/
│   ├── api.ts              # Backend API client
│   └── auth.tsx            # Auth context, hooks, functions
└── types/
    └── index.ts            # TypeScript interfaces
```

## Authentication
- Uses custom JWT implementation (not Better Auth)
- Session stored in localStorage as JSON: `{user: {id, email}, token}`
- `useSession()` hook provides: `data`, `status`, `signIn`, `signUp`, `signOut`
- `SessionProvider` wraps app in layout.tsx

## API Client (`lib/api.ts`)
- Extracts user_id and token from localStorage session
- Builds URLs: `/api/{user_id}/tasks/...`
- Attaches `Authorization: Bearer <token>` header
- Handles errors and returns typed responses

## Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Patterns
- Use 'use client' directive for interactive components
- Server components for static content
- All API calls go through `lib/api.ts`
- Auth state via `useSession()` hook from `lib/auth.tsx`

## Running Locally
```bash
cd frontend
npm install
npm run dev
```

## Building
```bash
npm run build
npm start
```