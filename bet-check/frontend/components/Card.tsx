/**
 * Card Component - Reusable neon-themed card container
 * 
 * Copyright (c) 2025 Jamie McNichol
 * Licensed under MIT License
 * https://jmenichole.github.io/Portfolio/
 */

interface CardProps {
  children: React.ReactNode
  className?: string
  glowing?: boolean
  onClick?: () => void
}

export default function Card({ children, className = '', glowing = false, onClick }: CardProps) {
  return (
    <div
      onClick={onClick}
      className={`
        bg-dark-card border border-dark-border rounded-lg p-6
        transition-all duration-300 ease-in-out
        ${glowing ? 'shadow-neon-pink-lg' : 'shadow-neon-pink'}
        ${onClick ? 'cursor-pointer hover:shadow-neon-pink-lg hover:border-neon-pink' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  )
}
