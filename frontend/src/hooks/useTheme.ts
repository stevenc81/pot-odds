// Custom hook for theme management

import { useEffect } from 'react'
import { useThemeStore } from '@/store/themeStore'
import { watchSystemTheme } from '@/utils/theme'

/**
 * Custom hook for theme management
 * Provides theme state and actions, and handles system theme changes
 */
export function useTheme() {
  const theme = useThemeStore(state => state.theme)
  const setTheme = useThemeStore(state => state.setTheme)
  const toggleTheme = useThemeStore(state => state.toggleTheme)
  const initializeTheme = useThemeStore(state => state.initializeTheme)
  
  // Initialize theme on first load
  useEffect(() => {
    initializeTheme()
  }, [initializeTheme])
  
  // Watch for system theme changes
  useEffect(() => {
    const unwatch = watchSystemTheme((newTheme) => {
      // Only update if no user preference is stored
      try {
        const hasStoredPreference = localStorage.getItem('theme-store') !== null
        if (!hasStoredPreference) {
          setTheme(newTheme)
        }
      } catch {
        // If localStorage is not available, just update the theme
        setTheme(newTheme)
      }
    })
    
    return unwatch
  }, [setTheme])
  
  return {
    theme,
    setTheme,
    toggleTheme,
    isDark: theme === 'dark',
    isLight: theme === 'light',
  }
}