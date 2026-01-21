import { Task } from '@/types';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number, currentStatus: boolean) => void;
  onDelete: (id: number) => void;
  onEdit?: (task: Task) => void;
}

export default function TaskCard({ task, onToggleComplete, onDelete, onEdit }: TaskCardProps) {
  return (
    <div className="bg-surface border border-border rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow flex items-center gap-4 group">
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggleComplete(task.id, task.completed)}
        className="w-6 h-6 border-2 border-border rounded-md checked:bg-success checked:border-success focus:ring-0 focus:ring-offset-0 cursor-pointer"
      />

      <div className="flex-grow">
        <h3 className={`text-base font-medium ${task.completed ? 'text-text-muted line-through' : 'text-text-primary'}`}>
          {task.title}
        </h3>
        {task.description && (
          <p className={`text-sm mt-1 ${task.completed ? 'text-text-muted line-through' : 'text-text-secondary'}`}>
            {task.description}
          </p>
        )}
        {task.created_at && (
          <p className="text-xs text-text-muted mt-2">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        )}
      </div>

      <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
        {onEdit && (
          <button
            onClick={() => onEdit(task)}
            className="w-9 h-9 rounded-lg hover:bg-background flex items-center justify-center text-text-secondary hover:text-text-primary transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </button>
        )}
        <button
          onClick={() => onDelete(task.id)}
          className="w-9 h-9 rounded-lg hover:bg-error-light flex items-center justify-center text-text-secondary hover:text-error transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  );
}