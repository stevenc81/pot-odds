// Grid of all available cards for selection

import { useMemo } from 'react'
import clsx from 'clsx'
import { Card } from '@/components/ui/Card'
import type { Card as CardType } from '@/types'
import { getAllCards } from '@/utils/cards'

interface CardGridProps {
  selectedCards: CardType[]
  onCardToggle: (card: CardType) => void
  disabledCards?: CardType[]
  className?: string
  cardSize?: 'sm' | 'md' | 'lg'
}

export function CardGrid({
  selectedCards,
  onCardToggle,
  disabledCards = [],
  className,
  cardSize = 'sm'
}: CardGridProps) {
  const allCards = useMemo(() => getAllCards(), [])
  const selectedCardSet = useMemo(() => new Set(selectedCards), [selectedCards])
  const disabledCardSet = useMemo(() => new Set(disabledCards), [disabledCards])
  
  // Group cards by suit for better visual organization
  const cardsBySuit = useMemo(() => {
    const suits = ['s', 'h', 'd', 'c'] as const
    return suits.map(suit => ({
      suit,
      cards: allCards.filter(card => card.endsWith(suit))
    }))
  }, [allCards])
  
  const handleCardClick = (card: CardType) => {
    if (disabledCardSet.has(card)) return
    onCardToggle(card)
  }
  
  return (
    <div className={clsx('space-y-4', className)}>
      {cardsBySuit.map(({ suit, cards }) => (
        <div key={suit} className="space-y-2">
          {/* Suit header */}
          <div className="text-xs font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wide">
            {suit === 's' && '♠'}
            {suit === 'h' && '♥'}
            {suit === 'd' && '♦'}
            {suit === 'c' && '♣'}
          </div>
          
          {/* Cards in this suit */}
          <div className="grid grid-cols-13 gap-1 sm:gap-2">
            {cards.map(card => (
              <Card
                key={card}
                card={card}
                isSelected={selectedCardSet.has(card)}
                isDisabled={disabledCardSet.has(card)}
                size={cardSize}
                onClick={() => handleCardClick(card)}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

