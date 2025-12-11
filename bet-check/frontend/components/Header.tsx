/**
 * Header Component - Page header with navigation
 * 
 * Copyright (c) 2025 Jmenichole
 * Licensed under CC BY-NC 4.0
 * https://jmenichole.github.io/Portfolio/
 */

import Link from 'next/link'

interface HeaderProps {
  title?: string
  subtitle?: string
  showNav?: boolean
}

export default function Header({ title = "BetCheck", subtitle, showNav = true }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 bg-dark-bg/95 backdrop-blur border-b border-gray-800 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex justify-between items-center">
          <div>
            <Link href="/">
              <h1 className="text-2xl sm:text-3xl font-bold text-white hover:text-neon-pink transition-colors duration-300">
                {title}
              </h1>
            </Link>
            {subtitle && (
              <p className="text-gray-400 text-sm mt-1">{subtitle}</p>
            )}
          </div>
          
          {showNav && (
            <nav className="flex gap-4 items-center">
              <Link href="/">
                <span className="px-4 py-2 rounded-lg text-white hover:text-neon-pink hover:bg-gray-800/50 transition-all duration-300">
                  Games
                </span>
              </Link>
              <Link href="/past-games">
                <span className="px-4 py-2 rounded-lg text-white hover:text-neon-pink hover:bg-gray-800/50 transition-all duration-300">
                  History
                </span>
              </Link>
              <Link href="/guru">
                <span className="px-4 py-2 rounded-lg text-white hover:text-neon-pink hover:bg-gray-800/50 transition-all duration-300">
                  AI Guru
                </span>
              </Link>
              <Link href="/mines">
                <span className="px-4 py-2 rounded-lg text-white hover:text-neon-pink hover:bg-gray-800/50 transition-all duration-300">
                  Mines
                </span>
              </Link>
              <Link href="/dashboard">
                <span className="px-4 py-2 rounded-lg text-white hover:text-neon-pink hover:bg-gray-800/50 transition-all duration-300">
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
