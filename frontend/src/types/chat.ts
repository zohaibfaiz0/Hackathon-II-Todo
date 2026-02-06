/**
 * Chat-related TypeScript types for Phase III AI Chatbot
 * These types match the backend Pydantic schemas in schemas/chat.py
 */

/**
 * Represents a single tool execution by the AI
 */
export interface ToolCall {
  /** Name of the tool that was called */
  tool: string;
  /** Arguments passed to the tool */
  arguments: Record<string, any>;
  /** Result returned from the tool */
  result: Record<string, any>;
}

/**
 * Represents a message in the chat conversation
 */
export interface ChatMessage {
  /** Unique message ID */
  id: number;
  /** Who sent the message */
  role: 'user' | 'assistant';
  /** Message content */
  content: string;
  /** ISO timestamp of when message was created */
  timestamp: string;
  /** Tool calls made during this message (assistant only) */
  toolCalls?: ToolCall[];
}

/**
 * Request body for POST /api/{user_id}/chat
 */
export interface ChatRequest {
  /** Optional conversation ID to continue existing conversation */
  conversation_id?: number;
  /** The user's message (1-2000 characters) */
  message: string;
}

/**
 * Response from POST /api/{user_id}/chat
 */
export interface ChatResponse {
  /** The conversation ID (new or existing) */
  conversation_id: number;
  /** The AI assistant's response text */
  response: string;
  /** List of tools that were called during processing */
  tool_calls: ToolCall[];
}

/**
 * Represents a chat conversation
 */
export interface Conversation {
  /** Unique conversation ID */
  id: number;
  /** ID of the user who owns this conversation */
  user_id: string;
  /** ISO timestamp of when conversation was created */
  created_at: string;
  /** ISO timestamp of last activity */
  updated_at: string;
}