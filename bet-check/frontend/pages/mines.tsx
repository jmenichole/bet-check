/**
 * Mines Game Page - Interactive mines game with AI predictions
 * 
 * Copyright (c) 2025 Jmenichole
 * Licensed under MIT License
 */

import axios from 'axios'
import { useEffect, useState } from 'react'
import Header from '@/components/Header'
import Card from '@/components/Card'
import Button from '@/components/Button'

const API_URL = process.env.NEXT_PUBLIC_API_URL
const GRID_CONFIGS: Record<number, { defaultBombs: number; min: number; max: number }> = {
  5: { defaultBombs: 3, min: 1, max: 10 },
  6: { defaultBombs: 5, min: 2, max: 14 },
  8: { defaultBombs: 8, min: 4, max: 26 },
  10: { defaultBombs: 15, min: 6, max: 40 },
}

interface MinesTile {
  x: number
  y: number
  revealed: boolean
  is_bomb: boolean
}

interface Prediction {
  x: number
  y: number
  safe_probability: number
  confidence: number
  recommendation: string
}

export default function Mines() {
  const [gameId, setGameId] = useState<string>('')
  const [gridSize, setGridSize] = useState(5)
  const [numBombs, setNumBombs] = useState(GRID_CONFIGS[5].defaultBombs)
  const [grid, setGrid] = useState<MinesTile[][]>([])
  const [predictions, setPredictions] = useState<Prediction[]>([])
  const [gameStats, setGameStats] = useState({ safe_clicks: 0, bombs_hit: 0, total_clicks: 0, bombs_remaining: GRID_CONFIGS[5].defaultBombs, remaining_safe: (5 * 5) - GRID_CONFIGS[5].defaultBombs })
  const [gameStatus, setGameStatus] = useState('idle') // idle, active, completed, busted
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const preset = GRID_CONFIGS[gridSize]
    const nextBombs = preset ? preset.defaultBombs : Math.max(1, Math.floor((gridSize * gridSize) * 0.2))
    setNumBombs(nextBombs)
    setGameStats((prev) => ({
      ...prev,
      bombs_remaining: nextBombs,
      remaining_safe: (gridSize * gridSize) - nextBombs,
    }))
  }, [gridSize])

  // Initialize new game
  const startNewGame = async () => {
    try {
      setLoading(true)
      setError('')
      console.log('Starting game with API_URL:', API_URL)
      const response = await axios.post(`${API_URL}/mines/game/create`, null, {
        params: { grid_size: gridSize, num_bombs: numBombs }
      })
      
      const newGameId = response.data.game_id
      const confirmedBombs = response.data.num_bombs ?? numBombs
      setGameId(newGameId)
      setNumBombs(confirmedBombs)
      setGameStatus('active')
      
      // Initialize empty grid
      const newGrid: MinesTile[][] = []
      for (let i = 0; i < gridSize; i++) {
        const row: MinesTile[] = []
        for (let j = 0; j < gridSize; j++) {
          row.push({ x: j, y: i, revealed: false, is_bomb: false })
        }
        newGrid.push(row)
      }
      setGrid(newGrid)
      
      // Get initial predictions
      await fetchPredictions(newGameId)
      setGameStats({
        safe_clicks: 0,
        bombs_hit: 0,
        total_clicks: 0,
        bombs_remaining: confirmedBombs,
        remaining_safe: (gridSize * gridSize) - confirmedBombs,
      })
    } catch (err) {
      console.error('Error starting game:', err)
      setError('Unable to start a new game. Please ensure the backend is running and try again.')
    } finally {
      setLoading(false)
    }
  }

  const fetchPredictions = async (id: string) => {
    try {
      const response = await axios.post(`${API_URL}/mines/predict/${id}`)
      setPredictions(response.data.tiles)
    } catch (err) {
      console.error('Error fetching predictions:', err)
    }
  }

  const clickTile = async (x: number, y: number) => {
    if (!gameId || grid[y][x].revealed) return
    
    try {
      setLoading(true)
      setError('')
      
      // In demo mode, randomly determine if tile is safe
      const is_safe = Math.random() > 0.3
      
      const response = await axios.post(`${API_URL}/mines/click/${gameId}`, null, {
        params: { x, y, is_safe }
      })
      
      // Update grid
      const newGrid = grid.map(row => [...row])
      newGrid[y][x].revealed = true
      newGrid[y][x].is_bomb = !is_safe
      setGrid(newGrid)
      
      // Update stats
      const stats = response.data.stats || {}
      setGameStats({
        safe_clicks: stats.safe_clicks ?? gameStats.safe_clicks,
        bombs_hit: stats.bombs_hit ?? gameStats.bombs_hit,
        total_clicks: stats.total_clicks ?? gameStats.total_clicks,
        bombs_remaining: stats.bombs_remaining ?? Math.max(numBombs - (stats.bombs_hit ?? 0), 0),
        remaining_safe: stats.remaining_safe ?? Math.max((gridSize * gridSize) - numBombs - (stats.safe_clicks ?? 0), 0),
      })
      
      // Update game status
      if (!is_safe) {
        setGameStatus('busted')
      }
      
      // Fetch new predictions
      await fetchPredictions(gameId)
    } catch (err) {
      console.error('Error clicking tile:', err)
    } finally {
      setLoading(false)
    }
  }

  const getTileColor = (tile: MinesTile, pred: Prediction | null) => {
    if (!tile.revealed) {
      if (pred && pred.safe_probability > 0.7) return 'bg-green-500/20 border-green-500/50 hover:bg-green-500/30'
      if (pred && pred.safe_probability < 0.4) return 'bg-red-500/20 border-red-500/50 hover:bg-red-500/30'
      return 'bg-gray-700/20 border-gray-500/50 hover:bg-gray-600/30'
    }
    return tile.is_bomb ? 'bg-red-600 border-red-400' : 'bg-green-600 border-green-400'
  }

  const getTileIcon = (tile: MinesTile) => {
    if (!tile.revealed) return '?'
    return tile.is_bomb ? '💣' : '✓'
  }

  return (
    <div className="min-h-screen bg-dark-bg flex flex-col">
      <Header title="Mines" subtitle="AI-Powered Tile Prediction Game" />

      <main className="flex-1 max-w-6xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
        {error && (
          <Card className="mb-6 border border-red-500/50 bg-red-500/10">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3 className="text-red-400 font-bold mb-1">Something went wrong</h3>
                <p className="text-red-200 text-sm">{error}</p>
              </div>
              <Button variant="primary" size="sm" onClick={startNewGame}>Retry</Button>
            </div>
          </Card>
        )}

        {/* Game Setup */}
        {!gameId && (
          <Card className="mb-8">
            <h2 className="text-2xl font-bold text-text-primary mb-4">Start a New Game</h2>
            <div className="flex flex-col sm:flex-row gap-4 items-end">
              <div>
                <label className="block text-sm font-semibold text-text-secondary mb-2">
                  Grid Size
                </label>
                <select
                  value={gridSize}
                  onChange={(e) => setGridSize(Number(e.target.value))}
                  className="px-4 py-2 bg-dark-bg border border-neon-pink/30 rounded text-text-primary"
                >
                  <option value={5}>5x5 (3 bombs)</option>
                  <option value={6}>6x6 (5 bombs)</option>
                  <option value={8}>8x8 (8 bombs)</option>
                  <option value={10}>10x10 (15 bombs)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold text-text-secondary mb-2">
                  Bombs
                </label>
                <input
                  type="number"
                  min={GRID_CONFIGS[gridSize]?.min ?? 1}
                  max={GRID_CONFIGS[gridSize]?.max ?? (gridSize * gridSize - 1)}
                  value={numBombs}
                  onChange={(e) => {
                    const raw = Number(e.target.value)
                    const min = GRID_CONFIGS[gridSize]?.min ?? 1
                    const max = GRID_CONFIGS[gridSize]?.max ?? (gridSize * gridSize - 1)
                    const clamped = Math.min(Math.max(raw, min), max)
                    setNumBombs(clamped)
                  }}
                  className="px-4 py-2 w-32 bg-dark-bg border border-neon-pink/30 rounded text-text-primary"
                />
                <p className="text-xs text-text-secondary mt-1">
                  Allowed: {GRID_CONFIGS[gridSize]?.min ?? 1} – {GRID_CONFIGS[gridSize]?.max ?? (gridSize * gridSize - 1)} | Default: {GRID_CONFIGS[gridSize]?.defaultBombs ?? Math.max(1, Math.floor((gridSize * gridSize) * 0.2))}
                </p>
              </div>
              <Button
                variant="primary"
                onClick={startNewGame}
                disabled={loading}
              >
                {loading ? 'Starting...' : 'Start Game'}
              </Button>
            </div>
          </Card>
        )}

        {/* Active Game */}
        {gameId && (
          <div className="space-y-8">
            {/* Stats */}
            <Card className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <p className="text-text-secondary text-sm mb-1">Safe Clicks</p>
                <p className="text-2xl font-bold text-green-400">{gameStats.safe_clicks}</p>
              </div>
              <div className="text-center">
                <p className="text-text-secondary text-sm mb-1">Bombs Hit</p>
                <p className="text-2xl font-bold text-red-400">{gameStats.bombs_hit}</p>
              </div>
              <div className="text-center">
                <p className="text-text-secondary text-sm mb-1">Bombs Remaining</p>
                <p className="text-2xl font-bold text-white">{gameStats.bombs_remaining}</p>
              </div>
              <div className="text-center">
                <p className="text-text-secondary text-sm mb-1">Status</p>
                <p className={`text-2xl font-bold ${gameStatus === 'busted' ? 'text-red-400' : 'text-green-400'}`}>
                  {gameStatus === 'busted' ? 'BUSTED' : 'ACTIVE'}
                </p>
              </div>
            </Card>

            {/* Game Grid */}
            <Card>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-text-primary">Game Grid</h2>
                <div className="text-sm text-text-secondary">
                  💡 Tip: Green = Safer, Red = Riskier
                </div>
              </div>
              <div className={`inline-grid gap-2 p-4 bg-dark-bg/50 rounded-lg`} style={{ gridTemplateColumns: `repeat(${gridSize}, minmax(0, 1fr))` }}>
                {grid.map((row, y) =>
                  row.map((tile, x) => {
                    const pred = predictions.find(p => p.x === x && p.y === y)
                    const isTopPick = pred && predictions.slice(0, 3).some(p => p.x === x && p.y === y)
                    return (
                      <button
                        key={`${x}-${y}`}
                        onClick={() => clickTile(x, y)}
                        disabled={tile.revealed || gameStatus === 'busted'}
                        className={`
                          w-12 h-12 rounded border transition-all font-bold text-lg relative
                          disabled:cursor-not-allowed
                          ${getTileColor(tile, pred)}
                          ${!tile.revealed && gameStatus !== 'busted' ? 'cursor-pointer hover:scale-105' : ''}
                          ${isTopPick && !tile.revealed ? 'ring-2 ring-green-400 ring-offset-2 ring-offset-dark-bg animate-pulse' : ''}
                        `}
                        title={pred ? `Safe: ${(pred.safe_probability * 100).toFixed(0)}%` : ''}
                      >
                        {getTileIcon(tile)}
                        {isTopPick && !tile.revealed && (
                          <span className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full text-white text-xs flex items-center justify-center">
                            ✓
                          </span>
                        )}
                      </button>
                    )
                  })
                )}
              </div>
            </Card>

            {/* AI Predictions - Simplified Top 3 */}
            <Card>
              <div className="flex items-center gap-2 mb-4">
                <span className="text-2xl">🤖</span>
                <h2 className="text-xl font-bold text-text-primary">AI Says: Click These Next</h2>
              </div>
              <p className="text-text-secondary text-sm mb-4">Top 3 safest tiles based on probability analysis</p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {predictions.slice(0, 3).map((pred, idx) => (
                  <button
                    key={idx}
                    onClick={() => clickTile(pred.x, pred.y)}
                    disabled={gameStatus === 'busted'}
                    className="relative p-6 rounded-lg border-2 border-green-500/50 bg-gradient-to-br from-green-500/10 to-green-500/5 hover:border-green-400 hover:shadow-lg hover:shadow-green-500/30 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed group"
                  >
                    {/* Rank Badge */}
                    <div className="absolute top-2 left-2 w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold text-sm">
                      #{idx + 1}
                    </div>
                    
                    {/* Tile Position - Large & Clear */}
                    <div className="text-center mb-3 mt-4">
                      <div className="text-5xl font-bold text-green-400 group-hover:scale-110 transition-transform">
                        ({pred.x}, {pred.y})
                      </div>
                      <div className="text-xs text-text-secondary mt-1">Row {pred.y}, Col {pred.x}</div>
                    </div>
                    
                    {/* Safety Score */}
                    <div className="text-center">
                      <div className="text-3xl font-bold text-white mb-1">
                        {(pred.safe_probability * 100).toFixed(0)}%
                      </div>
                      <div className="text-xs text-green-400 font-semibold uppercase tracking-wide">
                        {pred.recommendation === 'SAFE' ? '✓ Safe Bet' : 'Consider'}
                      </div>
                    </div>
                    
                    {/* Visual Bar */}
                    <div className="mt-4 h-2 bg-dark-bg rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-green-500 to-green-300 transition-all duration-500"
                        style={{ width: `${pred.safe_probability * 100}%` }}
                      ></div>
                    </div>
                    
                    {/* Click Hint */}
                    <div className="mt-3 text-center text-xs text-text-secondary opacity-0 group-hover:opacity-100 transition-opacity">
                      Click to reveal this tile
                    </div>
                  </button>
                ))}
              </div>
              
              {predictions.length === 0 && (
                <div className="text-center py-8 text-text-secondary">
                  Start clicking tiles to get AI recommendations!
                </div>
              )}
            </Card>

            {/* Game Over */}
            {gameStatus === 'busted' && (
              <Card className="border border-red-500/50 bg-red-500/10">
                <h3 className="text-xl font-bold text-red-400 mb-4">Game Over!</h3>
                <p className="text-text-secondary mb-4">
                  You hit a bomb! Final score: {gameStats.safe_clicks} safe clicks
                </p>
                <Button variant="primary" onClick={startNewGame}>
                  Play Again
                </Button>
              </Card>
            )}

            <Button variant="secondary" onClick={startNewGame}>
              New Game
            </Button>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-dark-border mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
          <p className="text-text-secondary text-sm">
            Mines Game with AI Predictions © 2025
          </p>
        </div>
      </footer>
    </div>
  )
}
