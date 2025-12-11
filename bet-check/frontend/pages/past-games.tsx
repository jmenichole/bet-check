/**
 * Past Games Page - Completed games and prediction accuracy
 * 
 * Copyright (c) 2025 Jamie McNichol
 * Licensed under MIT License
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

interface GameWithAccuracy extends Game {
  prediction?: string
  isCorrect?: boolean
}

export default function PastGames() {
  const [games, setGames] = useState<GameWithAccuracy[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedSport, setSelectedSport] = useState<string>('all')

  const sports = [
    { id: 'all', name: 'All Sports' },
    { id: 'nba', name: 'NBA' },
    { id: 'nfl', name: 'NFL' },
    { id: 'nhl', name: 'NHL' },
    { id: 'mlb', name: 'MLB' },
    { id: 'ncaaf', name: 'NCAAF' },
    { id: 'ncaab', name: 'NCAAB' },
  ]

  useEffect(() => {
    fetchCompletedGames()
  }, [selectedSport])

  const fetchCompletedGames = async () => {
    try {
      setLoading(true)
      const url = selectedSport === 'all'
        ? `${API_URL}/games`
        : `${API_URL}/games?sport=${selectedSport}`

      const response = await axios.get(url)
      // Filter only games with results
      const completedGames = response.data.filter((g: Game) => g.result)
      setGames(completedGames)
      setError('')
    } catch (err) {
      console.error('Error fetching games:', err)
      setError('Failed to load past games.')
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

  const calculateAccuracy = () => {
    const withPrediction = games.filter(g => g.isCorrect !== undefined)
    if (withPrediction.length === 0) return 0
    const correct = withPrediction.filter(g => g.isCorrect).length
    return Math.round((correct / withPrediction.length) * 100)
  }

  return (
    <div className="min-h-screen bg-dark-bg flex flex-col">
      <Header title="BetCheck" subtitle="Past Games & Prediction Accuracy" />

      <main className="flex-1 max-w-6xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
        {/* Stats Section */}
        <div className="mb-12 grid md:grid-cols-3 gap-6">
          <Card glowing={true}>
            <div className="text-center">
              <p className="text-text-secondary text-sm uppercase tracking-widest mb-2">Total Games</p>
              <p className="text-4xl font-bold text-neon-pink">{games.length}</p>
            </div>
          </Card>

          <Card glowing={true}>
            <div className="text-center">
              <p className="text-text-secondary text-sm uppercase tracking-widest mb-2">Overall Accuracy</p>
              <p className="text-4xl font-bold text-green-400">{calculateAccuracy()}%</p>
            </div>
          </Card>

          <Card glowing={true}>
            <div className="text-center">
              <p className="text-text-secondary text-sm uppercase tracking-widest mb-2">With Results</p>
              <p className="text-4xl font-bold text-blue-400">{games.filter(g => g.result).length}</p>
            </div>
          </Card>
        </div>

        {/* Sport Filter Tabs */}
        <div className="mb-8 flex flex-wrap gap-2">
          {sports.map((sport) => (
            <button
              key={sport.id}
              onClick={() => setSelectedSport(sport.id)}
              className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all duration-300 ${
                selectedSport === sport.id
                  ? 'bg-neon-pink text-dark-bg border-2 border-neon-pink'
                  : 'bg-dark-card border-2 border-dark-border text-text-primary hover:border-neon-pink hover:text-neon-pink'
              }`}
            >
              {sport.name}
            </button>
          ))}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <div className="inline-block">
                <div className="w-12 h-12 border-2 border-neon-pink border-t-transparent rounded-full animate-spin mb-4"></div>
              </div>
              <p className="text-text-secondary text-lg">Loading past games...</p>
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
              <Button variant="primary" size="sm" onClick={fetchCompletedGames}>
                Retry
              </Button>
            </div>
          </Card>
        )}

        {/* Empty State */}
        {!loading && !error && games.length === 0 && (
          <Card className="border-dashed border-2 border-neon-pink/30 text-center py-12">
            <p className="text-text-secondary mb-4">
              No completed games found. Check back once games are finished!
            </p>
            <Link href="/">
              <Button variant="primary" size="md">
                Browse Upcoming Games
              </Button>
            </Link>
          </Card>
        )}

        {/* Games Grid */}
        {!loading && !error && games.length > 0 && (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {games.map((game) => (
              <Link key={game.game_id} href={`/game/${game.game_id}`}>
                <Card
                  glowing={true}
                  className="h-full cursor-pointer group hover:scale-105"
                >
                  {/* Sport Badge & Result Status */}
                  <div className="flex justify-between items-start gap-2 mb-4">
                    <span className="bg-neon-pink bg-opacity-20 text-neon-pink text-xs font-bold px-3 py-1 rounded-full border border-neon-pink group-hover:bg-neon-pink group-hover:text-dark-bg transition-all">
                      {game.sport.toUpperCase()}
                    </span>
                    {game.result && (
                      <span className="text-lg font-bold">
                        ✓
                      </span>
                    )}
                  </div>

                  {/* Teams */}
                  <div className="mb-6">
                    <h3 className="text-lg font-bold text-text-primary group-hover:text-neon-pink transition-colors">
                      {game.team_a}
                    </h3>
                    <p className="text-text-secondary text-sm my-2">vs</p>
                    <h3 className="text-lg font-bold text-text-primary group-hover:text-neon-pink transition-colors">
                      {game.team_b}
                    </h3>
                  </div>

                  <div className="border-t border-dark-border my-4" />

                  {/* Date and Result */}
                  <div className="space-y-3">
                    <div>
                      <p className="text-text-secondary text-xs uppercase tracking-wider mb-1">Date</p>
                      <p className="text-text-primary text-sm font-semibold">
                        {formatDate(game.scheduled_date)}
                      </p>
                    </div>

                    {game.result && (
                      <div>
                        <p className="text-text-secondary text-xs uppercase tracking-wider mb-1">Final Result</p>
                        <p className="text-neon-pink font-bold text-sm">
                          {game.result}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* View Details Link */}
                  <div className="mt-6 pt-4 border-t border-dark-border">
                    <p className="text-neon-pink text-sm font-semibold group-hover:translate-x-1 transition-transform">
                      View Details →
                    </p>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        )}

        {/* Back Button */}
        <div className="flex justify-center mt-12">
          <Link href="/">
            <Button variant="secondary" size="md">
              ← Back to Upcoming Games
            </Button>
          </Link>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-dark-border mt-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
          <p className="text-text-secondary text-sm">
            Sports Prediction Tool © 2025 | Past Games & Accuracy Tracking
          </p>
        </div>
      </footer>
    </div>
  )
}
