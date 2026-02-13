# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Claude Code repository - an agentic coding CLI tool that extends Claude's capabilities through a modular plugin system. The repository contains:

- **`/plugins/`**: Official plugins that extend Claude Code functionality with commands, agents, skills, and hooks
- **`/examples/`**: Example configurations and hook patterns for settings, hooks, and development
- **`/scripts/`**: GitHub automation scripts for issue triage and management
- **`/.github/workflows/`**: GitHub Actions workflows for repository maintenance

## Plugin Architecture

Plugins are self-contained modules with a standardized structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata (name, version, author)
├── commands/                # Slash commands (.md files with YAML frontmatter)
├── agents/                  # Specialized agents (.md files with YAML frontmatter)
├── skills/                  # Knowledge bases with SKILL.md and references/
├── hooks/                   # Event handlers (hooks/hooks.json + scripts)
├── .mcp.json                # Optional MCP server configuration
└── README.md                # Plugin documentation
```

### Component Types

**Commands**: Slash commands triggered by users (e.g., `/code-review`). Defined in `.md` files with YAML frontmatter containing `description`, `argument-hint`, and `allowed-tools`.

**Agents**: Autonomous subagents with specific roles. Defined in `.md` files with frontmatter specifying `name`, `model`, `color`, and tools. Body contains the system prompt.

**Skills**: Contextual knowledge loaded based on trigger phrases. Include `SKILL.md` with third-person descriptions and optional `references/`, `examples/`, `scripts/` directories.

**Hooks**: Event-driven automation. Configured in `hooks/hooks.json` with event types (`PreToolUse`, `SessionStart`, `PostToolUse`, `Stop`) and command/prompt handlers.

**MCP Servers**: External tool integrations via `{
  "servers": {
    "server-name": {
      "type": "stdio",
      "command": "...",
      "args": ["..."]
    }
  }
}`.

### YAML Frontmatter Format

Commands and agents use YAML frontmatter:

```yaml
---
allowed-tools: ["Read", "Write", "Bash"]
description: Brief command description
argument-hint: Expected argument format
---
# Agent/command instructions (written FOR Claude, not TO user)
```

Use `${CLAUDE_PLUGIN_ROOT}` for portable paths in hook commands and MCP configs.

## Working with Plugins

### Creating New Plugins

Use the `/plugin-dev:create-plugin` command for an 8-phase guided workflow that covers discovery, component planning, implementation, validation, and documentation.

### Validation Scripts

Scripts in `plugins/plugin-dev/skills/*/scripts/` validate components:
- `validate-agent.sh <agent.md>` - Validates agent YAML structure
- `validate-hook-schema.sh <hooks.json>` - Validates hook JSON schema
- `test-hook.sh <hook.py> <input.json>` - Tests hook behavior with sample input

### Plugin Development Skills

Use the `Skill` tool to load development guidance:
- `plugin-structure` - Component types and when to use each
- `skill-development` - Writing effective skills with progressive disclosure
- `command-development` - Command patterns and tool access
- `agent-development` - Agent design and triggering conditions
- `hook-development` - Event handlers and validation
- `mcp-integration` - External tool integration

## Key Conventions

- **Progressive disclosure**: Skills provide layered information (metadata → summary → detailed references)
- **Third-person descriptions**: Skills describe what they do in third person (e.g., "This skill provides...")
- **Imperative instructions**: Command/agent bodies are written FOR Claude in imperative form
- **Specific triggers**: Agents use concrete `<example>` blocks with specific scenarios
- **Portable paths**: Always use `${CLAUDE_PLUGIN_ROOT}` instead of hardcoded paths
- **Security-first**: Use HTTPS, avoid hardcoded credentials, document required env vars

## GitHub Automation

The `/scripts/` directory contains TypeScript utilities for GitHub operations:
- `auto-close-duplicates.ts` - Auto-closes duplicate issues
- `backfill-duplicate-comments.ts` - Comments on duplicate issues
- `sweep.ts` - Archives old issues and PRs

Run with: `npx ts-node scripts/<script>.ts`

## Settings Configuration

The `examples/settings/` directory provides organizational settings templates:
- `settings-lax.json` - Permissive settings with marketplace blocking
- `settings-strict.json` - Strict settings blocking plugins, hooks, and web tools
- `settings-bash-sandbox.json` - Bash sandbox configuration

Settings are applied via the [settings hierarchy](https://code.claude.com/docs/en/settings).