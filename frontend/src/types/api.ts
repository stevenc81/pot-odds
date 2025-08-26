// TypeScript types for the Pot Odds Calculator API

/** Card notation type (e.g., 'As', 'Kh', '7d') */
export type Card = string

/** Valid card ranks */
export type Rank = '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'T' | 'J' | 'Q' | 'K' | 'A'

/** Valid card suits */
export type Suit = 's' | 'h' | 'd' | 'c'

/** Draw types that can be completed - matches backend API specification */
export type DrawType = 
  | 'flush'
  | 'straight'
  | 'pair'
  | 'two_pair'
  | 'three_of_a_kind'
  | 'full_house'
  | 'four_of_a_kind'
  | 'straight_flush'
  | 'royal_flush'

/** Request model for pot odds calculation */
export interface CalculateRequest {
  hole_cards: [Card, Card] // Exactly 2 hole cards
  community_cards: Card[] // 0-5 community cards
}

/** Out card with its draw type */
export interface OutCard {
  card: Card
  draw_type: string // Allow any string to handle backend variations
}

/** Response model for pot odds calculation */
export interface CalculationResponse {
  pot_odds_ratio: string // Format: "X.X:1"
  outs: OutCard[]
}


/** Error response from API */
export interface ApiError {
  detail: string | Array<{
    loc: string[]
    msg: string
    type: string
  }>
}

/** API endpoints configuration */
export const API_ENDPOINTS = {
  // Use environment variable if available, otherwise default to localhost
  // In production with nginx, we can use relative URLs since nginx proxies /api
  BASE_URL: import.meta.env.VITE_API_URL || 
            (import.meta.env.PROD ? '' : 'http://localhost:8000'),
  CALCULATE: '/api/calculate',
  HEALTH: '/health',
} as const