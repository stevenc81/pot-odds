// Zustand store for card selection state

import { create } from 'zustand'
import { devtools, subscribeWithSelector } from 'zustand/middleware'
import type { Card, CalculationResponse, OutCard } from '@/types'
import { validateCardSelection, canCalculate, canCalculatePotOdds } from '@/utils/cards'

interface CardState {
  // Card selection state
  holeCards: Card[]
  communityCards: Card[]
  
  // Calculation results
  potOddsRatio: string | null
  outs: OutCard[]
  
  // UI state
  isCalculating: boolean
  error: string | null
  
  // Actions
  selectHoleCard: (card: Card) => void
  deselectHoleCard: (card: Card) => void
  selectCommunityCard: (card: Card) => void
  deselectCommunityCard: (card: Card) => void
  resetCards: () => void
  setCalculating: (isCalculating: boolean) => void
  setResults: (results: CalculationResponse) => void
  setError: (error: string | null) => void
  clearResults: () => void
  
  // Computed values
  getAllSelectedCards: () => Card[]
  getValidationErrors: () => string[]
  canCalculate: () => boolean
  canCalculatePotOdds: () => boolean
  isCardSelected: (card: Card) => boolean
}

export const useCardStore = create<CardState>()(
  devtools(
    subscribeWithSelector(
      (set, get) => ({
        // Initial state
        holeCards: [],
        communityCards: [],
        potOddsRatio: null,
        outs: [],
        isCalculating: false,
        error: null,
        
        // Hole card actions
        selectHoleCard: (card: Card) => {
          const { holeCards, communityCards } = get()
          
          // Check if card is already selected somewhere
          if (holeCards.includes(card) || communityCards.includes(card)) {
            return
          }
          
          // Check if we can add more hole cards
          if (holeCards.length >= 2) {
            return
          }
          
          set(
            (state) => ({
              holeCards: [...state.holeCards, card],
              error: null, // Clear error when making changes
            }),
            false,
            'selectHoleCard'
          )
        },
        
        deselectHoleCard: (card: Card) => {
          set(
            (state) => ({
              holeCards: state.holeCards.filter(c => c !== card),
              error: null,
            }),
            false,
            'deselectHoleCard'
          )
        },
        
        // Community card actions
        selectCommunityCard: (card: Card) => {
          const { holeCards, communityCards } = get()
          
          // Check if card is already selected somewhere
          if (holeCards.includes(card) || communityCards.includes(card)) {
            return
          }
          
          // Check if we can add more community cards
          if (communityCards.length >= 5) {
            return
          }
          
          set(
            (state) => ({
              communityCards: [...state.communityCards, card],
              error: null,
            }),
            false,
            'selectCommunityCard'
          )
        },
        
        deselectCommunityCard: (card: Card) => {
          set(
            (state) => ({
              communityCards: state.communityCards.filter(c => c !== card),
              error: null,
            }),
            false,
            'deselectCommunityCard'
          )
        },
        
        // Reset all cards
        resetCards: () => {
          set(
            () => ({
              holeCards: [],
              communityCards: [],
              potOddsRatio: null,
              outs: [],
              isCalculating: false,
              error: null,
            }),
            false,
            'resetCards'
          )
        },
        
        // Results actions
        setCalculating: (isCalculating: boolean) => {
          set({ isCalculating }, false, 'setCalculating')
        },
        
        setResults: (results: CalculationResponse) => {
          set(
            {
              potOddsRatio: results.pot_odds_ratio,
              outs: results.outs,
              isCalculating: false,
              error: null,
            },
            false,
            'setResults'
          )
        },
        
        setError: (error: string | null) => {
          set(
            {
              error,
              isCalculating: false,
              potOddsRatio: null,
              outs: [],
            },
            false,
            'setError'
          )
        },
        
        clearResults: () => {
          set(
            {
              potOddsRatio: null,
              outs: [],
              error: null,
            },
            false,
            'clearResults'
          )
        },
        
        // Computed values
        getAllSelectedCards: () => {
          const { holeCards, communityCards } = get()
          return [...holeCards, ...communityCards]
        },
        
        getValidationErrors: () => {
          const { holeCards, communityCards } = get()
          const validation = validateCardSelection(holeCards, communityCards)
          return validation.errors
        },
        
        canCalculate: () => {
          const { holeCards, communityCards } = get()
          return canCalculate(holeCards, communityCards)
        },
        
        canCalculatePotOdds: () => {
          const { holeCards, communityCards } = get()
          return canCalculatePotOdds(holeCards, communityCards)
        },
        
        isCardSelected: (card: Card) => {
          const { holeCards, communityCards } = get()
          return holeCards.includes(card) || communityCards.includes(card)
        },
      })
    ),
    {
      name: 'card-store',
    }
  )
)

// Selectors for better performance
export const selectCommunityCards = (state: CardState) => state.communityCards
export const selectResults = (state: CardState) => ({
  potOddsRatio: state.potOddsRatio,
  outs: state.outs,
})
export const selectUIState = (state: CardState) => ({
  isCalculating: state.isCalculating,
  error: state.error,
})
export const selectCanCalculatePotOdds = (state: CardState) => state.canCalculatePotOdds()