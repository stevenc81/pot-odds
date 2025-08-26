// Utility functions for card handling

import type { Card, ParsedCard, Rank, Suit, CardValidation } from '@/types'
import { SUIT_SYMBOLS, RANK_NAMES } from '@/types/cards'

/** Parse a card notation into components */
export function parseCard(card: Card): ParsedCard {
  if (card.length !== 2) {
    throw new Error(`Invalid card notation: ${card}`)
  }
  
  const rank = card[0] as Rank
  const suit = card[1] as Suit
  
  if (!isValidRank(rank) || !isValidSuit(suit)) {
    throw new Error(`Invalid card notation: ${card}`)
  }
  
  return {
    rank,
    suit,
    notation: card,
    color: suit === 'h' || suit === 'd' ? 'red' : 'black'
  }
}

/** Check if rank is valid */
export function isValidRank(rank: string): rank is Rank {
  return ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'].includes(rank)
}

/** Check if suit is valid */
export function isValidSuit(suit: string): suit is Suit {
  return ['s', 'h', 'd', 'c'].includes(suit)
}

/** Validate card notation */
export function isValidCard(card: string): card is Card {
  try {
    parseCard(card)
    return true
  } catch {
    return false
  }
}

/** Get display text for a card */
export function getCardDisplay(card: Card): string {
  try {
    const parsed = parseCard(card)
    return `${RANK_NAMES[parsed.rank]}${SUIT_SYMBOLS[parsed.suit]}`
  } catch {
    return card
  }
}

/** Get CSS classes for card color */
export function getCardColorClasses(card: Card): string {
  try {
    const parsed = parseCard(card)
    if (parsed.color === 'red') {
      return parsed.suit === 'h' ? 'text-heart-light dark:text-heart-dark' : 'text-diamond-light dark:text-diamond-dark'
    } else {
      return parsed.suit === 's' ? 'text-spade-light dark:text-spade-dark' : 'text-club-light dark:text-club-dark'
    }
  } catch {
    return 'text-gray-600 dark:text-gray-300'
  }
}

/** Validate card selection */
export function validateCardSelection(
  holeCards: Card[],
  communityCards: Card[]
): CardValidation {
  const errors: string[] = []
  
  // Check hole cards count
  if (holeCards.length !== 2) {
    errors.push('Must select exactly 2 hole cards')
  }
  
  // Check community cards count
  if (communityCards.length > 5) {
    errors.push('Cannot select more than 5 community cards')
  }
  
  // Check for duplicates within hole cards
  if (new Set(holeCards).size !== holeCards.length) {
    errors.push('Duplicate hole cards are not allowed')
  }
  
  // Check for duplicates within community cards
  if (new Set(communityCards).size !== communityCards.length) {
    errors.push('Duplicate community cards are not allowed')
  }
  
  // Check for duplicates across hole and community cards
  const allCards = [...holeCards, ...communityCards]
  if (new Set(allCards).size !== allCards.length) {
    errors.push('The same card cannot be selected as both hole and community card')
  }
  
  // Check card notation validity
  for (const card of allCards) {
    if (!isValidCard(card)) {
      errors.push(`Invalid card notation: ${card}`)
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}


/** Check if cards can be used for calculation */
export function canCalculate(holeCards: Card[], communityCards: Card[]): boolean {
  const validation = validateCardSelection(holeCards, communityCards)
  return validation.isValid && holeCards.length === 2
}

/** Check if pot odds can be calculated (requires flop) */
export function canCalculatePotOdds(holeCards: Card[], communityCards: Card[]): boolean {
  return canCalculate(holeCards, communityCards) && communityCards.length >= 3
}


/** Get all 52 cards */
export function getAllCards(): Card[] {
  const cards: Card[] = []
  const ranks: Rank[] = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
  const suits: Suit[] = ['s', 'h', 'd', 'c']
  
  for (const suit of suits) {
    for (const rank of ranks) {
      cards.push(`${rank}${suit}` as Card)
    }
  }
  
  return cards
}


