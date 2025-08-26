// Theme management utilities

import type { Theme } from '@/types'

const THEME_STORAGE_KEY = 'pot-odds-theme'

/** Get theme preference from localStorage or system preference */
export function getStoredTheme(): Theme {
  try {
    const stored = localStorage.getItem(THEME_STORAGE_KEY) as Theme | null
    
    if (stored === 'light' || stored === 'dark') {
      return stored
    }
    
    // Fall back to system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark'
    }
    
    return 'light'
  } catch {
    return 'light'
  }
}

/** Store theme preference in localStorage */
export function storeTheme(theme: Theme): void {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme)
  } catch {
    // Ignore storage errors
  }
}

/** Apply theme to document */
export function applyTheme(theme: Theme): void {
  const root = document.documentElement
  
  if (theme === 'dark') {
    root.classList.add('dark')
  } else {
    root.classList.remove('dark')
  }
}

/** Toggle theme */
export function toggleTheme(currentTheme: Theme): Theme {
  return currentTheme === 'light' ? 'dark' : 'light'
}

/** Listen for system theme changes */
export function watchSystemTheme(callback: (theme: Theme) => void): () => void {
  if (!window.matchMedia) {
    return () => {}
  }
  
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  
  const handleChange = (e: MediaQueryListEvent) => {
    // Only update if no user preference is stored
    try {
      const stored = localStorage.getItem(THEME_STORAGE_KEY)
      if (!stored) {
        callback(e.matches ? 'dark' : 'light')
      }
    } catch {
      callback(e.matches ? 'dark' : 'light')
    }
  }
  
  mediaQuery.addEventListener('change', handleChange)
  
  return () => {
    mediaQuery.removeEventListener('change', handleChange)
  }
}