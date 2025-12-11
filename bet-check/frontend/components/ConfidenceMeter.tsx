/**
 * Confidence Meter Component - Visual confidence indicator with neon effect
 * 
 * Copyright (c) 2025 Jamie McNichol
 * Licensed under MIT License
 * https://jmenichole.github.io/Portfolio/
 */

interface ConfidenceMeterProps {
  confidence: number
  size?: 'sm' | 'md' | 'lg'
}

export default function ConfidenceMeter({ confidence, size = 'md' }: ConfidenceMeterProps) {
  const percentage = Math.round(confidence * 100)
  
  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
  }

  const labelSize = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
  }

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <span className={`${labelSize[size]} font-semibold text-text-primary`}>
          Confidence
        </span>
        <span className={`${labelSize[size]} font-bold text-neon-pink`}>
          {percentage}%
        </span>
      </div>
      
      <div className={`${sizeClasses[size]} w-full bg-dark-border rounded-full overflow-hidden relative`}>
        {/* Glitch effect background */}
        <div 
          className="absolute inset-0 bg-neon-pink rounded-full transition-all duration-300"
          style={{ width: `${percentage}%` }}
        >
          {/* Subtle glitch/glow effect */}
          <div className="absolute inset-0 animate-pulse opacity-70" />
          <div className="absolute top-0 left-0 right-0 bottom-0 bg-gradient-to-r from-neon-pink to-neon-pink-light opacity-50" />
        </div>
        
        {/* Neon glow wrapper */}
        <div 
          className="absolute top-0 left-0 h-full rounded-full"
          style={{
            width: `${percentage}%`,
            boxShadow: `0 0 8px rgba(255, 0, 204, 0.6), inset 0 0 8px rgba(255, 0, 204, 0.3)`,
          }}
        />
      </div>
    </div>
  )
}
