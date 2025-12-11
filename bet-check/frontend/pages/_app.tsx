/**
 * App Component - Global layout wrapper
 * 
 * Copyright (c) 2025 Jmenichole
 * Licensed under MIT License
 * https://jmenichole.github.io/Portfolio/
 */

import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import Head from 'next/head'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>
      <div className="min-h-screen flex flex-col bg-dark-bg">
        <Component {...pageProps} />
      </div>
    </>
  )
}
