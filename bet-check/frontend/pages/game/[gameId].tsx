/**
 * Game Prediction Page - Detailed prediction with confidence and reasoning
 * 
 * Copyright (c) 2025 Jamie McNichol
 * Licensed under MIT License
 * https://jmenichole.github.io/Portfolio/
 */

import axios from 'axios'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import Header from '@/components/Header'
import Card from '@/components/Card'
import ConfidenceMeter from '@/components/ConfidenceMeter'
import ReasonItem from '@/components/ReasonItem'
import Button from '@/components/Button'

const API_URL = process.env.NEXT_PUBLIC_API_URL

interface Prediction {
  game_id: string
  predicted_outcome: string
  confidence: number
  reasons: string[]
  factor_contributions: Record<string, { team_a: number; team_b: number }>
}

interface Game {
  game_id: string
  sport: string
  team_a: string
  team_b: string
  scheduled_date: string
  result: string | null
}

export default function GamePrediction() {
  const router = useRouter()
  const { gameId } = router.query

  const [game, setGame] = useState<Game | null>(null)
  const [prediction, setPrediction] = useState<Prediction | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!gameId) return

    fetchGameAndPrediction()
  }, [gameId])

  const fetchGameAndPrediction = async () => {
    try {
      setLoading(true)

      // Fetch game details
      const gameResponse = await axios.get(`${API_URL}/games?sport=nba`)
      const gameData = gameResponse.data.find((g: Game) => g.game_id === gameId)
      setGame(gameData || null)

      // Fetch prediction
      const predResponse = await axios.get(`${API_URL}/predict/${gameId}`)
      setPrediction(predResponse.data)

      setError('')
    } catch (err) {
      console.error('Error fetching data:', err)
      setError('Failed to load game or prediction. Make sure the backend is running.')
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
      <Header title="BetCheck" subtitle="Game Prediction Analysis" />

      {/* Main Content */}
      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <div className="inline-block">
                <div className="w-12 h-12 border-2 border-neon-pink border-t-transparent rounded-full animate-spin mb-4"></div>
              </div>
              <p className="text-text-secondary text-lg">Loading prediction...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="border border-red-500/50 bg-red-500/10 mb-8">
            <div className="flex justify-between items-start gap-4">
              <div className="flex-1">
                <h3 className="text-red-400 font-bold mb-2">Error Loading Prediction</h3>
                <p className="text-red-300 text-sm">{error}</p>
              </div>
              <Button
                variant="primary"
                size="sm"
                onClick={fetchGameAndPrediction}
              >
                Retry
              </Button>
            </div>
          </Card>
        )}

        {!loading && !error && game && prediction && (
          <div className="space-y-8">
            {/* Game Card */}
            <Card glowing={true}>
              <div className="mb-8">
                <div className="flex justify-between items-center gap-4 mb-8">
                  <div className="flex-1 text-center">
                    <h2 className="text-3xl sm:text-4xl font-bold text-text-primary mb-2">
                      {game.team_a}
                    </h2>
                  </div>
                  <div className="px-4 sm:px-6 text-text-secondary font-medium">vs</div>
                  <div className="flex-1 text-center">
                    <h2 className="text-3xl sm:text-4xl font-bold text-text-primary mb-2">
                      {game.team_b}
                    </h2>
                  </div>
                </div>

                <div className="border-t border-dark-border pt-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <p className="text-text-secondary text-xs uppercase tracking-widest mb-2">
                        Scheduled
                      </p>
                      <p className="text-text-primary font-semibold">
                        {formatDate(game.scheduled_date)}
                      </p>
                    </div>

                    {game.result && (
                      <div>
                        <p className="text-text-secondary text-xs uppercase tracking-widest mb-2">
                          Final Result
                        </p>
                        <p className="text-neon-pink font-bold text-lg">
                          {game.result}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </Card>

            {/* Prediction Card */}
            <Card glowing={true}>
              <h3 className="text-2xl font-bold text-text-primary mb-8">
                Prediction Analysis
              </h3>

              <div className="grid gap-8 md:grid-cols-2 mb-8">
                {/* Predicted Outcome */}
                <div className="text-center">
                  <p className="text-text-secondary text-xs uppercase tracking-widest mb-4">
                    Predicted Winner
                  </p>
                  <p className="text-4xl font-bold text-neon-pink animate-pulse">
                    {prediction.predicted_outcome}
                  </p>
                </div>

                {/* Confidence Meter */}
                <div>
                  <ConfidenceMeter confidence={prediction.confidence} size="lg" />
                </div>
              </div>

              {/* Divider */}
              <div className="border-t border-dark-border my-8" />

              {/* Top 3 Reasons */}
              <div>
                <h4 className="text-lg font-bold text-text-primary mb-6">
                  Top Reasons
                </h4>
                <div className="space-y-4">
                  {prediction.reasons.map((reason, index) => (
                    <ReasonItem
                      key={index}
                      reason={reason}
                      index={index}
                    />
                  ))}
                </div>
              </div>
            </Card>

            {/* Factor Analysis */}
            <Card glowing={true}>
              <h3 className="text-2xl font-bold text-text-primary mb-8">
                Factor Analysis
              </h3>

              <div className="space-y-6">
                {Object.entries(prediction.factor_contributions).map(([factor, scores]) => (
                  <div key={factor} className="border border-dark-border rounded-lg p-6 bg-dark-bg/50 hover:border-neon-pink transition-colors duration-300">
                    <h4 className="font-bold text-text-primary mb-6">{factor}</h4>

                    <div className="grid md:grid-cols-2 gap-6">
                      {/* Team A */}
                      <div>
                        <p className="text-text-secondary text-sm font-semibold mb-3">
                          {game.team_a}
                        </p>
                        <div className="space-y-2">
                          <div className="h-3 bg-dark-border rounded-full overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-neon-pink to-neon-pink-light rounded-full transition-all duration-500"
                              style={{ width: `${Math.max(scores.team_a * 100, 5)}%` }}
                            >
                              <div className="h-full bg-neon-pink animate-pulse opacity-70" />
                            </div>
                          </div>
                          <p className="text-neon-pink font-bold text-sm">
                            {(scores.team_a * 100).toFixed(1)}%
                          </p>
                        </div>
                      </div>

                      {/* Team B */}
                      <div>
                        <p className="text-text-secondary text-sm font-semibold mb-3">
                          {game.team_b}
                        </p>
                        <div className="space-y-2">
                          <div className="h-3 bg-dark-border rounded-full overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-neon-pink to-neon-pink-light rounded-full transition-all duration-500"
                              style={{ width: `${Math.max(scores.team_b * 100, 5)}%` }}
                            >
                              <div className="h-full bg-neon-pink animate-pulse opacity-70" />
                            </div>
                          </div>
                          <p className="text-neon-pink font-bold text-sm">
                            {(scores.team_b * 100).toFixed(1)}%
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Info Box */}
            <Card className="border-neon-pink/30 bg-neon-pink/5">
              <div className="flex gap-4">
                <span className="text-2xl">⚡</span>
                <div>
                  <p className="text-text-primary font-semibold mb-2">
                    How Our Predictions Work
                  </p>
                  <p className="text-text-secondary text-sm leading-relaxed">
                    Our prediction engine analyzes multiple factors including recent form, injuries, offensive/defensive efficiency, and home court advantage. The model continuously learns and adapts its weights based on prediction accuracy to improve future forecasts.
                  </p>
                </div>
              </div>
            </Card>

            {/* Back Button */}
            <div className="flex justify-center">
              <Link href="/">
                <Button variant="secondary" size="md">
                  ← Back to Games
                </Button>
              </Link>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-dark-border mt-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
          <p className="text-text-secondary text-sm">
            Sports Prediction Tool © 2025 | Built with FastAPI + Next.js
          </p>
        </div>
      </footer>
    </div>
  )
}
