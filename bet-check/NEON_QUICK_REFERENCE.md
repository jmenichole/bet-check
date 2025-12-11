# Dark Neon Theme Quick Reference

## 🎨 Color Palette

```css
/* Dark Mode Colors */
--bg-dark: #0d0d0d;      /* Main background */
--card-dark: #1a1a1a;    /* Card background */
--border-dark: #2a2a2a;  /* Borders */

/* Neon Accent Colors */
--neon-pink: #ff00cc;       /* Primary accent */
--neon-pink-light: #ff33dd; /* Hover state */
--neon-pink-dark: #cc0099;  /* Active state */

/* Text Colors */
--text-primary: #ffffff;  /* Main text */
--text-secondary: #b0b0b0; /* Secondary text */
```

## 🧩 Component Usage Examples

### Card Component
```tsx
import Card from '@/components/Card'

// Basic card
<Card>
  <p>Content here</p>
</Card>

// Glowing card
<Card glowing={true}>
  <p>Highlighted content</p>
</Card>

// Clickable card
<Card onClick={() => navigate('/')}>
  <p>Click me</p>
</Card>
```

### Button Component
```tsx
import Button from '@/components/Button'

// Primary button
<Button variant="primary" size="md">
  Click Me
</Button>

// Secondary button
<Button variant="secondary" size="lg" glow={true}>
  View Details
</Button>

// Outline button
<Button variant="outline" size="sm">
  Cancel
</Button>
```

### ConfidenceMeter Component
```tsx
import ConfidenceMeter from '@/components/ConfidenceMeter'

// Display confidence
<ConfidenceMeter confidence={0.85} size="lg" />
```

### ReasonItem Component
```tsx
import ReasonItem from '@/components/ReasonItem'

// Display reason with icon
<ReasonItem 
  reason="Team has strong recent form" 
  index={0}
/>
```

### Header Component
```tsx
import Header from '@/components/Header'

// Page header
<Header 
  title="BetCheck" 
  subtitle="Sports Prediction Engine"
/>
```

## 🎯 Tailwind Utilities

### Neon Colors
```tsx
// Text colors
<p className="text-neon-pink">Neon Text</p>
<p className="text-neon-pink-light">Light Neon</p>

// Background
<div className="bg-dark-bg">Dark background</div>
<div className="bg-dark-card">Card background</div>

// Borders
<div className="border border-dark-border">Border</div>
<div className="border border-neon-pink">Neon border</div>
```

### Shadow Effects
```tsx
// Neon glow
<div className="shadow-neon-pink">Glow effect</div>

// Large glow
<div className="shadow-neon-pink-lg">Large glow</div>

// Color glow
<div className="shadow-glow-pink">Pink glow</div>
```

### Responsive Classes
```tsx
// Single column on mobile, 3 on desktop
<div className="grid md:grid-cols-3">
  {/* Content */}
</div>

// Text sizing
<h1 className="text-2xl sm:text-3xl md:text-4xl">
  Heading
</h1>

// Padding responsive
<div className="px-4 sm:px-6 lg:px-8">
  Content
</div>
```

## 🎬 Common Animations

### Pulse
```tsx
<div className="animate-pulse">
  Pulsing element
</div>
```

### Scale on Hover
```tsx
<div className="hover:scale-105 transition-transform duration-300">
  Hover to scale
</div>
```

### Color Transition
```tsx
<div className="text-text-secondary hover:text-neon-pink transition-colors duration-300">
  Hover to change color
</div>
```

### Spinning
```tsx
<div className="animate-spin border-2 border-neon-pink border-t-transparent rounded-full">
  Loading...
</div>
```

## 📱 Layout Patterns

### Full-Width Page
```tsx
<div className="min-h-screen bg-dark-bg flex flex-col">
  <Header title="Page Title" />
  
  <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
    {/* Content */}
  </main>
  
  <footer className="border-t border-dark-border">
    {/* Footer */}
  </footer>
</div>
```

### Grid Layout
```tsx
<div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
  {items.map((item) => (
    <Card key={item.id}>
      {item.content}
    </Card>
  ))}
</div>
```

### Flexbox Layout
```tsx
<div className="flex flex-col sm:flex-row justify-between items-center gap-4">
  <div>Left content</div>
  <div>Right content</div>
</div>
```

## 🎨 Typography

### Headings
```tsx
// Large heading
<h1 className="text-3xl sm:text-4xl font-bold text-text-primary">
  Title
</h1>

// Medium heading
<h2 className="text-2xl font-bold text-text-primary">
  Subtitle
</h2>

// Small heading
<h3 className="text-lg font-semibold text-text-primary">
  Section
</h3>
```

### Text Styles
```tsx
// Primary text
<p className="text-text-primary">Main text</p>

// Secondary text
<p className="text-text-secondary">Helper text</p>

// Accent text
<p className="text-neon-pink font-semibold">Important</p>

// Small text
<p className="text-sm text-text-secondary">Caption</p>

// Uppercase
<p className="text-xs uppercase tracking-widest">Label</p>
```

## 🔧 Common Patterns

### Loading State
```tsx
{loading && (
  <div className="flex items-center justify-center py-20">
    <div className="w-12 h-12 border-2 border-neon-pink border-t-transparent rounded-full animate-spin" />
  </div>
)}
```

### Error State
```tsx
{error && (
  <Card className="border border-red-500/50 bg-red-500/10">
    <h3 className="text-red-400 font-bold mb-2">Error</h3>
    <p className="text-red-300 text-sm">{error}</p>
    <Button variant="primary" size="sm" onClick={retry}>
      Retry
    </Button>
  </Card>
)}
```

### Empty State
```tsx
{items.length === 0 && (
  <Card className="border-dashed border-2 border-neon-pink/30 text-center py-12">
    <p className="text-text-secondary">No items found</p>
  </Card>
)}
```

### Info Box
```tsx
<Card className="border-neon-pink/30 bg-neon-pink/5">
  <div className="flex gap-4">
    <span className="text-2xl">ℹ️</span>
    <div>
      <p className="text-text-primary font-semibold mb-2">
        Title
      </p>
      <p className="text-text-secondary text-sm">
        Description text
      </p>
    </div>
  </div>
</Card>
```

## 🎯 Interactive Examples

### Game Card
```tsx
<Link href={`/game/${gameId}`}>
  <Card glowing={true} className="cursor-pointer group hover:scale-105">
    <div className="flex justify-end mb-4">
      <span className="bg-neon-pink bg-opacity-20 text-neon-pink text-xs font-bold px-3 py-1 rounded-full border border-neon-pink">
        {sport.toUpperCase()}
      </span>
    </div>
    <h3 className="text-xl font-bold text-text-primary group-hover:text-neon-pink">
      {teamA} vs {teamB}
    </h3>
  </Card>
</Link>
```

### Metric Card
```tsx
<Card glowing={true}>
  <p className="text-text-secondary text-xs uppercase tracking-widest mb-3">
    Total Predictions
  </p>
  <p className="text-4xl font-bold text-neon-pink mb-2">
    {count}
  </p>
  <div className="border-t border-dark-border pt-3 mt-3">
    <p className="text-text-secondary text-xs">Evaluations</p>
  </div>
</Card>
```

### Factor Card with Progress
```tsx
<Card glowing={true}>
  <h3 className="text-lg font-bold text-text-primary mb-4">
    {factorName}
  </h3>
  <div className="h-3 bg-dark-border rounded-full overflow-hidden">
    <div
      className="h-full bg-gradient-to-r from-neon-pink to-neon-pink-light shadow-neon-pink"
      style={{ width: `${percentage}%` }}
    />
  </div>
  <p className="text-neon-pink font-bold text-sm mt-2">
    {percentage.toFixed(1)}%
  </p>
</Card>
```

## 📚 Quick Links

- **Components**: `/frontend/components/`
- **Pages**: `/frontend/pages/`
- **Styles**: `/frontend/styles/globals.css`
- **Config**: `/frontend/tailwind.config.ts`

## 🚀 Deploy & Build

```bash
# Development
cd frontend && npm run dev

# Production build
npm run build
npm start

# Lint check
npm run lint
```

---

**Version**: 1.0
**Last Updated**: December 11, 2025
**Status**: ✅ Production Ready
