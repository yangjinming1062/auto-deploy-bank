# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Obsidian Text Generator Plugin is an AI-powered text generation plugin for Obsidian that integrates with multiple LLM providers (OpenAI, Anthropic, Google, etc.). It provides template-based text generation, context management, and various AI-powered features within the Obsidian knowledge management system.

**Key Technologies**: TypeScript, esbuild, React, TailwindCSS, Handlebars, LangChain

## Common Commands

### Development
```bash
pnpm install     # Install dependencies
pnpm run dev     # Build plugin with watch mode (development)
pnpm run build   # Production build
```

### Code Quality
```bash
pnpm run eslint                # Run ESLint with auto-fix
pnpm run prettier:check        # Check code formatting
pnpm run prettier:format       # Format code
pnpm run build:css            # Build CSS from Tailwind
pnpm run dev:css              # Watch CSS changes
```

### Version Management
```bash
npm run version               # Bump version
npm run version:go            # Bump version and update Go modules
```

**Build Output**: `main.js` and `styles.css` (generated files - do not edit directly)

## Architecture

### Core Components

**Plugin Entry Point** (`src/main.ts`)
- Main `TextGeneratorPlugin` class extending Obsidian's `Plugin`
- Initializes all services and registers commands
- Handles plugin lifecycle events (onload/onunload)

**Services Layer** (`src/services/`)
- `text-generator.ts`: Core text generation logic
- `api-service.ts`: API request handling and LLM communication
- `pluginAPI-service.ts`: Plugin API for external integration
- `auto-suggest.ts`: Auto-suggestion feature
- `slash-suggest.ts`: Slash command suggestions
- `tgBlock.ts`: Block-level text generation
- `overlayToolbar-service.ts`: Floating toolbar UI

**LLM Providers** (`src/LLMProviders/`)
- **Base Layer**: Provider interface and registry (`interface.ts`, `registery.ts`)
- **LangChain Integration** (`langchain/`): OpenAI, Anthropic, Google, Azure, MistralAI, Ollama, HuggingFace, Replica
- **Custom Providers** (`custom/`): Direct API integrations for Anthropic, etc.
- Provider selection is configured in settings and used for different generation modes

**Scope Layer** (`src/scope/`)
- `commands.ts`: All Obsidian commands registration
- `context-manager.ts`: Context gathering from vault (current note, selection, linked notes, etc.)
- `content-manager.ts`: Editor content manipulation
- `tokens.tsx`: Token tracking and display
- `embeddings.ts`: Vector embeddings for semantic search
- `package-manager/`: Template/package management system
- `versionManager.ts`: Version and migration handling

**UI Components** (`src/ui/`)
- React-based components with TailwindCSS
- `settings/`: Settings panel and configuration UI
- `components/`: Reusable React components (modals, forms, etc.)
- `template-input-modal/`: Template parameter input
- `playground/`: Testing playground for prompts
- `tool/`: Extractors and utilities

**Extraction Tools** (`src/extractors/`)
- PDF, web pages, YouTube, audio, and image extraction
- Used to gather context for generation

### Data Flow

1. **Generation Request**: User triggers command or auto-suggest
2. **Context Gathering**: `ContextManager` collects relevant content from vault
3. **Template Processing**: Handlebars templates are rendered with context
4. **LLM Communication**: Request sent via selected `LLMProvider`
5. **Response Handling**: Streamed or direct response inserted into editor
6. **Metadata**: Generation info stored as YAML frontmatter

### Configuration

**Settings** (`src/types.ts`, `default-settings.ts`)
- API keys and endpoints per provider
- Default generation parameters (temperature, max_tokens, etc.)
- Feature flags and experimental options
- Auto-suggest and slash-suggest configurations

**Models** (`src/lib/models/index.ts`)
- Pre-configured AI models with metadata
- Pricing, max tokens, and encoding information
- Supported LLM provider mappings

## Build System

**esbuild Configuration** (`esbuild.config.mjs`)
- Bundles TypeScript to CommonJS (`main.js`)
- External packages: Obsidian, Electron, CodeMirror, builtins
- WASM plugin for handling WebAssembly files
- Watch mode for development
- Production minification enabled

**CSS** (`tailwind.config.js`, `postcss.config.js`)
- TailwindCSS with DaisyUI
- Global styles in `src/css/global.css`
- PostCSS compilation to `styles.css`

## Key Files to Know

- `manifest.json` / `manifest-beta.json`: Plugin manifest for Obsidian
- `src/constants.ts`: Shared constants and icons
- `src/utils/index.ts`: Utility functions
- `src/helpers/handlebars-helpers.ts`: Custom Handlebars helpers
- `.eslintrc`, `.prettierrc`: Linting and formatting rules
- `recipes.md`: Community template recipes (external links)

## Development Notes

### Testing
- **No test framework configured** - test manually in Obsidian
- Use `pnpm run dev` with Hot-Reload plugin for development
- Test generation with different LLM providers

### Adding New LLM Providers
1. Implement interface in `src/LLMProviders/interface.ts`
2. Create LangChain or custom implementation
3. Register in `src/LLMProviders/index.ts`
4. Add model metadata to `src/lib/models/index.ts`
5. Update settings UI as needed

### Creating Templates
- Templates use Handlebars syntax
- Access context variables using `{{variable}}`
- Helper functions available in `src/helpers/handlebars-helpers.ts`
- Store in configured `textGenPath` directory

### Performance Considerations
- Large vault context gathering can be slow
- Token counting uses `@dqbd/tiktoken`
- Streamed responses for better UX
- `PerformanceTracker` in `src/lib/utils.ts` for monitoring

## CI/CD

**GitHub Actions** (`.github/workflows/`)
- `ci.yml`: Prettier formatting checks on PR/push
- `release.yml`: Automated release process

No automated testing - ensure manual testing before releases.

## External Resources

- [Documentation](https://bit.ly/tg_docs)
- [Discord Community](https://discord.gg/mEhvhkRfq5)
- [GitHub Repository](https://github.com/nhaouari/obsidian-textgenerator-plugin)