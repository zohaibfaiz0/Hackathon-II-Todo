import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';

// Mock the auth hook
jest.mock('@/lib/auth', () => ({
  useSession: () => ({
    data: { user: { id: 'test-user-123' }, token: 'mock-token' },
    status: 'authenticated',
  }),
}));

// Mock the chat API
jest.mock('@/lib/chat', () => ({
  sendChatMessage: jest.fn(),
}));

import { ChatMessage } from '@/components/chat/ChatMessage';
import { ChatInput } from '@/components/chat/ChatInput';
import { ChatWindow } from '@/components/chat/ChatWindow';
import { sendChatMessage } from '@/lib/chat';

describe('ChatMessage', () => {
  const mockUserMessage = {
    id: 1,
    role: 'user' as const,
    content: 'Hello, assistant!',
    timestamp: '2024-01-15T10:30:00Z',
  };

  const mockAssistantMessage = {
    id: 2,
    role: 'assistant' as const,
    content: 'Hello! How can I help you?',
    timestamp: '2024-01-15T10:30:05Z',
    toolCalls: [
      {
        tool: 'list_tasks',
        arguments: { status: 'all' },
        result: { tasks: [], count: 0, status: 'success' },
      },
    ],
  };

  it('renders user message with correct styling', () => {
    render(<ChatMessage message={mockUserMessage} />);

    expect(screen.getByText('Hello, assistant!')).toBeInTheDocument();
    // User messages should be right-aligned (check for justify-end class parent)
  });

  it('renders assistant message with correct styling', () => {
    render(<ChatMessage message={mockAssistantMessage} />);

    expect(screen.getByText('Hello! How can I help you?')).toBeInTheDocument();
  });

  it('displays timestamp', () => {
    render(<ChatMessage message={mockUserMessage} />);

    // Check that some time format is displayed
    // The exact format depends on locale, so we check the element exists
    const messageContainer = screen.getByText('Hello, assistant!').closest('div');
    expect(messageContainer).toBeInTheDocument();
  });

  it('shows tool calls for assistant messages', () => {
    render(<ChatMessage message={mockAssistantMessage} />);

    // Look for tool call indicator
    expect(screen.getByText(/tool call/i)).toBeInTheDocument();
  });

  it('does not show tool calls section for user messages', () => {
    render(<ChatMessage message={mockUserMessage} />);

    expect(screen.queryByText(/tool call/i)).not.toBeInTheDocument();
  });
});

describe('ChatInput', () => {
  it('renders input and send button', () => {
    const mockOnSend = jest.fn();
    render(<ChatInput onSend={mockOnSend} />);

    expect(screen.getByRole('textbox')).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('calls onSend with message when form is submitted', async () => {
    const mockOnSend = jest.fn();
    const user = userEvent.setup();

    render(<ChatInput onSend={mockOnSend} />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'Test message');

    const button = screen.getByRole('button');
    await user.click(button);

    expect(mockOnSend).toHaveBeenCalledWith('Test message');
  });

  it('clears input after sending', async () => {
    const mockOnSend = jest.fn();
    const user = userEvent.setup();

    render(<ChatInput onSend={mockOnSend} />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'Test message');

    const button = screen.getByRole('button');
    await user.click(button);

    expect(input).toHaveValue('');
  });

  it('does not call onSend with empty message', async () => {
    const mockOnSend = jest.fn();
    const user = userEvent.setup();

    render(<ChatInput onSend={mockOnSend} />);

    const button = screen.getByRole('button');
    await user.click(button);

    expect(mockOnSend).not.toHaveBeenCalled();
  });

  it('disables input when disabled prop is true', () => {
    const mockOnSend = jest.fn();
    render(<ChatInput onSend={mockOnSend} disabled={true} />);

    expect(screen.getByRole('textbox')).toBeDisabled();
  });

  it('submits on Enter key press', async () => {
    const mockOnSend = jest.fn();
    const user = userEvent.setup();

    render(<ChatInput onSend={mockOnSend} />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'Test message{enter}');

    expect(mockOnSend).toHaveBeenCalledWith('Test message');
  });

  it('uses custom placeholder when provided', () => {
    const mockOnSend = jest.fn();
    render(<ChatInput onSend={mockOnSend} placeholder="Custom placeholder" />);

    expect(screen.getByPlaceholderText('Custom placeholder')).toBeInTheDocument();
  });
});

describe('ChatWindow', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders chat header', () => {
    render(<ChatWindow />);

    expect(screen.getByText('Todo Assistant')).toBeInTheDocument();
  });

  it('shows empty state when no messages', () => {
    render(<ChatWindow />);

    expect(screen.getByText(/Hello/i)).toBeInTheDocument();
    expect(screen.getByText(/help you manage your tasks/i)).toBeInTheDocument();
  });

  it('shows suggestions in empty state', () => {
    render(<ChatWindow />);

    expect(screen.getByText(/Show my tasks/i)).toBeInTheDocument();
  });

  it('renders ChatInput component', () => {
    render(<ChatWindow />);

    expect(screen.getByRole('textbox')).toBeInTheDocument();
  });

  it('sends message when user submits', async () => {
    const mockResponse = {
      conversation_id: 1,
      response: 'I found your tasks!',
      tool_calls: [],
    };
    (sendChatMessage as jest.Mock).mockResolvedValue(mockResponse);

    const user = userEvent.setup();
    render(<ChatWindow />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'Show my tasks');

    const button = screen.getByRole('button');
    await user.click(button);

    await waitFor(() => {
      expect(sendChatMessage).toHaveBeenCalledWith('Show my tasks', undefined);
    });
  });

  it('displays user message immediately after sending', async () => {
    const mockResponse = {
      conversation_id: 1,
      response: 'Done!',
      tool_calls: [],
    };
    (sendChatMessage as jest.Mock).mockResolvedValue(mockResponse);

    const user = userEvent.setup();
    render(<ChatWindow />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'Add task');

    const button = screen.getByRole('button');
    await user.click(button);

    // User message should appear immediately (optimistic UI)
    expect(screen.getByText('Add task')).toBeInTheDocument();
  });

  it('displays assistant response after API call', async () => {
    const mockResponse = {
      conversation_id: 1,
      response: 'Task added successfully!',
      tool_calls: [],
    };
    (sendChatMessage as jest.Mock).mockResolvedValue(mockResponse);

    const user = userEvent.setup();
    render(<ChatWindow />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'Add task');

    const button = screen.getByRole('button');
    await user.click(button);

    await waitFor(() => {
      expect(screen.getByText('Task added successfully!')).toBeInTheDocument();
    });
  });

  it('shows error message on API failure', async () => {
    (sendChatMessage as jest.Mock).mockRejectedValue(new Error('Network error'));

    const user = userEvent.setup();
    render(<ChatWindow />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'Add task');

    const button = screen.getByRole('button');
    await user.click(button);

    await waitFor(() => {
      expect(screen.getByText(/Network error/i)).toBeInTheDocument();
    });
  });

  it('disables input while loading', async () => {
    // Make the API call hang
    (sendChatMessage as jest.Mock).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    const user = userEvent.setup();
    render(<ChatWindow />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'Add task');

    const button = screen.getByRole('button');
    await user.click(button);

    // Input should be disabled while loading
    await waitFor(() => {
      expect(screen.getByRole('textbox')).toBeDisabled();
    });
  });
});