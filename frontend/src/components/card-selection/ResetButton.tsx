// Reset button to clear all card selections

import { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { useCardStore } from '@/store/cardStore'
import clsx from 'clsx'

interface ResetButtonProps {
  className?: string
}

export function ResetButton({ className }: ResetButtonProps) {
  const resetCards = useCardStore(state => state.resetCards)
  const holeCards = useCardStore(state => state.holeCards)
  const communityCards = useCardStore(state => state.communityCards)
  const [isResetting, setIsResetting] = useState(false)
  
  const hasSelectedCards = holeCards.length > 0 || communityCards.length > 0
  
  const handleReset = async () => {
    if (!hasSelectedCards) return
    
    setIsResetting(true)
    
    // Add a small delay for visual feedback
    setTimeout(() => {
      resetCards()
      setIsResetting(false)
    }, 100)
  }
  
  return (
    <div className={clsx('flex flex-col items-center space-y-2', className)}>
      <Button
        variant="danger"
        size="lg"
        onClick={handleReset}
        disabled={!hasSelectedCards}
        isLoading={isResetting}
        className={clsx(
          'min-w-32 transition-all duration-200',
          hasSelectedCards && 'hover:scale-105 active:scale-95',
          !hasSelectedCards && 'opacity-50'
        )}
      >
        {isResetting ? 'Clearing...' : 'Reset Cards'}
      </Button>
      
    </div>
  )
}