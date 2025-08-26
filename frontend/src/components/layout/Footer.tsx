// Application footer

import clsx from 'clsx'

interface FooterProps {
  className?: string
}

export function Footer({ className }: FooterProps) {
  return (
    <footer className={clsx(
      'border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50',
      className
    )}>
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
          <div className="text-center md:text-left">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Pot Odds Calculator
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-xs text-gray-500 dark:text-gray-500">
              v1.0.0
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}