// Responsive grid layout for card selection and results

import { type ReactNode } from 'react'
import clsx from 'clsx'

interface ResponsiveGridProps {
  children: ReactNode
  className?: string
}

export function ResponsiveGrid({ children, className }: ResponsiveGridProps) {
  return (
    <div className={clsx(
      // Mobile: Stack vertically
      'space-y-6',
      // Desktop: Side-by-side grid
      'lg:grid lg:grid-cols-2 lg:gap-8 lg:space-y-0',
      className
    )}>
      {children}
    </div>
  )
}

interface GridSectionProps {
  children: ReactNode
  className?: string
  priority?: 'high' | 'normal'
}

export function GridSection({ children, className, priority = 'normal' }: GridSectionProps) {
  return (
    <div className={clsx(
      'space-y-6',
      // On mobile, high priority sections come first
      priority === 'high' && 'order-first lg:order-none',
      className
    )}>
      {children}
    </div>
  )
}