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