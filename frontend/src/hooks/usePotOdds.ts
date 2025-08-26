// Custom hook for pot odds calculation with debouncing

import { useQuery } from '@tanstack/react-query'
import { useEffect, useRef } from 'react'
import type { Card, CalculateRequest, CalculationResponse } from '@/types'
import { calculatePotOdds, ApiErrorClass, formatApiError } from '@/utils/api'
import { useCardStore } from '@/store/cardStore'
import { useDebounce } from './useDebounce'

interface UsePotOddsOptions {
  enabled?: boolean
  debounceMs?: number
}

/**
 * Custom hook for calculating pot odds with debouncing and state management
 */
export function usePotOdds(
  holeCards: Card[],
  communityCards: Card[],
  options: UsePotOddsOptions = {}
) {
  const { enabled = true, debounceMs = 150 } = options
  
  // Debounce the card selections to avoid excessive API calls
  const debouncedHoleCards = useDebounce(holeCards, debounceMs)
  const debouncedCommunityCards = useDebounce(communityCards, debounceMs)
  
  // Store actions
  const setCalculating = useCardStore(state => state.setCalculating)
  const setResults = useCardStore(state => state.setResults)
  const setError = useCardStore(state => state.setError)
  
  // Track the current request to cancel if needed
  const abortControllerRef = useRef<AbortController | null>(null)
  
  // Determine if we should make the API call - require flop (3+ community cards) for pot odds
  const shouldCalculate = enabled && 
    debouncedHoleCards.length === 2 && 
    debouncedCommunityCards.length >= 3 &&
    debouncedCommunityCards.length <= 5
  
  // Create the request object
  const request: CalculateRequest | null = shouldCalculate
    ? {
        hole_cards: debouncedHoleCards as [Card, Card],
        community_cards: debouncedCommunityCards,
      }
    : null
  
  // Create a stable query key
  const queryKey = request 
    ? ['potOdds', request.hole_cards, request.community_cards] as const
    : null
  
  const query = useQuery<CalculationResponse>({
    queryKey: queryKey || [],
    queryFn: async ({ signal }) => {
      if (!request) {
        throw new Error('No valid request')
      }
      
      // Cancel previous request if it exists
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
      
      // Create new abort controller
      abortControllerRef.current = new AbortController()
      
      try {
        const result = await calculatePotOdds(request, signal)
        return result
      } finally {
        abortControllerRef.current = null
      }
    },
    enabled: !!request && !!queryKey,
    retry: (failureCount, error) => {
      // Don't retry on validation errors (4xx status codes)
      if (error instanceof ApiErrorClass && error.status >= 400 && error.status < 500) {
        return false
      }
      return failureCount < 2
    },
    retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
  })
  
  // Update store state based on query state
  useEffect(() => {
    if (query.isLoading) {
      setCalculating(true)
      setError(null)
    } else if (query.data) {
      setResults(query.data)
    } else if (query.error) {
      let errorMessage = 'An unexpected error occurred'
      
      if (query.error instanceof ApiErrorClass) {
        errorMessage = formatApiError(query.error.apiError)
      } else if (query.error instanceof Error) {
        errorMessage = query.error.message
      }
      
      setError(errorMessage)
    }
  }, [query.isLoading, query.data, query.error, setCalculating, setResults, setError])
  
  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])
  
  return {
    data: query.data,
    isLoading: query.isLoading,
    error: query.error,
    isError: query.isError,
    refetch: query.refetch,
    cancel: () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    },
  }
}

/**
 * Hook to automatically calculate pot odds when cards change
 */
export function useAutoPotOdds(options: UsePotOddsOptions = {}) {
  const holeCards = useCardStore(state => state.holeCards)
  const communityCards = useCardStore(state => state.communityCards)
  const canCalculatePotOdds = useCardStore(state => state.canCalculatePotOdds())
  
  return usePotOdds(holeCards, communityCards, {
    enabled: canCalculatePotOdds && options.enabled !== false,
    debounceMs: options.debounceMs,
  })
}