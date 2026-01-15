# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DragonBonesJS is a JavaScript/TypeScript runtime for the DragonBones 2D skeletal animation system. The core library is framework-agnostic and uses adapter pattern to support multiple HTML5 game engines: Egret, PixiJS, Phaser, Hilo, and Cocos Creator.

## Build Commands

```bash
# Install dependencies
npm install

# Build core DragonBones library (outputs to DragonBones/out/)
cd DragonBones && npm install && npm run build

# Build specific framework runtime
cd Egret/4.x && npm install && npm run build
cd Pixi/2.x && npm install && npm run build
cd Phaser/2.x && npm install && npm run build
cd Hilo/1.x && npm install && npm run build
cd Cocos/1.x && npm install && npm run build

# Build all frameworks
cd DragonBones && npm run build-all
```

The CLI tool can also build runtimes against specific library versions:
```bash
npx dbr pixijs@4.0.0 -o ./build-output
```

## Architecture

### Core Library (`DragonBones/src/dragonBones/`)

The framework-agnostic animation engine organized into modules:
- **core/**: DragonBones singleton (entry point), BaseObject (object pooling)
- **animation/**: Animation, AnimationState, WorldClock, timeline states
- **armature/**: Armature, Bone, Slot, Constraint, TransformObject
- **model/**: Data classes defining the DragonBones JSON/binary format
- **parser/**: ObjectDataParser (JSON), BinaryDataParser (binary)
- **factory/**: BaseFactory - creates armatures from parsed data
- **event/**: Event system for animation callbacks
- **geom/**: Matrix, Transform, Point, Rectangle, ColorTransform

### Framework Adapters

Each supported engine has an adapter layer that implements framework-specific classes:

| Engine | Path | Version |
|--------|------|---------|
| Egret | Egret/4.x/src/dragonBones/egret/ | 4.x |
| PixiJS | Pixi/2.x/src/dragonBones/pixi/ | 2.x (v4) |
| Phaser | Phaser/2.x/src/dragonBones/phaser/ | 2.x (Phaser CE) |
| Hilo | Hilo/1.x/src/dragonBones/hilo/ | 1.x |
| Cocos | Cocos/1.x/src/dragonBones/cocos/ | 1.x |

Adapter classes typically include:
- `*Factory`: Extends BaseFactory to create framework-native armatures
- `*Slot`: Renders display objects in slots
- `*ArmatureDisplay`: Container for armature display
- `*TextureAtlasData`: Wraps framework texture atlases

### Data Flow

1. Parse DragonBones JSON/binary data using `factory.parseDragonBonesData()`
2. Parse texture atlas data using `factory.parseTextureAtlasData()`
3. Create armatures via `factory.buildArmature(name)`
4. Add armature display to stage and advance time via `armature.clock.advanceTime()`

## Code Conventions

- Uses internal `dragonBones` namespace (not ES modules)
- TypeScript 2.4.2 targeting ES5 with DOM and ES2015 Promise libs
- All files must be explicitly listed in tsconfig.json `files` array
- TSLint: semicolons required, no unused variables/parameters, triple-equals
- Object pooling via `BaseObject.borrowObject()` / `returnToPool()`
- Event buffering through DragonBones singleton's event queue

## Key Classes

- `DragonBones`: Main singleton, manages event dispatch and world clock
- `BaseFactory`: Abstract factory for building armatures
- `Armature`: Container for bones, slots, and animation controller
- `Animation`: Manages animation states for an armature
- `WorldClock`: Global time keeper for animations