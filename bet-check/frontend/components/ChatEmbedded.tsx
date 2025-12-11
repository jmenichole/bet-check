/**
 * AI Sports Guru - Embedded Chat Component
 * Displays an embedded chat interface at the top of the page
 * with scrollable history and intelligent game suggestions
 * 
 * Copyright (c) 2025 Jmenichole
 * Licensed under CC BY-NC 4.0
 * https://jmenichole.github.io/Portfolio/
 */

import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL

interface Message {
  id: string
  text: string
  isAI: boolean
  timestamp: string
  suggestedGames?: any[]
}

export default function ChatEmbedded() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load welcome message on mount
  useEffect(() => {
    setMessages([
      {
        id: 'welcome',
        text: "👋 Hey! I'm your AI Sports Guru. Ask me about upcoming games, and I'll suggest the best bets with predictions!",
        isAI: true,
        timestamp: new Date().toISOString()
      }
    ])
  }, [])

  const handleSendMessage = async () => {
    if (!inputText.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isAI: false,
      timestamp: new Date().toISOString()
    }

    // Add user message to chat
    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setLoading(true)

    try {
      // Send to AI endpoint
      const response = await axios.post(`${API_URL}/chat`, {
        message: inputText,
        user_id: 'anonymous'
      })

      // Add AI response
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.ai_message,
        isAI: true,
        timestamp: response.data.timestamp,
        suggestedGames: response.data.suggested_games
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      console.error('Chat error:', error)
      
      // Add error message
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        text: "Oops! I'm having trouble connecting right now. Make sure the backend is running!",
        isAI: true,
        timestamp: new Date().toISOString()
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="w-full bg-[#0d0d0d] rounded-lg border border-[#ff00cc]/20 shadow-lg shadow-[#ff00cc]/10">
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-[#ff00cc]/20 to-[#00ffff]/20 p-4 rounded-t-lg border-b border-[#ff00cc]/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#ff00cc] to-[#00ffff] flex items-center justify-center">
            <span className="text-2xl">🤖</span>
          </div>
          <div>
            <h3 className="text-white font-bold text-lg">AI Sports Guru</h3>
            <p className="text-gray-400 text-xs">Ask me anything about sports betting</p>
          </div>
        </div>
      </div>

      {/* Chat Messages Area - Scrollable */}
      <div className="h-[400px] overflow-y-auto p-4 space-y-4 custom-scrollbar">
        {messages.map((message) => (
          <div key={message.id}>
            {/* Message Bubble */}
            <div className={`flex ${message.isAI ? 'justify-start' : 'justify-end'} mb-2`}>
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  message.isAI
                    ? 'bg-[#ff00cc]/20 border border-[#ff00cc]/40 shadow-lg shadow-[#ff00cc]/20'
                    : 'bg-white/10 border border-white/20'
                }`}
              >
                <p className="text-white text-sm leading-relaxed">{message.text}</p>
                <p className="text-gray-500 text-xs mt-1">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </p>
              </div>
            </div>

            {/* Suggested Games Cards */}
            {message.suggestedGames && message.suggestedGames.length > 0 && (
              <div className="mt-3 space-y-2">
                {message.suggestedGames.map((game) => (
                  <a
                    key={game.game_id}
                    href={`/game/${game.game_id}`}
                    className="block bg-[#1a1a1a] border border-[#00ffff]/30 rounded-lg p-3 hover:border-[#00ffff] hover:shadow-lg hover:shadow-[#00ffff]/30 transition-all duration-300 cursor-pointer"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="text-[#00ffff] font-bold text-sm mb-1">
                          {game.sport.toUpperCase()}
                        </div>
                        <div className="text-white font-semibold">
                          {game.team_a} vs {game.team_b}
                        </div>
                        <div className="text-gray-400 text-xs mt-1">
                          {new Date(game.scheduled_date).toLocaleDateString()}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-[#ff00cc] font-bold text-lg">
                          {game.confidence}%
                        </div>
                        <div className="text-xs text-gray-400">confidence</div>
                      </div>
                    </div>
                    <div className="mt-2 pt-2 border-t border-gray-700">
                      <div className="text-white text-sm">
                        <strong>Prediction:</strong> {game.predicted_outcome}
                      </div>
                      {game.reasoning && game.reasoning.length > 0 && (
                        <div className="text-gray-400 text-xs mt-1">
                          💡 {game.reasoning[0]}
                        </div>
                      )}
                    </div>
                  </a>
                ))}
              </div>
            )}
          </div>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-[#ff00cc]/20 border border-[#ff00cc]/40 rounded-lg p-3">
              <div className="flex gap-2">
                <div className="w-2 h-2 bg-[#ff00cc] rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-[#ff00cc] rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-2 h-2 bg-[#ff00cc] rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-[#ff00cc]/30 bg-[#0d0d0d]">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about games, predictions, or best bets..."
            className="flex-1 bg-[#1a1a1a] border border-[#ff00cc]/30 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-[#ff00cc] focus:shadow-lg focus:shadow-[#ff00cc]/20 transition-all"
            disabled={loading}
          />
          <button
            onClick={handleSendMessage}
            disabled={loading || !inputText.trim()}
            className="bg-gradient-to-r from-[#ff00cc] to-[#00ffff] text-white px-6 py-3 rounded-lg font-bold hover:shadow-lg hover:shadow-[#ff00cc]/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
          >
            Send
          </button>
        </div>
      </div>

      {/* Custom scrollbar styles */}
      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #1a1a1a;
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #ff00cc;
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #00ffff;
        }
      `}</style>
    </div>
  )
}
