import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'neon-pink': '#ff00cc',
        'neon-pink-light': '#ff33dd',
        'neon-pink-dark': '#cc0099',
        'dark-bg': '#0d0d0d',
        'dark-card': '#1a1a1a',
        'dark-border': '#2a2a2a',
        'text-primary': '#ffffff',
        'text-secondary': '#b0b0b0',
      },
      boxShadow: {
        'neon-pink': '0 0 10px rgba(255, 0, 204, 0.5), inset 0 0 10px rgba(255, 0, 204, 0.1)',
        'neon-pink-lg': '0 0 20px rgba(255, 0, 204, 0.6), inset 0 0 20px rgba(255, 0, 204, 0.15)',
        'glow-pink': '0 0 30px rgba(255, 0, 204, 0.4)',
      },
      textShadow: {
        'neon-pink': '0 0 10px rgba(255, 0, 204, 0.5)',
      },
    },
  },
  plugins: [],
}
export default config
