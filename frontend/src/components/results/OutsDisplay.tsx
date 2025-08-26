// Display for outs analysis with grouping by draw type

import { useMemo } from 'react'
import clsx from 'clsx'
import { Card } from '@/components/ui/Card'
import { useCardStore, selectResults } from '@/store/cardStore'
import type { OutCard, DrawType } from '@/types'

interface OutsDisplayProps {
  className?: string
}

// Draw type display configuration - matches backend API specification
const DRAW_TYPE_CONFIG: Record<DrawType, { name: string; color: string; priority: number }> = {
  royal_flush: { name: 'Royal Flush', color: 'text-purple-600 dark:text-purple-400', priority: 1 },
  straight_flush: { name: 'Straight Flush', color: 'text-purple-600 dark:text-purple-400', priority: 2 },
  four_of_a_kind: { name: 'Four of a Kind', color: 'text-red-600 dark:text-red-400', priority: 3 },
  full_house: { name: 'Full House', color: 'text-red-600 dark:text-red-400', priority: 4 },
  flush: { name: 'Flush', color: 'text-blue-600 dark:text-blue-400', priority: 5 },
  straight: { name: 'Straight', color: 'text-green-600 dark:text-green-400', priority: 6 },
  three_of_a_kind: { name: 'Three of a Kind', color: 'text-yellow-600 dark:text-yellow-400', priority: 7 },
  two_pair: { name: 'Two Pair', color: 'text-orange-600 dark:text-orange-400', priority: 8 },
  pair: { name: 'Pair', color: 'text-gray-600 dark:text-gray-400', priority: 9 },
}

export function OutsDisplay({ className }: OutsDisplayProps) {
  const { outs } = useCardStore(selectResults)
  const canCalculate = useCardStore(state => state.canCalculate())
  
  // Group and sort outs by draw type
  const groupedOuts = useMemo(() => {
    if (!outs || outs.length === 0) return []
    
    const groups = outs.reduce((acc, out) => {
      const drawType = out.draw_type
      if (!acc[drawType]) {
        acc[drawType] = []
      }
      acc[drawType].push(out)
      return acc
    }, {} as Record<string, OutCard[]>)
    
    // Sort groups by priority and convert to array
    return Object.entries(groups)
      .map(([drawType, cards]) => ({
        drawType: drawType,
        cards: cards.sort((a, b) => a.card.localeCompare(b.card)),
        config: DRAW_TYPE_CONFIG[drawType as DrawType] || { 
          name: drawType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()), 
          color: 'text-gray-600 dark:text-gray-400', 
          priority: 10 
        }
      }))
      .sort((a, b) => a.config.priority - b.config.priority)
  }, [outs])
  
  if (!canCalculate) {
    return null
  }
  
  if (!outs || outs.length === 0) {
    return (
      <div className={clsx('text-center py-6', className)}>
        <div className="text-gray-400 dark:text-gray-500">
          <div className="w-12 h-12 mx-auto mb-3 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
            <svg 
              className="w-6 h-6" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M20 12H4" 
              />
            </svg>
          </div>
          <p className="text-sm">No outs available</p>
        </div>
      </div>
    )
  }
  
  
  return (
    <div className={clsx('space-y-6', className)}>
      {/* Header */}
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-1">
          Your Outs
        </h3>
      </div>
      
      {/* Grouped outs */}
      <div className="space-y-4">
        {groupedOuts.map(({ drawType, cards, config }) => (
          <div key={drawType} className="space-y-3">
            {/* Draw type header */}
            <div className="flex items-center space-x-2">
              <h4 className={clsx('font-medium', config.color)}>
                {config.name}
              </h4>
              <span className="text-xs text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full">
                {cards.length} card{cards.length !== 1 ? 's' : ''}
              </span>
            </div>
            
            {/* Cards for this draw type */}
            <div className="flex flex-wrap gap-2">
              {cards.map(out => (
                <Card
                  key={out.card}
                  card={out.card}
                  size="sm"
                  className="cursor-default hover:scale-100 active:scale-100"
                />
              ))}
            </div>
          </div>
        ))}
      </div>
      
    </div>
  )
}