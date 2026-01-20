import { Task } from '@/types';

interface EditTaskModalProps {
  isOpen: boolean;
  task: Task | null;
  onClose: () => void;
  onSave: (updatedTask: Task) => void;
  onChange: (field: keyof Task, value: any) => void;
}

export default function EditTaskModal({ isOpen, task, onClose, onSave, onChange }: EditTaskModalProps) {
  if (!isOpen || !task) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="bg-surface rounded-xl w-full max-w-md mx-4 shadow-xl transform transition-all">
        {/* Header */}
        <div className="p-5 border-b border-border flex items-center justify-between">
          <h3 className="text-lg font-semibold text-text-primary">Edit Task</h3>
          <button
            onClick={onClose}
            className="w-9 h-9 flex items-center justify-center rounded-lg hover:bg-background text-text-secondary"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Body */}
        <div className="p-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-text-primary mb-1.5">Title</label>
            <input
              type="text"
              value={task.title}
              onChange={(e) => onChange('title', e.target.value)}
              className="w-full h-11 bg-background border border-border rounded-lg px-4 text-base placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition"
              placeholder="Task title"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1.5">Description</label>
            <textarea
              value={task.description || ''}
              onChange={(e) => onChange('description', e.target.value)}
              className="w-full h-24 bg-background border border-border rounded-lg px-4 py-3 text-base placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition resize-none"
              placeholder="Task description"
            />
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-border flex justify-end gap-3">
          <button
            onClick={onClose}
            className="h-10 px-4 bg-surface text-text-primary border border-border rounded-lg text-sm font-medium hover:bg-background transition"
          >
            Cancel
          </button>
          <button
            onClick={() => onSave(task)}
            className="h-10 px-4 bg-primary text-text-inverse rounded-lg text-sm font-medium hover:bg-primary-hover transition"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}