# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Commits is an IntelliJ IDEA/Android Studio plugin that generates git commit messages using LLMs. It integrates with the IDE's commit workflow and supports 11+ LLM providers via langchain4j.

**Tech Stack:**
- Kotlin 2.2.21 with JVM toolchain 21
- IntelliJ Platform SDK 2024.2+
- Gradle 9.1.0 with Kotlin DSL
- langchain4j 1.8.0 for LLM integrations
- kotlinx-serialization-json 1.9.0

## Common Commands

```bash
# Build plugin and run tests
./gradlew build

# Run IDE with plugin installed (sandbox mode)
./gradlew runIde

# Build distribution zip
./gradlew buildPlugin

# Run specific test class
./gradlew test --tests "com.github.blarc.ai.commits.intellij.plugin.HintRegexTest"

# Lint and code analysis
./gradlew check

# Publish to JetBrains Marketplace (requires env vars)
./gradlew publishPlugin
```

## Architecture

### Core Entry Points

**Actions** (`src/main/kotlin/.../plugin/`):
- `AICommitAction`: Keyboard shortcut action (Ctrl+Alt+C) for commit dialog
- `AICommitSplitButtonAction`: Commit toolwindow button with dropdown for client selection
- Both trigger `LLMClientConfiguration.generateCommitMessageAction()` to generate messages

**Plugin Configuration** (`plugin.xml`):
- Registers actions, notification groups, project configurables, and checkin handler
- Key extension point: `checkinHandlerFactory` for commit workflow integration

### Settings Architecture

**AppSettings2** (APP-level, singleton):
- Stored in `AICommits2.xml`
- Contains LLM client configurations, prompts, exclusions, and global settings
- Uses IntelliJ's `PersistentStateComponent` for persistence

**ProjectSettings** (PROJECT-level):
- Per-project active LLM client, selected prompt, and exclusions
- Tracks which LLM was used via split button for future shortcuts

**Client Configuration Pattern**:
Each LLM provider implements a consistent 4-class pattern:
1. `*ClientConfiguration`: Config data (model, temperature, host, tokens), extends `LLMClientConfiguration`
2. `*ClientService`: LLM API logic, extends `LLMClientService<*ClientConfiguration>`
3. `*ClientPanel`: Settings UI form component
4. `*ClientSharedState`: Caches hosts/models lists across sessions

Providers: OpenAI, Ollama, Anthropic, Azure OpenAI, Gemini (Google + Vertex), HuggingFace, GitHub Models, Mistral, Amazon Bedrock, Qianfan

### LLM Integration Flow

```
AICommitAction/AICommitSplitButtonAction
    → LLMClientConfiguration.generateCommitMessageAction()
    → LLMClientService.generateCommitMessage()
    → computeDiff() / constructPrompt()
    → buildChatModel() / buildStreamingChatModel()
    → LLM API call via langchain4j
    → setCommitMessage() on workflow handler
```

**Key Utilities** (`AICommitsUtils.kt`):
- `computeDiff()`: Builds unified diff from selected changes, respecting exclusions
- `constructPrompt()`: Substitutes variables ({diff}, {branch}, {taskId}, {hint}) in prompt templates
- `getCommonBranch()`: Determines common VCS branch across changes (Git + SVN)
- `matchesGlobs()`: Path exclusion matching using FileSystem glob patterns

### Prompt Template Variables

- `{diff}`: Git diff output
- `{branch}`: Common branch name (defaults to "main" if undetermined)
- `{taskId}`, `{taskSummary}`, `{taskDescription}`, `{taskTimeSpent}`: IntelliJ Task integration
- `{hint}`: Optional commit hint from user
- `{locale}`: IDE display language

### Credential Management

API tokens stored via IntelliJ's `PasswordSafe` using `CredentialAttributes`. Each client generates unique credential attributes from its ID for secure storage.

## Key Files

- `build.gradle.kts`: Build configuration, dependencies (langchain4j integrations)
- `src/main/resources/META-INF/plugin.xml`: Plugin descriptor with extensions/actions
- `src/main/kotlin/.../settings/AppSettings2.kt`: Main settings storage
- `src/main/kotlin/.../settings/clients/LLMClientService.kt`: Abstract base for LLM API calls
- `src/main/kotlin/.../plugin/AICommitsUtils.kt`: Diff computation, prompt construction