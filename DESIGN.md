# DESIGN.md - VoltAgent

## Visual Identity
- **Core Concept**: Void-black canvas, emerald accent, terminal-native.
- **Aesthetic**: High-contrast, developer-centric, electric, and precise.
- **Vibe**: "The Matrix" meets modern high-end IDE.

## Color Palette
- **Background**: `#000000` (Pure Black)
- **Surface**: `#0A0A0A` (Deep Grey)
- **Primary (Accent)**: `#10B981` (Emerald Green)
- **Secondary**: `#34D399` (Mint)
- **Text (Primary)**: `#FFFFFF` (White)
- **Text (Secondary)**: `#9CA3AF` (Cool Grey)
- **Border**: `#1F2937` (Dark Slate)
- **Glow**: `rgba(16, 185, 129, 0.15)`

## Typography
- **Primary Font**: `Geist Mono`, `JetBrains Mono`, or any high-quality monospace font.
- **Secondary Font**: `Geist Sans` or `Inter` for UI labels.
- **Scale**:
  - **H1**: 2.5rem, Bold, Tight tracking (-0.05em)
  - **H2**: 1.75rem, Semi-bold
  - **Body**: 0.875rem, Regular
  - **Code**: 0.8125rem, Monospace

## Layout & Spacing
- **Grid**: 8px base unit.
- **Container**: Max-width 1200px, centered.
- **Padding**: Generous internal padding (24px+) to create "breathing room" against the black background.
- **Borders**: 1px solid `#1F2937`. No rounded corners (0px) or very slight (2px) for a sharp, technical feel.

## Components
- **Buttons**:
  - **Primary**: Emerald background (`#10B981`), black text, sharp corners.
  - **Ghost**: Transparent background, emerald border, emerald text.
- **Cards**: Pure black background, 1px slate border, subtle emerald glow on hover.
- **Inputs**: Terminal-style. No background, bottom border only or thin slate border. Emerald cursor/caret.
- **Badges**: Monospace text, emerald border, small font size.

## Effects
- **Glow**: Use `box-shadow: 0 0 20px rgba(16, 185, 129, 0.1)` for active states.
- **Transitions**: Fast, linear transitions (150ms).
- **Scanlines**: Optional subtle overlay of horizontal lines (opacity 0.03) to enhance the terminal feel.

## Design Guardrails
- **NO Gradients**: Use solid colors only.
- **NO Soft Shadows**: Use borders or glows instead.
- **NO Rounded Corners**: Keep it sharp and "engineered."
- **Contrast**: Maintain AAA contrast ratios at all times.
