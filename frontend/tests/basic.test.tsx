/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskCard from '../src/components/tasks/TaskCard';
import { Task } from '../src/types';

// Mock Task type for testing
const mockTask: Task = {
  id: 1,
  user_id: 'user1',
  title: 'Test Task',
  description: 'Test Description',
  completed: false,
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z',
};

// Define jest type for testing
const mockJest = jest;

describe('TaskCard Component', () => {
  it('renders task title and description', () => {
    render(<TaskCard task={mockTask} onToggleComplete={jest.fn()} onDelete={jest.fn()} />);

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('shows completed style when task is completed', () => {
    const completedTask = { ...mockTask, completed: true };
    render(<TaskCard task={completedTask} onToggleComplete={jest.fn()} onDelete={jest.fn()} />);

    const titleElement = screen.getByText('Test Task');
    expect(titleElement).toHaveClass('line-through');
  });

  it('calls onToggleComplete when complete button is clicked', () => {
    const onToggleComplete = jest.fn();
    render(<TaskCard task={mockTask} onToggleComplete={onToggleComplete} onDelete={jest.fn()} />);

    const completeButton = screen.getByText('Complete');
    completeButton.click();

    expect(onToggleComplete).toHaveBeenCalledWith(mockTask.id, mockTask.completed);
  });

  it('calls onDelete when delete button is clicked', () => {
    const onDelete = jest.fn();
    render(<TaskCard task={mockTask} onToggleComplete={jest.fn()} onDelete={onDelete} />);

    const deleteButton = screen.getByText('Delete');
    deleteButton.click();

    expect(onDelete).toHaveBeenCalledWith(mockTask.id);
  });
});

describe('Basic Component Tests', () => {
  it('has all required components created', () => {
    // This test verifies that our components exist
    expect(typeof TaskCard).toBe('function');
  });
});