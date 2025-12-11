/**
 * App Component - Global layout wrapper
 * 
 * Copyright (c) 2025 Jmenichole
 * Licensed under MIT License
 * https://jmenichole.github.io/Portfolio/
 */

import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import Footer from '@/components/Footer'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div className="min-h-screen flex flex-col bg-dark-bg">
      <Component {...pageProps} />
      <Footer />
    </div>
  )
}
