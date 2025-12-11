/**
 * Home Page - List of upcoming games
 * 
 * Copyright (c) 2025 Jmenichole
 * Licensed under CC BY-NC 4.0
 * https://jmenichole.github.io/Portfolio/
 */

import axios from 'axios'
import Link from 'next/link'
import { useEffect, useState } from 'react'
import Header from '@/components/Header'
import Card from '@/components/Card'
import Button from '@/components/Button'

const API_URL = process.env.NEXT_PUBLIC_API_URL

interface Game {
  game_id: string
  sport: string
  team_a: string
  team_b: string
  scheduled_date: string
  result: string | null
}

const SUGGESTED_QUESTIONS = [
  "Which team has the best recent form?",
  "Who's more likely to win this matchup?",
  "What factors favor the home team?",
  "How accurate are recent predictions?",
  "What's the prediction confidence?",
  "Compare offensive vs defensive stats",
]

export default function Home() {
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchGames()
  }, [])

  const fetchGames = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/games`)
      setGames(response.data)
      setError('')
    } catch (err) {
      console.error('Error fetching games:', err)
      setError('Failed to load games. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <div className="min-h-screen bg-dark-bg flex flex-col">
      <Header title="BetCheck" subtitle="Sports Prediction Engine" />

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
        {/* Section Header */}
        <div className="mb-10">
          <h2 className="text-3xl sm:text-4xl font-bold text-text-primary mb-3">
            Upcoming Games
          </h2>
          <p className="text-text-secondary text-lg">
            Click on any game to view predictions and analysis
          </p>
        </div>

        {/* Suggested Questions */}
        {!loading && games.length > 0 && (
          <div className="mb-12">
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4">
              Common Questions
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {SUGGESTED_QUESTIONS.map((question, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    // Store question in session/context for future use
                    console.log('Clicked question:', question)
                  }}
                  className="text-left p-3 rounded-lg border border-gray-700 bg-dark-bg/50 hover:bg-gray-800 hover:border-neon-pink transition-all duration-300 group"
                >
                  <p className="text-white group-hover:text-neon-pink text-sm font-medium transition-colors">
                    {question}
                  </p>
                  <p className="text-xs text-text-secondary/60 mt-1 group-hover:text-neon-pink/60">
                    Click to explore
                  </p>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <div className="inline-block">
                <div className="w-12 h-12 border-2 border-white border-t-transparent rounded-full animate-spin mb-4"></div>
              </div>
              <p className="text-text-secondary text-lg">Loading games...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="border border-red-500/50 bg-red-500/10 mb-8">
            <div className="flex justify-between items-start gap-4">
              <div className="flex-1">
                <h3 className="text-red-400 font-bold mb-2">Error Loading Games</h3>
                <p className="text-red-300 text-sm">{error}</p>
              </div>
              <Button
                variant="primary"
                size="sm"
                onClick={fetchGames}
              >
                Retry
              </Button>
            </div>
          </Card>
        )}

        {/* Empty State */}
        {!loading && !error && games.length === 0 && (
          <Card className="border-dashed border-2 border-neon-pink/30 text-center py-12">
            <p className="text-text-secondary mb-4">
              No recent searches. Click a question above or use the search feature to get started.
            </p>
          </Card>
        )}

        {/* Games Grid - Hidden by default, shown only if user has recent searches */}
        {!loading && !error && games.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-text-secondary uppercase tracking-wider mb-6">
              Your Recent Searches (Last 48 Hours)
            </h3>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {games.map((game) => (
              <Link key={game.game_id} href={`/game/${game.game_id}`}>
                <Card
                  glowing={true}
                  onClick={() => {}}
                  className="h-full cursor-pointer group hover:scale-105"
                >
                  {/* Sport Badge */}
                  <div className="flex justify-end mb-4">
                    <span className="bg-neon-pink bg-opacity-20 text-neon-pink text-xs font-bold px-3 py-1 rounded-full border border-neon-pink group-hover:bg-neon-pink group-hover:text-dark-bg transition-all duration-300">
                      {game.sport.toUpperCase()}
                    </span>
                  </div>

                  {/* Teams */}
                  <div className="mb-6">
                    <h3 className="text-xl font-bold text-text-primary group-hover:text-neon-pink transition-colors duration-300">
                      {game.team_a}
                    </h3>
                    <p className="text-text-secondary text-sm my-2">vs</p>
                    <h3 className="text-xl font-bold text-text-primary group-hover:text-neon-pink transition-colors duration-300">
                      {game.team_b}
                    </h3>
                  </div>

                  {/* Divider */}
                  <div className="border-t border-dark-border my-6" />

                  {/* Game Info */}
                  <div className="space-y-3 mb-6">
                    <div>
                      <p className="text-text-secondary text-xs uppercase tracking-wider mb-1">
                        Scheduled
                      </p>
                      <p className="text-text-primary text-sm font-semibold">
                        {formatDate(game.scheduled_date)}
                      </p>
                    </div>

                    {game.result && (
                      <div className="pt-2 border-t border-dark-border">
                        <p className="text-text-secondary text-xs uppercase tracking-wider mb-1">
                          Result
                        </p>
                        <p className="text-neon-pink font-bold text-sm">
                          {game.result}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* CTA */}
                  <div className="text-neon-pink font-semibold text-sm group-hover:text-neon-pink-light transition-colors duration-300">
                    View Prediction →
                  </div>
                </Card>
              </Link>
            ))}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-dark-border mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
          <p className="text-text-secondary text-sm">
            Sports Prediction Tool © 2025 | Built with FastAPI + Next.js
          </p>
        </div>
      </footer>
    </div>
  )
}
