import React from 'react';
import { Task } from '@/types';
import { Card, CardContent } from '../ui/Card';
import Button from '../ui/Button';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number, currentStatus: boolean) => void;
  onDelete: (id: number) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggleComplete, onDelete }) => {
  return (
    <Card className={`${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      <CardContent className="p-4">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-1 ${task.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
                {task.description}
              </p>
            )}
            <div className="mt-2 text-xs text-gray-500">
              Created: {new Date(task.created_at).toLocaleDateString()}
            </div>
          </div>
          <div className="flex space-x-2 ml-4">
            <Button
              variant={task.completed ? 'secondary' : 'primary'}
              size="sm"
              onClick={() => onToggleComplete(task.id, task.completed)}
            >
              {task.completed ? 'Undo' : 'Complete'}
            </Button>
            <Button
              variant="danger"
              size="sm"
              onClick={() => onDelete(task.id)}
            >
              Delete
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default TaskCard;