// API utility functions

import type { CalculateRequest, CalculationResponse, ApiError } from '@/types'
import { API_ENDPOINTS } from '@/types/api'

/** Custom error class for API errors */
export class ApiErrorClass extends Error {
  public status: number
  public apiError: ApiError

  constructor(status: number, apiError: ApiError) {
    const message = typeof apiError.detail === 'string' 
      ? apiError.detail 
      : 'API validation error'
    
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.apiError = apiError
  }
}

/** Make API request to calculate pot odds */
export async function calculatePotOdds(
  request: CalculateRequest,
  signal?: AbortSignal
): Promise<CalculationResponse> {
  try {
    const response = await fetch(`${API_ENDPOINTS.BASE_URL}${API_ENDPOINTS.CALCULATE}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
      signal,
    })

    if (!response.ok) {
      const errorData: ApiError = await response.json()
      throw new ApiErrorClass(response.status, errorData)
    }

    const data: CalculationResponse = await response.json()
    return data
  } catch (error) {
    if (error instanceof ApiErrorClass) {
      throw error
    }
    
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new Error('Request was cancelled')
    }
    
    if (error instanceof TypeError) {
      throw new Error('Network error - please check your connection')
    }
    
    throw new Error('An unexpected error occurred')
  }
}


/** Format API error message for display */
export function formatApiError(error: ApiError): string {
  if (typeof error.detail === 'string') {
    return error.detail
  }
  
  if (Array.isArray(error.detail) && error.detail.length > 0) {
    return error.detail.map(err => err.msg).join('; ')
  }
  
  return 'An unknown error occurred'
}

