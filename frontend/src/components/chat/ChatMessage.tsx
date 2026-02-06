'use client';

import React, { useState } from 'react';
import { ChatMessage as ChatMessageType, ToolCall } from '@/types/chat';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const [showToolCalls, setShowToolCalls] = useState(false);

  const isUser = message.role === 'user';
  const hasToolCalls = message.toolCalls && message.toolCalls.length > 0;

  const formatTime = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
      return '';
    }
  };

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md">
          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
      )}

      <div
        className={`
          max-w-[75%] rounded-2xl px-4 py-3 shadow-md
          ${isUser
            ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white rounded-tr-sm'
            : 'bg-white text-gray-800 rounded-tl-sm border border-gray-100'
          }
        `}
      >
        <p className="text-sm whitespace-pre-wrap break-words leading-relaxed">{message.content}</p>

        <p
          className={`
            text-[10px] mt-2 font-medium
            ${isUser ? 'text-blue-100' : 'text-gray-400'}
          `}
        >
          {formatTime(message.timestamp)}
        </p>

        {hasToolCalls && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <button
              onClick={() => setShowToolCalls(!showToolCalls)}
              className="text-xs text-gray-500 hover:text-gray-700 flex items-center gap-1.5 font-medium transition-colors"
            >
              <svg
                className={`w-3 h-3 transition-transform duration-200 ${showToolCalls ? 'rotate-90' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
              {showToolCalls ? 'Hide' : 'Show'} {message.toolCalls!.length} action{message.toolCalls!.length > 1 ? 's' : ''}
            </button>

            {showToolCalls && (
              <div className="mt-3 space-y-2">
                {message.toolCalls!.map((toolCall, index) => (
                  <ToolCallDisplay key={index} toolCall={toolCall} />
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 bg-gradient-to-br from-gray-200 to-gray-300 rounded-xl flex items-center justify-center flex-shrink-0 text-xs font-bold text-gray-600 shadow-md">
          U
        </div>
      )}
    </div>
  );
}

function ToolCallDisplay({ toolCall }: { toolCall: ToolCall }) {
  const getStatusEmoji = () => {
    if (toolCall.result.status === 'failed' || toolCall.result.error) {
      return '❌';
    }
    return '✅';
  };

  return (
    <div className="bg-gray-50 rounded-xl p-3 text-xs border border-gray-200 space-y-2">
      <div className="font-semibold text-gray-700 flex items-center gap-2">
        <span>{getStatusEmoji()}</span>
        <span className="text-blue-600">{toolCall.tool}</span>
      </div>
      <div className="space-y-1">
        <div className="text-gray-600">
          <span className="font-medium text-gray-700">Args:</span>{' '}
          <code className="bg-white px-2 py-0.5 rounded border border-gray-200 text-[10px]">
            {JSON.stringify(toolCall.arguments)}
          </code>
        </div>
        <div className="text-gray-600">
          <span className="font-medium text-gray-700">Result:</span>{' '}
          <code className="bg-white px-2 py-0.5 rounded border border-gray-200 text-[10px]">
            {JSON.stringify(toolCall.result)}
          </code>
        </div>
      </div>
    </div>
  );
}

export default ChatMessage;

