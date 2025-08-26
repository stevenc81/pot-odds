// Individual card component with visual representation and selection

import { type ButtonHTMLAttributes, forwardRef } from 'react'
import clsx from 'clsx'
import type { Card as CardType } from '@/types'
import { getCardDisplay, getCardColorClasses } from '@/utils/cards'

interface CardProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'type'> {
  card: CardType
  isSelected?: boolean
  isDisabled?: boolean
  size?: 'sm' | 'md' | 'lg'
}

export const Card = forwardRef<HTMLButtonElement, CardProps>(
  ({ card, isSelected = false, isDisabled = false, size = 'md', className, ...props }, ref) => {
    const cardDisplay = getCardDisplay(card)
    const colorClasses = getCardColorClasses(card)
    
    const sizeClasses = {
      sm: 'w-12 h-16 text-sm',
      md: 'w-16 h-20 text-base',
      lg: 'w-20 h-26 text-lg',
    }
    
    return (
      <button
        ref={ref}
        type="button"
        disabled={isDisabled}
        className={clsx(
          // Base styles
          'relative rounded-card bg-card-light dark:bg-card-dark border-2 font-mono font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900',
          
          // Size
          sizeClasses[size],
          
          // Interactive states (only apply hover scale when not selected to avoid conflicts)
          !isSelected && 'hover:scale-105',
          'active:scale-95',
          
          // Selection states
          isSelected
            ? 'border-card-selected dark:border-card-selected-dark bg-card-selected-bg dark:bg-card-selected-bg-dark shadow-card-selected dark:shadow-card-selected-dark transform scale-105 ring-2 ring-card-selected dark:ring-card-selected-dark ring-offset-2 dark:ring-offset-gray-900'
            : 'border-gray-300 dark:border-gray-600 shadow-card dark:shadow-card-dark hover:border-gray-400 dark:hover:border-gray-500 hover:shadow-lg dark:hover:shadow-xl',
          
          // Disabled states
          isDisabled && 'opacity-50 cursor-not-allowed hover:scale-100 active:scale-100',
          
          // Card text color
          colorClasses,
          
          className
        )}
        aria-pressed={isSelected}
        aria-label={`Card ${cardDisplay}${isSelected ? ' (selected)' : ''}`}
        {...props}
      >
        <div className={clsx(
          "flex flex-col items-center justify-center h-full transition-all duration-200",
          isSelected && "pt-5" // Add padding when selected to account for overlay
        )}>
          <span className={clsx(
            "leading-none font-bold transition-all duration-200",
            // Enhanced contrast for selected state - subtle text shadow for better readability
            isSelected && "drop-shadow-sm",
            // Ensure text remains readable on both light and dark backgrounds
            "relative z-10",
            // Add text shadow for better contrast in dark mode
            "text-shadow-card-light dark:text-shadow-card-dark"
          )}>
            {cardDisplay}
          </span>
        </div>
        
        {/* Selection indicator */}
        {isSelected && (
          <>
            {/* Corner indicator */}
            <div className="absolute -top-1 -right-1 w-5 h-5 bg-card-selected dark:bg-card-selected-dark rounded-full border-2 border-white dark:border-gray-900 animate-scale-in flex items-center justify-center">
              <svg 
                className="w-3 h-3 text-white" 
                fill="currentColor" 
                viewBox="0 0 20 20"
              >
                <path 
                  fillRule="evenodd" 
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" 
                  clipRule="evenodd" 
                />
              </svg>
            </div>
            {/* Selected label overlay */}
            <div className="absolute inset-x-0 top-0 bg-card-selected dark:bg-card-selected-dark text-white text-xs font-bold py-1 text-center rounded-t-card opacity-90">
              SELECTED
            </div>
          </>
        )}
      </button>
    )
  }
)

Card.displayName = 'Card'