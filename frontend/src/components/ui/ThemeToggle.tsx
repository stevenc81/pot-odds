// Theme toggle component with smooth animation

import { useTheme } from '@/hooks/useTheme'
import clsx from 'clsx'

export function ThemeToggle() {
  const { theme, toggleTheme, isDark } = useTheme()
  
  return (
    <button
      onClick={toggleTheme}
      className={clsx(
        'relative inline-flex items-center justify-center w-12 h-6 rounded-full transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
        'bg-gray-200 dark:bg-gray-700',
        'dark:focus:ring-offset-gray-900'
      )}
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} theme`}
      role="switch"
      aria-checked={isDark}
    >
      {/* Track */}
      <span
        className={clsx(
          'absolute left-1 inline-block w-4 h-4 rounded-full transition-transform duration-200 ease-in-out',
          'bg-white dark:bg-gray-900',
          'shadow-lg',
          isDark ? 'translate-x-6' : 'translate-x-0'
        )}
      />
      
      {/* Sun icon */}
      <svg
        className={clsx(
          'absolute left-1.5 w-3 h-3 transition-opacity duration-200',
          isDark ? 'opacity-0' : 'opacity-100',
          'text-yellow-500'
        )}
        fill="currentColor"
        viewBox="0 0 20 20"
        aria-hidden="true"
      >
        <path
          fillRule="evenodd"
          d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
          clipRule="evenodd"
        />
      </svg>
      
      {/* Moon icon */}
      <svg
        className={clsx(
          'absolute right-1.5 w-3 h-3 transition-opacity duration-200',
          isDark ? 'opacity-100' : 'opacity-0',
          'text-blue-400'
        )}
        fill="currentColor"
        viewBox="0 0 20 20"
        aria-hidden="true"
      >
        <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
      </svg>
      
      <span className="sr-only">
        Current theme: {theme}. Click to switch to {isDark ? 'light' : 'dark'} theme.
      </span>
    </button>
  )
}