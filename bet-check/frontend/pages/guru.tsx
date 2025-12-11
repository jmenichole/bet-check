/**
 * AI Sports Guru Page - Chat interface with game predictions
 * 
 * Copyright (c) 2025 Jmenichole
 * Licensed under CC BY-NC 4.0
 * https://jmenichole.github.io/Portfolio/
 */

import Header from '@/components/Header'
import ChatEmbedded from '@/components/ChatEmbedded'
import PopularMatchesList from '@/components/PopularMatchesList'

export default function GuruPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0a0a] via-[#1a0a1f] to-[#0a1a1f]">
      <Header title="AI Sports Guru" />
      
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header Section */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#ff00cc] to-[#00ffff] mb-3">
            AI Sports Guru
          </h1>
          <p className="text-gray-400 text-sm md:text-base">
            Ask me anything about upcoming games and get AI-powered predictions
          </p>
        </div>

        {/* Chat Module */}
        <div className="mb-8">
          <ChatEmbedded />
        </div>

        {/* Popular Matches */}
        <div>
          <PopularMatchesList />
        </div>

        {/* Info Section */}
        <div className="mt-12 text-center">
          <div className="inline-block bg-[#1a1a1a]/50 border border-[#ff00cc]/20 rounded-lg px-6 py-4 max-w-2xl">
            <p className="text-gray-400 text-sm mb-2">
              💡 <span className="text-[#ff00cc] font-semibold">Pro Tip:</span>
            </p>
            <p className="text-gray-300 text-xs">
              Try asking "Show me the best NBA picks for today" or "What are the safest bets?"
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 mt-16 py-6">
        <div className="container mx-auto px-4 text-center text-gray-500 text-xs">
          <p>Powered by adaptive machine learning • BetCheck © 2025 Jmenichole</p>
          <p className="mt-2">
            <a
              href="https://www.begambleaware.org"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-neon-cyan transition-colors"
            >
              🎲 Gamble Responsibly
            </a>
          </p>
        </div>
      </footer>
    </div>
  )
}
