/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Poker-themed color palette
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          900: '#0c4a6e',
        },
        // Card suits colors
        spade: {
          light: '#000000',
          dark: '#ffffff',
        },
        club: {
          light: '#000000', 
          dark: '#ffffff',
        },
        heart: {
          light: '#dc2626',
          dark: '#f87171',
        },
        diamond: {
          light: '#dc2626',
          dark: '#f87171',
        },
        // Theme colors
        surface: {
          light: '#ffffff',
          dark: '#1a1a1a',
        },
        background: {
          light: '#f8fafc',
          dark: '#0f0f0f',
        },
        card: {
          light: '#ffffff',
          dark: '#2d2d2d',
          selected: '#10b981',
          'selected-dark': '#059669',
          'selected-bg': '#d1fae5',
          'selected-bg-dark': '#064e3b',
        },
        // Status colors
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        '26': '6.5rem',
      },
      borderRadius: {
        'card': '0.75rem',
      },
      boxShadow: {
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'card-selected': '0 0 0 3px rgb(16 185 129 / 0.6), 0 8px 25px -5px rgb(16 185 129 / 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'card-dark': '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
        'card-selected-dark': '0 0 0 3px rgb(5 150 105 / 0.8), 0 8px 25px -5px rgb(5 150 105 / 0.6), 0 10px 10px -5px rgba(0, 0, 0, 0.2)',
      },
      textShadow: {
        'card-dark': '0 1px 2px rgba(0, 0, 0, 0.8)',
        'card-light': '0 1px 2px rgba(255, 255, 255, 0.8)',
      },
      animation: {
        'scale-in': 'scaleIn 0.15s ease-out',
      },
      keyframes: {
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}