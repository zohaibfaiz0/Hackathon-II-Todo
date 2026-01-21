import React from 'react';
import { Task } from '@/types';
import TaskCard from './TaskCard';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (id: number, currentStatus: boolean) => void;
  onDelete: (id: number) => void;
  filter: 'all' | 'pending' | 'completed';
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onToggleComplete, onDelete, filter }) => {
  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return !task.completed
    if (filter === 'completed') return task.completed
    return true
  })

  if (filteredTasks.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        {filter === 'all' ? 'No tasks yet' :
         filter === 'pending' ? 'No pending tasks' :
         'No completed tasks'}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {filteredTasks.map(task => (
        <TaskCard
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export default TaskList;