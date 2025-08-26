// Hole cards selection section

import { useCallback } from 'react'
import clsx from 'clsx'
import { useCardStore } from '@/store/cardStore'
import { CardGrid } from './CardGrid'
import type { Card as CardType } from '@/types'

interface HoleCardsSectionProps {
  className?: string
}

export function HoleCardsSection({ className }: HoleCardsSectionProps) {
  const holeCards = useCardStore(state => state.holeCards)
  const communityCards = useCardStore(state => state.communityCards)
  const selectHoleCard = useCardStore(state => state.selectHoleCard)
  const deselectHoleCard = useCardStore(state => state.deselectHoleCard)
  const disabledCards = communityCards // Can't select cards that are already community cards
  
  const handleCardToggle = useCallback((card: CardType) => {
    if (holeCards.includes(card)) {
      deselectHoleCard(card)
    } else if (holeCards.length < 2) {
      selectHoleCard(card)
    }
  }, [holeCards, selectHoleCard, deselectHoleCard])
  
  
  return (
    <div className={clsx('space-y-4', className)}>
      {/* Header with selection status */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Hole Cards
          </h2>
        </div>
        
        {/* Selection status indicator */}
        <div className={clsx(
          'px-3 py-1 rounded-full text-xs font-medium',
          holeCards.length === 2
            ? 'bg-success/10 text-success border border-success/20'
            : holeCards.length > 0
            ? 'bg-warning/10 text-warning border border-warning/20'
            : 'bg-gray-100 text-gray-600 border border-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700'
        )}>
          {holeCards.length === 2 ? 'Complete' : holeCards.length === 1 ? 'Select 1 more' : 'Select 2 cards'}
        </div>
      </div>
      
      
      {/* Card selection grid */}
      <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
        <CardGrid
          selectedCards={holeCards}
          onCardToggle={handleCardToggle}
          disabledCards={disabledCards}
          cardSize="sm"
        />
      </div>
      
    </div>
  )
}