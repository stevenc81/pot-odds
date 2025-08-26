// Community cards selection section

import { useCallback } from 'react'
import clsx from 'clsx'
import { useCardStore } from '@/store/cardStore'
import { CardGrid } from './CardGrid'
import type { Card as CardType } from '@/types'

interface CommunityCardsSectionProps {
  className?: string
}

export function CommunityCardsSection({ className }: CommunityCardsSectionProps) {
  const holeCards = useCardStore(state => state.holeCards)
  const communityCards = useCardStore(state => state.communityCards)
  const selectCommunityCard = useCardStore(state => state.selectCommunityCard)
  const deselectCommunityCard = useCardStore(state => state.deselectCommunityCard)
  const disabledCards = holeCards // Can't select cards that are already hole cards
  
  const handleCardToggle = useCallback((card: CardType) => {
    if (communityCards.includes(card)) {
      deselectCommunityCard(card)
    } else if (communityCards.length < 5) {
      selectCommunityCard(card)
    }
  }, [communityCards, selectCommunityCard, deselectCommunityCard])
  
  
  // Get the current board stage name
  const getBoardStageName = (count: number) => {
    if (count === 0) return 'Pre-flop'
    if (count === 3) return 'Flop'
    if (count === 4) return 'Turn'
    if (count === 5) return 'River'
    return `${count} cards`
  }
  
  return (
    <div className={clsx('space-y-4', className)}>
      {/* Header with selection status */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Community Cards
          </h2>
        </div>
        
        {/* Board stage indicator */}
        <div className={clsx(
          'px-3 py-1 rounded-full text-xs font-medium',
          communityCards.length === 0
            ? 'bg-blue-100 text-blue-700 border border-blue-200 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800'
            : 'bg-primary-100 text-primary-700 border border-primary-200 dark:bg-primary-900/30 dark:text-primary-300 dark:border-primary-800'
        )}>
          {getBoardStageName(communityCards.length)}
        </div>
      </div>
      
      
      {/* Card selection grid */}
      <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
        <CardGrid
          selectedCards={communityCards}
          onCardToggle={handleCardToggle}
          disabledCards={disabledCards}
          cardSize="sm"
        />
      </div>
      
    </div>
  )
}