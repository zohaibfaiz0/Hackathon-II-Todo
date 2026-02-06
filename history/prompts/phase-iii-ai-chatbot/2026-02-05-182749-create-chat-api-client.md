---
id: phr-322-20260205182749
stage: green
date: 2026-02-05
title: Create Chat API Client
feature: phase-iii-ai-chatbot
---

# Create Chat API Client

## Prompt Text

```
# Implement T-319: Create chat API client

## Task Reference
- Task ID: T-319
- Spec: @specs/phase-iii-ai-chatbot/spec.md (Section 5.1)
- Plan: @specs/phase-iii-ai-chatbot/plan.md (Section 6.1)
- Dependencies: T-318 (chat types)

## File to Create
`frontend/src/lib/chat.ts`

## Context Reference
Read these files to understand existing patterns:
- @frontend/src/lib/api.ts (API client pattern)
- @frontend/src/types/chat.ts (ChatResponse interface)

## Requirements

Create a client-side API client for chat functionality that:
1. Uses 'use client' directive
2. Imports ChatResponse from '@/types/chat'
3. Defines API_BASE_URL constant with fallback
4. Includes getSessionData function (extracts session from localStorage)
5. Exports sendChatMessage function with signature:
   - Parameters: message (string), conversationId? (number)
   - Returns: Promise<ChatResponse>
6. Uses fetch API with async/await
7. Attaches JWT token from session as Bearer
8. Sends conversation_id and message in request body
9. Handles errors appropriately
10. Both named and default export

### Expected Implementation Pattern
```typescript
'use client';

import { ChatResponse } from '@/types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const getSessionData = (): { userId: string; token: string } | null => {
  if (typeof window === 'undefined') return null;
  const sessionStr = localStorage.getItem('session');
  if (!sessionStr) return null;
  try {
    const session = JSON.parse(sessionStr);
    const userId = session.user?.id;
    const token = session.token;
    if (!userId || !token) return null;
    return { userId, token };
  } catch (e) {
    console.error('Failed to parse session data', e);
    return null;
  }
};

export const sendChatMessage = async (
  message: string,
  conversationId?: number
): Promise<ChatResponse> => {
  const sessionData = getSessionData();
  if (!sessionData) {
    throw new Error('User not authenticated');
  }

  const { userId, token } = sessionData;
  const url = `${API_BASE_URL}/api/${userId}/chat`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      message: message,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

export default sendChatMessage;
```

### Key Implementation Notes
1. Use same pattern as existing api.ts for session handling
2. Follow existing API client conventions (headers, error handling)
3. Use POST /api/{user_id}/chat endpoint (per spec)
4. Include conversation_id in request body (optional)
5. Include message in request body (required)
6. Attach Bearer token from session
7. Handle JSON parsing safely with .catch fallback

## Verification

After creating the file, verify:

```bash
cd frontend
npx tsc --noEmit src/lib/chat.ts
```

### Verify Exports
```bash
cd frontend
echo "=== Checking exports ==="
grep -E "^export" src/lib/chat.ts
```

### Verify Implementation Details
```bash
cd frontend
echo "=== Checking implementation ==="
grep -E "API_BASE_URL|getSessionData|sendChatMessage" src/lib/chat.ts
echo "=== Checking auth pattern ==="
grep -C 3 "Bearer" src/lib/chat.ts
```

## Acceptance Criteria Checklist
- [x] File created at `frontend/src/lib/chat.ts`
- [x] Uses 'use client' directive
- [x] Imports ChatResponse from '@/types/chat'
- [x] API_BASE_URL constant with fallback
- [x] getSessionData function extracts session from localStorage
- [x] sendChatMessage function with correct signature
- [x] Uses fetch API with async/await
- [x] Attaches JWT token as Bearer
- [x] Sends conversation_id and message in body
- [x] Handles errors appropriately
- [x] Named export: sendChatMessage
- [x] Default export: sendChatMessage
- [x] TypeScript compilation passes

## DO NOT
- Modify any existing files
- Use external HTTP libraries (use native fetch)
- Skip error handling
- Hardcode API URL (use environment variable)
- Forget to attach auth token
- Break existing API client patterns
```

## Response Text

Implemented T-319 by creating the chat API client at `frontend/src/lib/chat.ts` with all required functionality:

- Added 'use client' directive
- Imported ChatResponse from '@/types/chat'
- Created API_BASE_URL constant with fallback to environment variable
- Implemented getSessionData function to extract userId and token from localStorage session
- Created sendChatMessage function with proper signature (message: string, conversationId?: number)
- Used fetch API with async/await pattern
- Attached JWT token as Bearer in Authorization header
- Sent conversation_id and message in request body
- Implemented proper error handling with fallbacks
- Added both named and default exports for sendChatMessage
- Ensured TypeScript compilation passes

The implementation follows the same patterns as the existing api.ts file and integrates properly with the session management system.