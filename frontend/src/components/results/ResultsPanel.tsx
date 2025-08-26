// Main results panel combining pot odds and outs display

import clsx from 'clsx'
import { PotOddsDisplay } from './PotOddsDisplay'
import { OutsDisplay } from './OutsDisplay'
import { UnifiedSelectedCards } from '@/components/card-selection/UnifiedSelectedCards'
import { useCardStore, selectResults, selectUIState } from '@/store/cardStore'

interface ResultsPanelProps {
  className?: string
}

export function ResultsPanel({ className }: ResultsPanelProps) {
  const { potOddsRatio, outs } = useCardStore(selectResults)
  const { isCalculating, error } = useCardStore(selectUIState)
  const canCalculate = useCardStore(state => state.canCalculate())
  
  const hasResults = potOddsRatio && outs
  const showContent = canCalculate || error || hasResults
  
  return (
    <div className={clsx('space-y-6', className)}>
      {/* Unified Selected Cards Display */}
      <UnifiedSelectedCards />
      
      {/* Results Section */}
      <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
          {!showContent ? (
            <div className="text-center py-12">
              <div className="text-gray-400 dark:text-gray-500">
                <div className="w-20 h-20 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
                  <svg 
                    className="w-10 h-10" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={1.5} 
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" 
                    />
                  </svg>
                </div>
                <h3 className="text-lg font-medium mb-2">Ready to Calculate</h3>
              </div>
            </div>
          ) : (
            <div className="space-y-8">
              {/* Pot Odds Display */}
              <PotOddsDisplay />
              
              {/* Divider */}
              {(hasResults && !error && !isCalculating) && (
                <div className="border-t border-gray-200 dark:border-gray-700" />
              )}
              
              {/* Outs Display */}
              {(hasResults && !error && !isCalculating) && (
                <OutsDisplay />
              )}
            </div>
          )}
      </div>
    </div>
  )
}