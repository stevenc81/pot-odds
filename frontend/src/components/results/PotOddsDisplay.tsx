// Display for pot odds ratio with visual emphasis

import clsx from 'clsx'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { useCardStore, selectResults, selectUIState, selectCanCalculatePotOdds, selectCommunityCards } from '@/store/cardStore'

interface PotOddsDisplayProps {
  className?: string
}

export function PotOddsDisplay({ className }: PotOddsDisplayProps) {
  const { potOddsRatio } = useCardStore(selectResults)
  const { isCalculating, error } = useCardStore(selectUIState)
  const canCalculate = useCardStore(state => state.canCalculate())
  const canCalculatePotOdds = useCardStore(selectCanCalculatePotOdds)
  const communityCards = useCardStore(selectCommunityCards)
  
  // Show message when hole cards are available but flop is not present
  if (canCalculate && !canCalculatePotOdds && !error) {
    const neededCards = 3 - communityCards.length
    return (
      <div className={clsx('text-center py-8', className)}>
        <div className="text-gray-400 dark:text-gray-500">
          <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
            <svg 
              className="w-8 h-8" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" 
              />
            </svg>
          </div>
          <h3 className="text-lg font-medium mb-2">Pot odds available after the flop</h3>
          <p className="text-sm">
            Select {neededCards} more community card{neededCards > 1 ? 's' : ''} to see pot odds calculations
          </p>
        </div>
      </div>
    )
  }
  
  if (!canCalculate && !error) {
    return (
      <div className={clsx('text-center py-8', className)}>
        <div className="text-gray-400 dark:text-gray-500">
          <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
            <svg 
              className="w-8 h-8" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" 
              />
            </svg>
          </div>
        </div>
      </div>
    )
  }
  
  if (error) {
    return (
      <div className={clsx('text-center py-8', className)}>
        <div className="text-error">
          <div className="w-16 h-16 mx-auto mb-4 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center">
            <svg 
              className="w-8 h-8" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" 
              />
            </svg>
          </div>
          <p className="text-sm font-medium mb-2">Calculation Error</p>
        </div>
      </div>
    )
  }
  
  if (isCalculating) {
    return (
      <div className={clsx('text-center py-8', className)}>
        <div className="space-y-4">
          <LoadingSpinner size="lg" className="mx-auto text-primary-600" />
        </div>
      </div>
    )
  }
  
  if (!potOddsRatio) {
    return null
  }
  
  return (
    <div className={clsx('text-center py-8', className)}>
      <div className="space-y-4">
        <div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
            Pot Odds
          </h3>
          <div className="text-5xl md:text-6xl font-bold text-primary-600 dark:text-primary-400 font-mono animate-scale-in">
            {potOddsRatio}
          </div>
        </div>
        
      </div>
    </div>
  )
}