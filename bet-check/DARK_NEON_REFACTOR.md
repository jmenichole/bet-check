# Dark Neon Theme Refactor - BetCheck Frontend

## Overview

The BetCheck frontend has been completely refactored to feature a **dark neon theme** with a sophisticated B-mode sports prediction aesthetic. The design emphasizes visual polish while maintaining simplicity and readability.

## 🎨 Design System

### Color Palette
- **Dark Background**: `#0d0d0d` (near black)
- **Card Background**: `#1a1a1a`
- **Border Color**: `#2a2a2a`
- **Neon Pink**: `#ff00cc` (primary accent)
- **Neon Pink Light**: `#ff33dd` (hover states)
- **Neon Pink Dark**: `#cc0099` (active states)
- **Text Primary**: `#ffffff` (white)
- **Text Secondary**: `#b0b0b0` (light gray)

### Visual Effects
- **Neon Glow**: Cards have subtle pink glow with inset lighting
- **Animated Pulse**: Confidence meters and factor weights pulse with neon glow
- **Hover States**: Interactive elements brighten and glow on hover
- **Custom Scrollbar**: Neon pink scrollbar with glow effect
- **Smooth Transitions**: 300ms easing on all interactive elements

## 📦 Reusable Components

### 1. Card Component (`components/Card.tsx`)
Flexible, glowing card container with optional click handlers.

**Features:**
- Neon pink border glow
- Configurable glow intensity
- Smooth hover transitions
- Responsive padding

**Usage:**
```tsx
<Card glowing={true} onClick={handleClick}>
  Content here
</Card>
```

### 2. Button Component (`components/Button.tsx`)
Stylized button with multiple variants and sizes.

**Variants:**
- `primary`: Solid neon pink background
- `secondary`: Outlined with neon pink
- `outline`: Transparent with pink border

**Sizes:** `sm`, `md`, `lg`

**Features:**
- Glow effect on hover (optional)
- Disabled state styling
- Configurable className override

**Usage:**
```tsx
<Button variant="primary" size="lg" glow={true}>
  Click Me
</Button>
```

### 3. ConfidenceMeter Component (`components/ConfidenceMeter.tsx`)
Animated confidence meter with neon glow and pulse effects.

**Features:**
- Animated progress bar
- Percentage display in neon pink
- Pulsing animation
- Three sizes: `sm`, `md`, `lg`
- Glowing edge effects

**Usage:**
```tsx
<ConfidenceMeter confidence={0.85} size="lg" />
```

### 4. ReasonItem Component (`components/ReasonItem.tsx`)
Reason display with neon bullet points and rotating icons.

**Features:**
- Dynamic icon rotation (⚡ 📊 🏆 💯 🎯)
- Neon bullet point with glow
- Hover state with icon transformation
- Smooth transitions

**Usage:**
```tsx
<ReasonItem reason="Team has strong recent form" index={0} />
```

### 5. Header Component (`components/Header.tsx`)
Sticky navigation header with logo and links.

**Features:**
- Sticky positioning with backdrop blur
- Logo animation on hover
- Navigation with hover effects
- Responsive design

**Usage:**
```tsx
<Header title="BetCheck" subtitle="Sports Prediction Engine" />
```

## 📄 Refactored Pages

### 1. Home Page (`pages/index.tsx`)
**Displays:** List of upcoming games with predictions

**Updates:**
- Dark background with neon accents
- Game cards with hover scale effect
- Sport badges with neon styling
- Loading spinner with neon border
- Error handling with retry button
- Responsive grid layout (1, 2, or 3 columns)

**Key Elements:**
- Header component integration
- Reusable Card component
- Neon pink button styling
- Formatted dates with improved readability

### 2. Game Prediction Page (`pages/game/[gameId].tsx`)
**Displays:** Detailed prediction analysis for selected game

**Updates:**
- Large, centered team names
- Predicted winner highlighted in neon pink with pulse
- ConfidenceMeter component for visual representation
- ReasonItem components for explanation
- Factor analysis with animated progress bars
- Information card explaining adaptive learning

**Key Elements:**
- Full-width layout
- Pulsing predicted outcome
- Animated factor contribution bars
- Back navigation button
- Responsive grid for team comparison

### 3. Dashboard Page (`pages/dashboard.tsx`)
**Displays:** Model analytics and factor weight adjustments

**Updates:**
- Four metric cards: total predictions, correct, accuracy rate, sample size
- Neon pink highlighting for key metrics
- Factor cards with weight visualization
- Animated progress bars showing weight ranges
- Color-coded weight change indicators (green for +, red for -)
- Adaptive learning explanation card

**Key Elements:**
- Analytics grid (responsive 1-4 columns)
- Individual factor cards with detailed info
- Weight change percentage display
- Range visualization with allowed bounds
- Educational content cards

## 🎯 Design Features

### Neon Glow Effects
```css
box-shadow: 0 0 10px rgba(255, 0, 204, 0.5), inset 0 0 10px rgba(255, 0, 204, 0.1);
```

### Text Shadows
Subtle glow effect on interactive text:
```css
text-shadow: 0 0 10px rgba(255, 0, 204, 0.5);
```

### Animations
- **Pulse**: Used on confidence meters and predictions
- **Spin**: Loading indicator with neon border
- **Glow**: Box shadow animation on cards
- **Glitch**: CSS animation for edge effects

### Responsive Design
- Mobile: Single column layouts
- Tablet: 2-column grids
- Desktop: 3-4 column grids
- Flexible spacing and padding

## 🔧 Configuration

### Tailwind Config (`tailwind.config.ts`)
Extended theme with custom colors and shadows:
```typescript
colors: {
  'neon-pink': '#ff00cc',
  'neon-pink-light': '#ff33dd',
  'neon-pink-dark': '#cc0099',
  'dark-bg': '#0d0d0d',
  'dark-card': '#1a1a1a',
  'dark-border': '#2a2a2a',
  'text-primary': '#ffffff',
  'text-secondary': '#b0b0b0',
}

boxShadow: {
  'neon-pink': '0 0 10px rgba(255, 0, 204, 0.5), inset 0 0 10px rgba(255, 0, 204, 0.1)',
  'neon-pink-lg': '0 0 20px rgba(255, 0, 204, 0.6), inset 0 0 20px rgba(255, 0, 204, 0.15)',
  'glow-pink': '0 0 30px rgba(255, 0, 204, 0.4)',
}
```

### Global Styles (`styles/globals.css`)
- Dark background applied to body
- Custom scrollbar with neon styling
- Neon glow and glitch animations
- Smooth transition utilities

## 📱 Responsive Breakpoints

Using Tailwind's responsive prefixes:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

All components adapt seamlessly across breakpoints.

## 🚀 Running the Application

### Backend (FastAPI)
```bash
cd backend
source venv/bin/activate
python main.py
# Running on port 9001
```

### Frontend (Next.js)
```bash
cd frontend
npm run dev
# Running on port 3001
```

Access the application at: **http://localhost:3001**

## 📊 Component Structure

```
frontend/
├── pages/
│   ├── index.tsx           # Home - Games list
│   ├── dashboard.tsx       # Dashboard - Metrics
│   └── game/
│       └── [gameId].tsx    # Prediction - Game details
├── components/
│   ├── Button.tsx          # Reusable button
│   ├── Card.tsx            # Reusable card container
│   ├── ConfidenceMeter.tsx # Confidence visualization
│   ├── Header.tsx          # Navigation header
│   └── ReasonItem.tsx      # Reason display
├── styles/
│   └── globals.css         # Global styles & animations
├── tailwind.config.ts      # Tailwind theme config
└── next.config.js          # Next.js config
```

## 🎨 Design Principles

1. **Dark First**: All backgrounds are dark to reduce eye strain
2. **Neon Accents**: Neon pink used sparingly for key information
3. **Readable**: High contrast between text and background
4. **Interactive**: Clear hover and active states
5. **Polished**: Smooth animations and transitions
6. **B-Mode Simple**: No unnecessary complexity
7. **Responsive**: Works seamlessly on all devices

## 💡 Key Features

✅ Dark neon theme with pink accents
✅ Animated confidence meters with glow effects
✅ Reusable, composable components
✅ Smooth transitions and hover states
✅ Responsive design for all screen sizes
✅ Readable text with high contrast
✅ Animated loading states
✅ Error handling with retry buttons
✅ Factor analysis with visual bars
✅ Adaptive learning explanation cards

## 📝 Notes

- All color values are Tailwind utilities defined in `tailwind.config.ts`
- Animations are defined in `styles/globals.css`
- Components use TypeScript for type safety
- Responsive design uses Tailwind breakpoints
- API integration matches backend on port 9001
- Error states provide clear feedback to users

---

**Design completed:** December 11, 2025
**Status:** ✅ Production Ready
