# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

t3tr0s is a multiplayer Tetris clone built with ClojureScript. It features 10 historical themes representing different versions of Tetris from 1984-2014, single-player and multiplayer modes, real-time spectating, and a master of ceremonies (MC) control panel.

## Build Commands

```sh
# Install dependencies
npm install

# Install grunt globally (for LESS compilation)
npm install -g grunt-cli

# Compile LESS to CSS
grunt

# Compile ClojureScript (client and server)
lein clean && lein cljsbuild once

# Copy config and start server
cp example.config.json config.json
node server.js
```

- Development server runs at http://localhost:1984
- Browser REPL for interactive testing: `lein repl` then `(brepl)`

## Architecture

### Source Organization

- `src/client/` - Browser-side ClojureScript
  - `game/` - Core game logic (rules, board, painting, history, vcr)
  - `pages/` - Route handlers (login, lobby, play, spectate, mc, menu)
  - `core.cljs` - Main entry point, game state management, input handling
  - `socket.cljs` - WebSocket communication wrapper
  - `state.cljs` - Global state atoms
  - `routes.cljs` - Page routing via page.js

- `src/server/` - Node.js server compiled from ClojureScript
  - `core.cljs` - Express server, Socket.io, game loop, player management
  - `html.cljs` - Static HTML generation
  - `util.cljs` - Server utilities

- `public/` - Static assets (CSS, images, audio, fonts)
  - Tilemap images for 10 themes in `img/`

### Key Patterns

**State Management**: Uses Clojure atoms for reactive state. Game state is in `client.game.core/state`. Server player table is in `server.core/players`.

**Game Loop**: Gravity and control loops use `go-loop` with `alts!` for concurrent channel operations. Key channels include `quit-chan` (exit signal), `move-down-chan`, `move-left-chan`, `move-right-chan`.

**Game Logic** (in `client/game/`):
- `board.cljs` - Board operations (collision, rotation, row collapse)
- `rules.cljs` - Scoring, leveling, gravity speed curves
- `paint.cljs` - Canvas rendering with theme support
- `history.cljs` - Score history graph visualization
- `vcr.cljs` - Game recording/playback

**Server Events**: Socket.io events for multiplayer sync (`update-player`, `game-over`, `countdown`, leaderboards).

**Themes**: Theme configurations are in `client.game.core/themes` map, each with year and platform. Theme ID is saved in localStorage.

## Theme System

10 themes represent Tetris versions:
- 0/10: 1984 Electronika 60
- 1: 1986 MS DOS
- 2: 1986 Tengen/Atari Arcade
- 3/13: 1989 Gameboy
- 4: 1989 NES
- 5: 1989 Sega Genesis
- 6: 1998 Gameboy Color
- 7: 2000 TI-83
- 8: 2002 Flash
- 9: 2012 Facebook
- 19: 2014 Mario

Key numbers (1-9) switch themes; Shift+number for alternates.

## Deployment

Single-player build deploys to GitHub Pages:
```sh
./deploy-singleplayer.sh
```