// Unified display for all selected cards (hole cards + community cards)

import clsx from 'clsx'
import { Card } from '@/components/ui/Card'
import { useCardStore } from '@/store/cardStore'
import type { Card as CardType } from '@/types'

interface UnifiedSelectedCardsProps {
  className?: string
}

export function UnifiedSelectedCards({ className }: UnifiedSelectedCardsProps) {
  const holeCards = useCardStore(state => state.holeCards)
  const communityCards = useCardStore(state => state.communityCards)
  const deselectHoleCard = useCardStore(state => state.deselectHoleCard)
  const deselectCommunityCard = useCardStore(state => state.deselectCommunityCard)
  
  const hasAnyCards = holeCards.length > 0 || communityCards.length > 0
  
  // Create hole card slots (always show 2 slots)
  const holeSlots = Array.from({ length: 2 }, (_, index) => ({
    id: `hole-${index}`,
    card: holeCards[index] || null,
    type: 'hole' as const,
  }))
  
  // Create community card slots (always show 5 slots)
  const communitySlots = Array.from({ length: 5 }, (_, index) => ({
    id: `community-${index}`,
    card: communityCards[index] || null,
    type: 'community' as const,
  }))
  
  const handleCardDeselect = (card: CardType, type: 'hole' | 'community') => {
    if (type === 'hole') {
      deselectHoleCard(card)
    } else {
      deselectCommunityCard(card)
    }
  }
  
  // Get board stage name for community cards
  const getBoardStageName = (count: number) => {
    if (count === 0) return 'Pre-flop'
    if (count === 3) return 'Flop'
    if (count === 4) return 'Turn'
    if (count === 5) return 'River'
    return `${count} cards`
  }
  
  if (!hasAnyCards) {
    return (
      <div className={clsx(
        'bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6',
        className
      )}>
          <div className="text-center py-8">
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
                    strokeWidth={1.5} 
                    d="M4 7v10c0 2.21 3.79 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.79 4 8 4s8-1.79 8-4M4 7c0-2.21 3.79-4 8-4s8 1.79 8 4" 
                  />
                </svg>
              </div>
              <p className="text-sm">No cards selected yet</p>
            </div>
          </div>
      </div>
    )
  }
  
  return (
    <div className={clsx(
      'bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6 space-y-6',
      className
    )}>
        {/* Hole Cards Section */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Hole Cards
            </h4>
            <div className={clsx(
              'px-2 py-1 rounded text-xs font-medium',
              holeCards.length === 2
                ? 'bg-success/10 text-success'
                : holeCards.length > 0
                ? 'bg-warning/10 text-warning'
                : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
            )}>
              {holeCards.length === 2 ? 'Complete' : holeCards.length === 1 ? '1 more' : 'Select 2'}
            </div>
          </div>
          
          <div className="flex gap-2">
            {holeSlots.map(slot => (
              <div key={slot.id} className="relative">
                {slot.card ? (
                  <Card
                    card={slot.card}
                    isSelected={true}
                    size="md"
                    onClick={() => handleCardDeselect(slot.card!, slot.type)}
                    className="relative"
                  />
                ) : (
                  <div className="w-16 h-20 rounded-card border-2 border-dashed border-gray-300 dark:border-gray-600 flex items-center justify-center bg-gray-100 dark:bg-gray-700/50">
                    <span className="text-xs text-gray-400 dark:text-gray-500">
                      {slot.id.split('-')[1] === '0' ? 'H1' : 'H2'}
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
        
        {/* Community Cards Section */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Community Cards
            </h4>
            <div className={clsx(
              'px-2 py-1 rounded text-xs font-medium',
              communityCards.length === 0
                ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                : 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
            )}>
              {getBoardStageName(communityCards.length)}
            </div>
          </div>
          
          <div className="flex gap-2">
            {communitySlots.map(slot => (
              <div key={slot.id} className="relative">
                {slot.card ? (
                  <Card
                    card={slot.card}
                    isSelected={true}
                    size="md"
                    onClick={() => handleCardDeselect(slot.card!, slot.type)}
                    className="relative"
                  />
                ) : (
                  <div className="w-16 h-20 rounded-card border-2 border-dashed border-gray-300 dark:border-gray-600 flex items-center justify-center bg-gray-100 dark:bg-gray-700/50">
                    <span className="text-xs text-gray-400 dark:text-gray-500">
                      {slot.id.split('-')[1] === '0' ? 'F1' : 
                       slot.id.split('-')[1] === '1' ? 'F2' : 
                       slot.id.split('-')[1] === '2' ? 'F3' : 
                       slot.id.split('-')[1] === '3' ? 'T' : 'R'}
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
    </div>
  )
}