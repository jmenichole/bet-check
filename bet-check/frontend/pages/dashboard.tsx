/**
 * Dashboard Page - Accuracy metrics and factor weights
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

interface Factor {
  factor_id: number
  name: string
  description: string
  base_weight: number
  current_weight: number
  min_weight: number
  max_weight: number
}

interface Analytics {
  total_predictions: number
  correct_predictions: number
  accuracy: number
  sample_size: number
}

export default function Dashboard() {
  const [factors, setFactors] = useState<Factor[]>([])
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)

      const [factorsRes, analyticsRes] = await Promise.all([
        axios.get(`${API_URL}/factors`),
        axios.get(`${API_URL}/analytics`),
      ])

      setFactors(factorsRes.data)
      setAnalytics(analyticsRes.data)
      setError('')
    } catch (err) {
      console.error('Error fetching dashboard data:', err)
      setError('Failed to load dashboard. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const getWeightChange = (base: number, current: number) => {
    const change = current - base
    const percentage = ((change / base) * 100).toFixed(1)
    const color = change > 0 ? 'text-green-400' : change < 0 ? 'text-red-400' : 'text-text-secondary'
    const sign = change > 0 ? '+' : ''

    return (
      <span className={`${color} font-semibold text-sm`}>
        {sign}
        {percentage}%
      </span>
    )
  }

  return (
    <div className="min-h-screen bg-dark-bg flex flex-col">
      <Header title="BetCheck" subtitle="Performance Metrics & Model Analysis" />

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <div className="inline-block">
                <div className="w-12 h-12 border-2 border-neon-pink border-t-transparent rounded-full animate-spin mb-4"></div>
              </div>
              <p className="text-text-secondary text-lg">Loading dashboard...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="border border-red-500/50 bg-red-500/10 mb-8">
            <div className="flex justify-between items-start gap-4">
              <div className="flex-1">
                <h3 className="text-red-400 font-bold mb-2">Error Loading Dashboard</h3>
                <p className="text-red-300 text-sm">{error}</p>
              </div>
              <Button
                variant="primary"
                size="sm"
                onClick={fetchData}
              >
                Retry
              </Button>
            </div>
          </Card>
        )}

        {!loading && !error && (
          <div className="space-y-10">
            {/* Analytics Section */}
            {analytics && (
              <div>
                <h2 className="text-3xl sm:text-4xl font-bold text-text-primary mb-8">
                  Prediction Accuracy
                </h2>

                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
                  {/* Total Predictions */}
                  <Card glowing={true}>
                    <p className="text-text-secondary text-xs uppercase tracking-widest mb-3">
                      Total Predictions
                    </p>
                    <p className="text-4xl font-bold text-text-primary mb-2">
                      {analytics.total_predictions}
                    </p>
                    <div className="border-t border-dark-border pt-3 mt-3">
                      <p className="text-text-secondary text-xs">Model Evaluations</p>
                    </div>
                  </Card>

                  {/* Correct Predictions */}
                  <Card glowing={true}>
                    <p className="text-text-secondary text-xs uppercase tracking-widest mb-3">
                      Correct Predictions
                    </p>
                    <p className="text-4xl font-bold text-neon-pink mb-2">
                      {analytics.correct_predictions}
                    </p>
                    <div className="border-t border-dark-border pt-3 mt-3">
                      <p className="text-text-secondary text-xs">Accurate Forecasts</p>
                    </div>
                  </Card>

                  {/* Accuracy Rate */}
                  <Card glowing={true}>
                    <p className="text-text-secondary text-xs uppercase tracking-widest mb-3">
                      Accuracy Rate
                    </p>
                    <p className="text-4xl font-bold text-neon-pink-light mb-2">
                      {analytics.accuracy.toFixed(1)}%
                    </p>
                    <div className="border-t border-dark-border pt-3 mt-3">
                      <p className="text-text-secondary text-xs">Success Rate</p>
                    </div>
                  </Card>

                  {/* Sample Size */}
                  <Card glowing={true}>
                    <p className="text-text-secondary text-xs uppercase tracking-widest mb-3">
                      Sample Size
                    </p>
                    <p className="text-4xl font-bold text-text-primary mb-2">
                      {analytics.sample_size}
                    </p>
                    <div className="border-t border-dark-border pt-3 mt-3">
                      <p className="text-text-secondary text-xs">Observations</p>
                    </div>
                  </Card>
                </div>

                {analytics.accuracy === 0 && (
                  <Card className="border-dashed border-2 border-neon-pink/30 bg-neon-pink/5">
                    <div className="flex gap-3">
                      <span className="text-2xl">📊</span>
                      <p className="text-text-secondary text-sm">
                        No completed games yet. Use the <code className="bg-dark-bg px-2 py-1 rounded text-neon-pink">/log_result</code> endpoint to record game results and improve the model.
                      </p>
                    </div>
                  </Card>
                )}
              </div>
            )}

            {/* Factors Section */}
            <div>
              <h2 className="text-3xl sm:text-4xl font-bold text-text-primary mb-8">
                Prediction Factors
              </h2>

              <div className="space-y-6">
                {factors.map((factor) => (
                  <Card key={factor.factor_id} glowing={true}>
                    <div className="flex flex-col sm:flex-row justify-between items-start gap-6 mb-6">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-text-primary mb-2">
                          {factor.name}
                        </h3>
                        <p className="text-text-secondary text-sm leading-relaxed">
                          {factor.description}
                        </p>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <p className="text-text-secondary text-xs uppercase tracking-widest mb-2">
                          Current Weight
                        </p>
                        <p className="text-3xl font-bold text-neon-pink mb-2">
                          {(factor.current_weight * 100).toFixed(1)}%
                        </p>
                        <div className="flex items-center justify-end gap-2">
                          <p className="text-text-secondary text-xs">
                            Base: {(factor.base_weight * 100).toFixed(1)}%
                          </p>
                          <div>{getWeightChange(factor.base_weight, factor.current_weight)}</div>
                        </div>
                      </div>
                    </div>

                    {/* Weight Range Visualization */}
                    <div className="border-t border-dark-border pt-6">
                      <div className="mb-3">
                        <p className="text-text-secondary text-xs uppercase tracking-widest mb-3">
                          Weight Range
                        </p>
                        <div className="relative">
                          {/* Background track */}
                          <div className="h-3 bg-dark-border rounded-full overflow-hidden">
                            {/* Allowed range highlight */}
                            <div
                              className="absolute top-0 h-3 bg-neon-pink/20 rounded-full"
                              style={{
                                left: `${(factor.min_weight / factor.max_weight) * 100}%`,
                                width: `${((factor.max_weight - factor.min_weight) / factor.max_weight) * 100}%`,
                              }}
                            />
                            
                            {/* Current weight bar */}
                            <div
                              className="h-3 bg-gradient-to-r from-neon-pink to-neon-pink-light rounded-full transition-all duration-500 shadow-neon-pink"
                              style={{
                                width: `${(factor.current_weight / factor.max_weight) * 100}%`,
                              }}
                            >
                              <div className="h-full bg-neon-pink animate-pulse opacity-70" />
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Range labels */}
                      <div className="flex justify-between text-xs text-text-secondary mt-3">
                        <span>Min: {(factor.min_weight * 100).toFixed(1)}%</span>
                        <span>Max: {(factor.max_weight * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>

            {/* Info Box */}
            <Card className="border-neon-pink/30 bg-neon-pink/5">
              <div className="flex gap-4">
                <span className="text-3xl">🧠</span>
                <div>
                  <p className="text-text-primary font-semibold mb-2">
                    Adaptive Learning Model
                  </p>
                  <p className="text-text-secondary text-sm leading-relaxed">
                    Factor weights automatically adjust based on prediction accuracy. When predictions are correct, contributing factors increase in weight. When predictions are incorrect, factors decrease. This allows the model to learn which factors are most predictive over time, ensuring continuous improvement of forecast accuracy.
                  </p>
                </div>
              </div>
            </Card>
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
