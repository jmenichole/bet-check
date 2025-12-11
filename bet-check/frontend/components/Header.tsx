/**
 * Header Component - Page header with navigation
 * 
 * Copyright (c) 2025 Jamie McNichol
 * Licensed under MIT License
 * https://jmenichole.github.io/Portfolio/
 */

import Link from 'next/link'

interface HeaderProps {
  title: string
  subtitle?: string
  showNav?: boolean
}

export default function Header({ title, subtitle, showNav = true }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 bg-dark-bg/95 backdrop-blur border-b border-dark-border shadow-lg shadow-neon-pink/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex justify-between items-center">
          <div>
            <Link href="/">
              <h1 className="text-2xl sm:text-3xl font-bold text-text-primary hover:text-neon-pink transition-colors duration-300">
                ⚡ BetCheck
              </h1>
            </Link>
            {subtitle && (
              <p className="text-text-secondary text-sm mt-1">{subtitle}</p>
            )}
          </div>
          
          {showNav && (
            <nav className="flex gap-2 sm:gap-4">
              <Link href="/">
                <span className="px-3 py-2 rounded-lg text-text-secondary hover:text-neon-pink hover:bg-dark-card transition-all duration-300">
                  Games
                </span>
              </Link>
              <Link href="/dashboard">
                <span className="px-3 py-2 rounded-lg text-text-secondary hover:text-neon-pink hover:bg-dark-card transition-all duration-300">
                  Dashboard
                </span>
              </Link>
            </nav>
          )}
        </div>
      </div>
    </header>
  )
}
