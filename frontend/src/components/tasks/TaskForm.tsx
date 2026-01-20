import React, { useState } from 'react';
import { TaskInput } from '@/types';
import Input from '../ui/Input';
import Button from '../ui/Button';

interface TaskFormProps {
  onSubmit: (taskData: TaskInput) => void;
  onCancel?: () => void;
  initialData?: TaskInput;
  submitButtonText?: string;
}

const TaskForm: React.FC<TaskFormProps> = ({
  onSubmit,
  onCancel,
  initialData = { title: '', description: '' },
  submitButtonText = 'Add Task'
}) => {
  const [title, setTitle] = useState(initialData.title);
  const [description, setDescription] = useState(initialData.description);
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.length < 1 || title.length > 200) {
      setError('Title must be between 1 and 200 characters');
      return;
    }

    if (description && description.length > 1000) {
      setError('Description must be at most 1000 characters');
      return;
    }

    onSubmit({ title, description });
    setError('');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <Input
        label="Title*"
        type="text"
        id="title"
        name="title"
        required
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title (1-200 characters)"
        maxLength={200}
      />

      <div>
        <label htmlFor="description" className="block text-sm font-medium leading-6 text-gray-900">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Task description (optional, max 1000 characters)"
          className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
          rows={3}
          maxLength={1000}
        />
      </div>

      <div className="flex space-x-2">
        <Button type="submit">{submitButtonText}</Button>
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
};

export default TaskForm;