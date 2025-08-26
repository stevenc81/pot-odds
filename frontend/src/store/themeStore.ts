// Zustand store for theme management

import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type { Theme } from '@/types'
import { getStoredTheme, storeTheme, applyTheme, toggleTheme } from '@/utils/theme'

interface ThemeState {
  theme: Theme
  setTheme: (theme: Theme) => void
  toggleTheme: () => void
  initializeTheme: () => void
}

export const useThemeStore = create<ThemeState>()(
  devtools(
    persist(
      (set, get) => ({
        theme: 'light',
        
        setTheme: (theme: Theme) => {
          set({ theme }, false, 'setTheme')
          applyTheme(theme)
          storeTheme(theme)
        },
        
        toggleTheme: () => {
          const currentTheme = get().theme
          const newTheme = toggleTheme(currentTheme)
          get().setTheme(newTheme)
        },
        
        initializeTheme: () => {
          const storedTheme = getStoredTheme()
          set({ theme: storedTheme }, false, 'initializeTheme')
          applyTheme(storedTheme)
        },
      }),
      {
        name: 'theme-store',
        partialize: (state) => ({ theme: state.theme }),
      }
    ),
    {
      name: 'theme-store',
    }
  )
)

