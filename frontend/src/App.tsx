// Main application component

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { ErrorBoundary } from '@/components/ui/ErrorBoundary'
import { MainLayout } from '@/components/layout/MainLayout'
import { ResponsiveGrid, GridSection } from '@/components/layout/ResponsiveGrid'
import { HoleCardsSection } from '@/components/card-selection/HoleCardsSection'
import { CommunityCardsSection } from '@/components/card-selection/CommunityCardsSection'
import { ResetButton } from '@/components/card-selection/ResetButton'
import { ResultsPanel } from '@/components/results/ResultsPanel'
import { useAutoPotOdds } from '@/hooks/usePotOdds'
import { useTheme } from '@/hooks/useTheme'
import './index.css'

// Create a client instance
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 30000, // 30 seconds
      gcTime: 300000, // 5 minutes
    },
  },
})

function AppContent() {
  // Initialize theme
  useTheme()
  
  // Start automatic pot odds calculation
  useAutoPotOdds({
    debounceMs: 150,
  })
  
  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Main grid layout */}
        <ResponsiveGrid>
          {/* Card Selection Section */}
          <GridSection>
            <div className="space-y-8">
              <HoleCardsSection />
              <CommunityCardsSection />
              <div className="flex justify-center">
                <ResetButton />
              </div>
            </div>
          </GridSection>
          
          {/* Results Section */}
          <GridSection priority="high">
            <ResultsPanel />
          </GridSection>
        </ResponsiveGrid>
      </div>
    </MainLayout>
  )
}

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AppContent />
        {import.meta.env.DEV && (
          <ReactQueryDevtools initialIsOpen={false} />
        )}
      </QueryClientProvider>
    </ErrorBoundary>
  )
}

export default App