/**
 * Reason Item Component - Individual prediction reason with neon bullet
 * 
 * Copyright (c) 2025 Jamie McNichol
 * Licensed under MIT License
 * https://jmenichole.github.io/Portfolio/
 */

interface ReasonItemProps {
  reason: string
  index: number
}

const icons = ['⚡', '📊', '🏆', '💯', '🎯']

export default function ReasonItem({ reason, index }: ReasonItemProps) {
  const icon = icons[index % icons.length]

  return (
    <div className="group relative">
      <div className="flex items-start gap-4 p-4 bg-dark-card border border-dark-border rounded-lg hover:border-neon-pink transition-all duration-300 group-hover:shadow-neon-pink">
        {/* Neon bullet/icon */}
        <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-neon-pink bg-opacity-20 border border-neon-pink text-neon-pink font-bold group-hover:bg-neon-pink group-hover:text-dark-bg group-hover:shadow-glow-pink transition-all duration-300">
          {icon}
        </div>
        
        {/* Reason text */}
        <p className="flex-1 text-text-primary text-sm sm:text-base leading-relaxed group-hover:text-neon-pink-light transition-colors duration-300">
          {reason}
        </p>
      </div>
    </div>
  )
}
