// Types for card representation and selection

import type { Card, Rank, Suit } from './api'

/** Parsed card object */
export interface ParsedCard {
  rank: Rank
  suit: Suit
  notation: Card
  color: 'red' | 'black'
}


/** Card validation result */
export interface CardValidation {
  isValid: boolean
  errors: string[]
}

/** Theme preference */
export type Theme = 'light' | 'dark'



/** Suit symbols for display */
export const SUIT_SYMBOLS = {
  s: '♠',
  h: '♥',
  d: '♦',
  c: '♣',
} as const

/** Rank display names */
export const RANK_NAMES = {
  '2': '2',
  '3': '3', 
  '4': '4',
  '5': '5',
  '6': '6',
  '7': '7',
  '8': '8',
  '9': '9',
  'T': '10',
  'J': 'J',
  'Q': 'Q',
  'K': 'K',
  'A': 'A',
} as const