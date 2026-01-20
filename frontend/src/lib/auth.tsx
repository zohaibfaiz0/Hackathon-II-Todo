// Real authentication implementation
import { useState, useEffect, createContext, useContext } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface User {
  id: string;
  email: string;
}

interface SessionData {
  user: User | null;
  token: string | null;
}

interface SessionContextType {
  data: SessionData | null;
  status: 'loading' | 'authenticated' | 'unauthenticated';
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

// Authentication functions
export const login = async (email: string, password: string): Promise<SessionData> => {
  try {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Login failed');
    }

    const data = await response.json();

    // Extract user ID from JWT token (the 'sub' claim in the payload)
    let userId = '';
    try {
      const tokenParts = data.access_token.split('.');
      if (tokenParts.length === 3) {
        const payload = atob(tokenParts[1]);
        const tokenPayload = JSON.parse(payload);
        userId = tokenPayload.sub || '';
      }
    } catch (e) {
      console.error('Error decoding JWT token:', e);
      throw new Error('Invalid token received from server');
    }

    const sessionData = {
      user: { id: userId, email: email },
      token: data.access_token
    };

    localStorage.setItem('session', JSON.stringify(sessionData));
    return sessionData;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};

export const signup = async (email: string, password: string): Promise<SessionData> => {
  try {
    const response = await fetch(`${API_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Signup failed');
    }

    const data = await response.json();

    // Extract user ID from JWT token (the 'sub' claim in the payload)
    let userId = '';
    try {
      const tokenParts = data.access_token.split('.');
      if (tokenParts.length === 3) {
        const payload = atob(tokenParts[1]);
        const tokenPayload = JSON.parse(payload);
        userId = tokenPayload.sub || '';
      }
    } catch (e) {
      console.error('Error decoding JWT token:', e);
      throw new Error('Invalid token received from server');
    }

    const sessionData = {
      user: { id: userId, email: email },
      token: data.access_token
    };

    localStorage.setItem('session', JSON.stringify(sessionData));
    return sessionData;
  } catch (error) {
    console.error('Signup failed:', error);
    throw error;
  }
};

export const logout = (): void => {
  localStorage.removeItem('session');
  window.location.href = '/auth/login';
};

// Custom hook for session management
export const useSession = (): SessionContextType => {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
};

// Session provider component
export const SessionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sessionData, setSessionData] = useState<SessionData | null>(null);
  const [status, setStatus] = useState<'loading' | 'authenticated' | 'unauthenticated'>('loading');

  useEffect(() => {
    // Initialize session on mount
    const initSession = () => {
      try {
        const sessionStr = localStorage.getItem('session');
        if (sessionStr) {
          const session = JSON.parse(sessionStr);
          setSessionData(session);
          setStatus('authenticated');
        } else {
          setSessionData(null);
          setStatus('unauthenticated');
        }
      } catch (error) {
        console.error('Error initializing session:', error);
        setSessionData(null);
        setStatus('unauthenticated');
      }
    };

    initSession();
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const session = await login(email, password);
      setSessionData(session);
      setStatus('authenticated');
    } catch (error) {
      throw error;
    }
  };

  const signUp = async (email: string, password: string) => {
    try {
      const session = await signup(email, password);
      setSessionData(session);
      setStatus('authenticated');
    } catch (error) {
      throw error;
    }
  };

  const signOut = () => {
    logout();
    setSessionData(null);
    setStatus('unauthenticated');
  };

  const value: SessionContextType = {
    data: sessionData,
    status,
    signIn,
    signUp,
    signOut
  };

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  );
};