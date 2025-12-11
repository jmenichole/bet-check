/**
 * Popular Matches List - Small card list under chat
 * Displays trending/popular games with predictions
 * 
 * Copyright (c) 2025 Jmenichole
 * Licensed under CC BY-NC 4.0
 * https://jmenichole.github.io/Portfolio/
 */

import { useState, useEffect } from 'react'
import axios from 'axios'
import Link from 'next/link'

const API_URL = process.env.NEXT_PUBLIC_API_URL

interface PopularGame {
  game_id: string
  sport: string
  team_a: string
  team_b: string
  scheduled_date: string
  predicted_outcome: string
  confidence: number
}

export default function PopularMatchesList() {
  const [games, setGames] = useState<PopularGame[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPopularGames()
  }, [])

  const fetchPopularGames = async () => {
    try {
      const response = await axios.get(`${API_URL}/chat/popular-games`)
      setGames(response.data)
    } catch (error) {
      console.error('Error fetching popular games:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="mt-6">
        <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
          <span className="text-2xl">🔥</span>
          Popular Matches
        </h3>
        <div className="text-gray-400 text-center py-8">Loading...</div>
      </div>
    )
  }

  if (games.length === 0) {
    return null
  }

  return (
    <div className="mt-6">
      <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
        <span className="text-2xl">🔥</span>
        Popular Matches
      </h3>

      {/* Horizontal scroll container for mobile, grid for desktop */}
      <div className="overflow-x-auto pb-4">
        <div className="flex gap-4 md:grid md:grid-cols-2 lg:grid-cols-4 md:gap-4">
          {games.map((game) => (
            <Link
              key={game.game_id}
              href={`/game/${game.game_id}`}
              className="flex-shrink-0 w-72 md:w-auto"
            >
              <div className="bg-[#1a1a1a] border border-[#00ffff]/30 rounded-lg p-4 hover:border-[#00ffff] hover:shadow-lg hover:shadow-[#00ffff]/30 transition-all duration-300 cursor-pointer h-full">
                {/* Sport badge */}
                <div className="inline-block bg-gradient-to-r from-[#ff00cc]/20 to-[#00ffff]/20 border border-[#00ffff]/40 rounded-full px-3 py-1 mb-3">
                  <span className="text-[#00ffff] text-xs font-bold uppercase">
                    {game.sport}
                  </span>
                </div>

                {/* Teams */}
                <div className="mb-3">
                  <div className="text-white font-semibold text-sm mb-1">
                    {game.team_a}
                  </div>
                  <div className="text-gray-500 text-xs mb-1">vs</div>
                  <div className="text-white font-semibold text-sm">
                    {game.team_b}
                  </div>
                </div>

                {/* Date */}
                <div className="text-gray-400 text-xs mb-3">
                  📅 {new Date(game.scheduled_date).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                  })}
                </div>

                {/* Prediction */}
                <div className="pt-3 border-t border-gray-700">
                  <div className="flex justify-between items-center">
                    <div className="text-gray-400 text-xs">Confidence</div>
                    <div className="text-[#ff00cc] font-bold text-lg">
                      {game.confidence}%
                    </div>
                  </div>
                  
                  {/* Confidence bar */}
                  <div className="mt-2 h-1.5 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-[#ff00cc] to-[#00ffff] rounded-full transition-all duration-500"
                      style={{ width: `${game.confidence}%` }}
                    ></div>
                  </div>

                  {/* Prediction text */}
                  <div className="text-white text-xs mt-2 truncate">
                    ⚡ {game.predicted_outcome}
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Custom scrollbar for horizontal scroll */}
      <style jsx>{`
        .overflow-x-auto::-webkit-scrollbar {
          height: 6px;
        }
        .overflow-x-auto::-webkit-scrollbar-track {
          background: #1a1a1a;
          border-radius: 3px;
        }
        .overflow-x-auto::-webkit-scrollbar-thumb {
          background: #ff00cc;
          border-radius: 3px;
        }
        .overflow-x-auto::-webkit-scrollbar-thumb:hover {
          background: #00ffff;
        }
      `}</style>
    </div>
  )
}
