import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input: React.FC<InputProps> = ({ label, error, className = '', ...props }) => {
  const baseClasses = 'block w-full rounded-md border-0 py-1.5 shadow-sm ring-1 ring-inset focus:ring-2 focus:ring-inset sm:text-sm sm:leading-6';

  const inputClasses = `${baseClasses} ${
    error
      ? 'text-red-900 ring-red-300 placeholder:text-red-300 focus:ring-red-500'
      : 'text-gray-900 ring-gray-300 placeholder:text-gray-400 focus:ring-blue-600'
  } ${className}`;

  return (
    <div>
      {label && (
        <label className="block text-sm font-medium leading-6 text-gray-900">
          {label}
        </label>
      )}
      <input className={inputClasses} {...props} />
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
    </div>
  );
};

export default Input;