/**
 * Button Component - Styled button with neon effects
 * 
 * Copyright (c) 2025 Jamie McNichol
 * Licensed under MIT License
 * https://jmenichole.github.io/Portfolio/
 */

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  glow?: boolean
}

export default function Button({ 
  children, 
  variant = 'primary', 
  size = 'md',
  glow = true,
  className = '',
  ...props 
}: ButtonProps) {
  const baseClasses = 'font-semibold rounded-lg transition-all duration-300 ease-in-out'
  
  const variantClasses = {
    primary: 'bg-neon-pink hover:bg-neon-pink-light text-dark-bg border border-neon-pink hover:border-neon-pink-light',
    secondary: 'bg-dark-card text-neon-pink border border-neon-pink hover:bg-neon-pink hover:text-dark-bg',
    outline: 'bg-transparent text-neon-pink border border-neon-pink hover:bg-neon-pink hover:bg-opacity-10',
  }

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  const glowClass = glow ? 'hover:shadow-glow-pink' : ''

  return (
    <button
      className={`
        ${baseClasses}
        ${variantClasses[variant]}
        ${sizeClasses[size]}
        ${glowClass}
        disabled:opacity-50 disabled:cursor-not-allowed
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  )
}
