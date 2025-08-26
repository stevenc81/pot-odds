// Main application layout with responsive design

import { type ReactNode } from 'react'
import clsx from 'clsx'
import { Header } from './Header'
import { Footer } from './Footer'

interface MainLayoutProps {
  children: ReactNode
  className?: string
}

export function MainLayout({ children, className }: MainLayoutProps) {
  return (
    <div className="min-h-screen flex flex-col bg-background-light dark:bg-background-dark">
      <Header />
      
      <main className={clsx(
        'flex-1 container mx-auto px-4 py-6 md:py-8',
        className
      )}>
        {children}
      </main>
      
      <Footer />
    </div>
  )
}