# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Tailwind Ink** is an AI-powered color palette generator that uses neural networks trained on Tailwind CSS colors. Given a single input color, it generates complete color palettes with 10 shades (50-900) and predicts harmonious adjacent colors.

## Build Commands

```bash
npm install          # Install dependencies
npm run watch        # Development server with hot reload
npm run dev          # Development build
npm run prod         # Production build
```

## Architecture

### Neural Network Models (brain.js)

Two trained neural networks handle color prediction:

1. **Shades Model** (`src/models/shadesModel.js`, `src/training/shades.js`)
   - Input: A single RGB color (normalized 0-1)
   - Output: 10 shade variants (50-900) for that color family
   - Structure: 3 inputs → [3 hidden neurons] → 30 outputs

2. **Next Model** (`src/models/nextModel.js`, `src/training/next.js`)
   - Input: A color at a specific shade level
   - Output: 9 adjacent colors in a palette (horizontally)
   - Structure: 3 inputs → [3 hidden neurons] → 27 outputs

### Entry Points

- `index.html` - Main application with interactive palette generation
- `shades.html` - UI for testing/training the shades model
- `next.html` - UI for testing/training the next model

### Key Source Files

- `src/main.js` - Main application logic (palette generation, chart rendering, color manipulation)
- `src/models/wrapper/wrapper.js` - Adapter that converts hex colors to RGB format for model input
- `src/training/*.js` - Scripts for training new neural network models

### Datasets

Located in `src/datasets/`, these contain color palettes used for training:
- `originals.js` - Original Tailwind palette colors
- `news.js`, `news-revised.js`, `news-revised-desaturated*.js` - Additional training data
- `ui.js` - UI-focused color palettes
- `may/may.js` - Another training dataset (currently used in shades training)

### Model Training

To train models, open `shades.html` or `next.html` in a browser (requires `npm run watch`), or run directly:

```bash
node src/training/shades.js    # Train shades model
node src/training/next.js      # Train next model
```

Training outputs the inference function to console - copy this to `models/shadesModel.js` or `models/nextModel.js`.

### Color Manipulation

The app uses `chroma-js` for color space conversions (RGB ↔ LCH). All internal color operations use LCH for perceptual uniformity. Key conversion functions:
- `rgbToHex()` - RGB to hex
- `normalizeToLCH()` - Converts model output to LCH color space
- `normalizeFamily()` - Converts a single color family to LCH format

## Dependencies

Key libraries:
- `brain.js@2.0.0-beta.2` - Neural network library
- `chroma-js` - Color manipulation
- `chart.js` - Interactive charts (luminosity, chroma, hue, contrast)
- `@simonwep/pickr` - Color picker component
- `tailwindcss@1.7.x` - CSS framework
- `laravel-mix` - Webpack-based build system