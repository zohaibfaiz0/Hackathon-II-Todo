'use client';

import React, { useState, useEffect, useRef } from 'react';
import { ChatMessage as ChatMessageType, ChatResponse } from '@/types/chat';
import { ChatInput } from './ChatInput';
import { ChatMessage } from './ChatMessage';
import { sendChatMessage } from '@/lib/chat';
import { useSession } from '@/lib/auth';

interface ChatWindowProps {
  initialConversationId?: number;
  onConversationChange?: (conversationId: number) => void;
  onTaskUpdate?: () => void;
}

export function ChatWindow({ 
  initialConversationId,
  onConversationChange,
  onTaskUpdate
}: ChatWindowProps) {
  const { data: session, status } = useSession();
  
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(
    initialConversationId ?? null
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async (messageText: string) => {
    const userMessage: ChatMessageType = {
      id: Date.now(),
      role: 'user',
      content: messageText,
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response: ChatResponse = await sendChatMessage(
        messageText,
        conversationId ?? undefined
      );

      if (response.conversation_id !== conversationId) {
        setConversationId(response.conversation_id);
        onConversationChange?.(response.conversation_id);
      }

      if (response.tool_calls && response.tool_calls.length > 0) {
        onTaskUpdate?.();
      }

      const assistantMessage: ChatMessageType = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        toolCalls: response.tool_calls.length > 0 ? response.tool_calls : undefined,
      };

      setMessages(prev => [...prev, assistantMessage]);
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  if (status === 'loading') {
    return (
      <div className="flex flex-col h-full items-center justify-center bg-gradient-to-b from-gray-50 to-white">
        <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (status === 'unauthenticated') {
    return (
      <div className="flex flex-col h-full items-center justify-center bg-gradient-to-b from-gray-50 to-white p-6 text-center">
        <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mb-4">
          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <p className="text-gray-500 text-sm font-medium">Please log in to chat</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-gray-50 to-white">
      {/* Premium Header */}
      <div className="relative bg-gradient-to-r from-blue-600 to-indigo-600 p-5 shadow-lg">
        <div className="absolute inset-0 bg-black/10" />
        <div className="relative flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center shadow-lg">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="font-bold text-white">AI Assistant</h3>
            <p className="text-xs text-blue-100 font-medium">Here to help you stay productive</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse shadow-lg shadow-green-400/50" />
            <span className="text-[10px] text-white/80 font-semibold uppercase tracking-wide">Online</span>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-5 space-y-4">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-gray-400 space-y-4">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-2xl flex items-center justify-center">
              <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <p className="text-sm font-medium text-gray-500">How can I help you today?</p>
            <div className="flex flex-wrap gap-2 justify-center max-w-xs">
              <span className="px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs text-gray-600">Add a task</span>
              <span className="px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs text-gray-600">Show pending</span>
              <span className="px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs text-gray-600">Complete task</span>
            </div>
          </div>
        )}
        
        {messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-100 rounded-2xl rounded-tl-sm px-5 py-3 shadow-md">
              <div className="flex gap-1.5 items-center">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}
        
        {error && (
          <div className="flex justify-center my-2">
            <div className="bg-red-50 text-red-600 text-xs py-2 px-4 rounded-xl flex items-center gap-2 border border-red-200 shadow-sm">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="font-medium">{error}</span>
              <button onClick={() => setError(null)} className="ml-2 font-bold hover:text-red-800 transition-colors">×</button>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
}

export default ChatWindow;

