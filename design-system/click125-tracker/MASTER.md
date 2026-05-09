# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** Click125 Tracker
**Generated:** 2026-05-09
**Category:** Personal Utility / Mobile Tracker (Motorcycle Maintenance)
**Stack:** SvelteKit (Svelte 5)

---

## Hard Overrides (Non-Negotiable)

These override anything the design system generator suggested:

- **Theme**: Dark only (no light mode)
- **Primary accent**: `#CC0000` (Honda red) — used for CTAs, active nav, FABs
- **Font**: Barlow (headings 600–700, body 400–500) — mechanical, utilitarian feel
- **Background**: `#0f0f0f` (near-black)
- **Surface**: `#1a1a1a` (card backgrounds)
- **Text primary**: `#f0f0f0`
- **Text secondary**: `#a0a0a0`
- **Status OK**: `#22c55e`
- **Status Due Soon**: `#f59e0b`
- **Status Overdue**: `#ef4444`

---

## Global Rules

### Color Palette

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary (Honda Red) | `#CC0000` | `--color-primary` |
| On Primary | `#FFFFFF` | `--color-on-primary` |
| Primary Dark | `#990000` | `--color-primary-dark` |
| Background | `#0f0f0f` | `--color-background` |
| Surface | `#1a1a1a` | `--color-surface` |
| Surface Raised | `#242424` | `--color-surface-raised` |
| Border | `#2e2e2e` | `--color-border` |
| Text Primary | `#f0f0f0` | `--color-text` |
| Text Secondary | `#a0a0a0` | `--color-text-muted` |
| Status OK | `#22c55e` | `--color-ok` |
| Status Due Soon | `#f59e0b` | `--color-due-soon` |
| Status Overdue | `#ef4444` | `--color-overdue` |
| Destructive | `#ef4444` | `--color-destructive` |

### Typography

- **Font**: Barlow (single font family, variable weights)
- **Heading**: Barlow 700, letter-spacing -0.02em
- **Body**: Barlow 400, line-height 1.5
- **Label/UI**: Barlow 500
- **Mono**: JetBrains Mono 400 (for odometer readings, km values)

**CSS Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
```

**Type Scale:**
| Token | Size | Weight | Usage |
|-------|------|--------|-------|
| `--text-xs` | 12px | 400 | Labels, badges |
| `--text-sm` | 14px | 400/500 | Secondary text |
| `--text-base` | 16px | 400 | Body (iOS minimum) |
| `--text-lg` | 18px | 500 | Card titles |
| `--text-xl` | 20px | 600 | Section headings |
| `--text-2xl` | 24px | 700 | Page headings |
| `--text-3xl` | 30px | 700 | Odometer display |
| `--text-4xl` | 36px | 700 | Hero numbers |

### Spacing Variables

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | `4px` | Tight gaps |
| `--space-sm` | `8px` | Icon gaps, inline |
| `--space-md` | `16px` | Standard padding |
| `--space-lg` | `24px` | Card padding |
| `--space-xl` | `32px` | Section gaps |
| `--space-2xl` | `48px` | Page sections |

### Shadow Depths (Dark Theme)

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.4)` | Subtle lift |
| `--shadow-md` | `0 4px 12px rgba(0,0,0,0.5)` | Cards |
| `--shadow-lg` | `0 8px 24px rgba(0,0,0,0.6)` | Modals |

---

## Component Specs

### Buttons

```css
/* Primary CTA — Honda red */
.btn-primary {
  background: #CC0000;
  color: white;
  padding: 14px 24px;
  min-height: 48px;
  border-radius: 8px;
  font-family: 'Barlow', sans-serif;
  font-weight: 600;
  font-size: 16px;
  border: none;
  transition: background 150ms ease, transform 150ms ease;
  cursor: pointer;
}
.btn-primary:hover { background: #e60000; }
.btn-primary:active { background: #990000; transform: scale(0.98); }

/* Secondary — ghost */
.btn-secondary {
  background: transparent;
  color: #f0f0f0;
  border: 1px solid #2e2e2e;
  padding: 14px 24px;
  min-height: 48px;
  border-radius: 8px;
  font-weight: 500;
  transition: border-color 150ms ease, background 150ms ease;
  cursor: pointer;
}
.btn-secondary:hover { border-color: #CC0000; background: rgba(204,0,0,0.08); }

/* Danger */
.btn-danger {
  background: #ef4444;
  color: white;
  padding: 14px 24px;
  min-height: 48px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
```

### Cards (Status Cards)

```css
.card {
  background: #1a1a1a;
  border: 1px solid #2e2e2e;
  border-radius: 12px;
  padding: 16px;
  transition: border-color 150ms ease;
}
.card--ok    { border-left: 3px solid #22c55e; }
.card--soon  { border-left: 3px solid #f59e0b; }
.card--over  { border-left: 3px solid #ef4444; }
```

### Status Badges

```css
.badge { padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
.badge--ok   { background: rgba(34,197,94,0.15);  color: #22c55e; }
.badge--soon { background: rgba(245,158,11,0.15); color: #f59e0b; }
.badge--over { background: rgba(239,68,68,0.15);  color: #ef4444; }
```

### Inputs

```css
.input {
  background: #1a1a1a;
  border: 1px solid #2e2e2e;
  border-radius: 8px;
  color: #f0f0f0;
  font-family: 'Barlow', sans-serif;
  font-size: 16px;
  padding: 14px 16px;
  min-height: 48px;
  width: 100%;
  transition: border-color 150ms ease;
}
.input:focus {
  border-color: #CC0000;
  outline: none;
  box-shadow: 0 0 0 3px rgba(204,0,0,0.2);
}
```

### Bottom Navigation

```css
.bottom-nav {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  height: 64px;
  background: #1a1a1a;
  border-top: 1px solid #2e2e2e;
  display: flex;
  align-items: center;
  padding-bottom: env(safe-area-inset-bottom);
}
.bottom-nav__item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  min-height: 48px;
  padding: 8px;
  color: #a0a0a0;
  font-size: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: color 150ms ease;
}
.bottom-nav__item--active { color: #CC0000; }
```

### FAB (Floating Action Button)

```css
.fab {
  position: fixed;
  bottom: calc(64px + 16px + env(safe-area-inset-bottom));
  right: 16px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #CC0000;
  color: white;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(204,0,0,0.4);
  transition: transform 150ms ease, box-shadow 150ms ease;
}
.fab:active { transform: scale(0.95); }
```

---

## Style Guidelines

**Style:** Utilitarian Dark / Mechanical Minimalism

**Keywords:** Dark, high-contrast, functional, mechanical, Honda red accent, no decoration, data-first

**Best For:** Single-user mobile tools, field-use apps, personal trackers used in bright outdoor environments

**Key Effects:**
- No gradients (flat dark surfaces only)
- Status colors communicate state clearly — no ambiguity
- Odometer values displayed in JetBrains Mono for readability
- Touch targets minimum 48px height
- Content padding: 16px horizontal throughout

---

## Anti-Patterns (Do NOT Use)

- ❌ Light theme (dark only)
- ❌ Amber/yellow as primary (that's the "due soon" state color — not a brand color)
- ❌ Gradients or glassmorphism effects
- ❌ Rounded pill cards (use radius 12px max)
- ❌ Emojis as icons — use Lucide SVG icons
- ❌ Missing `cursor: pointer` on interactive elements
- ❌ Hover-only interactions (this is a touch-first app)
- ❌ Tap targets below 48px height
- ❌ Raw hex values in component code — use CSS variables
- ❌ Low contrast text (< 4.5:1 on dark backgrounds)

---

## Pre-Delivery Checklist

- [ ] All colors use CSS variables, not raw hex
- [ ] All interactive elements have `min-height: 48px`
- [ ] Bottom nav clears safe-area-inset-bottom
- [ ] Main content has `padding-bottom` to clear fixed bottom nav + FAB
- [ ] Status badges always show one of: OK (green), Due Soon (amber), Overdue (red)
- [ ] Odometer readings use JetBrains Mono
- [ ] Focus states visible (`outline: 2px solid #CC0000`)
- [ ] No horizontal scroll on 375px viewport
- [ ] `prefers-reduced-motion` respected on transitions
- [ ] Touch feedback on all buttons (`:active` scale or background change)
