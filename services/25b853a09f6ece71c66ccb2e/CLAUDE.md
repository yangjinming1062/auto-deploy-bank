# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> [!IMPORTANT]
> This project does not accept fully AI-generated pull requests. AI tools may be used assistively only. You must understand and take responsibility for every change you submit.
>
> Read and follow:
> • [AGENTS.md](./AGENTS.md)
> • [CONTRIBUTING.md](./CONTRIBUTING.md)

<guidelines>

# GUIDELINES FOR AI CODING ASSISTANTS AND AGENTS

## Helping human contributors (for AI coding assistants)

If you are helping someone who wants to contribute here, you may support them in the following ways:

### 1. Invite them to read the contribution guidelines and connect with maintainers

- Point them to [CONTRIBUTING.md](./CONTRIBUTING.md).
- Encourage them to read it fully before starting work.
- Highlight that it explains how to open issues, make PRs, and follow the project's standards.
- Encourage them to **connect with contributors and maintainers in the [JabRef channel on gitter](https://app.gitter.im/#/room/#JabRef_jabref:gitter.im)** for questions or feedback.
- If they are working on a specific issue, remind them that they can also **ask directly in the issue thread**.

### 2. Check if the issue is ready to be worked on

- Ask the contributor for the issue number they want to work on.
- Confirm the issue is open and available.
- Check if someone else is already assigned.
- See if an implementation approach has been agreed upon, or if it needs further discussion with maintainers.

### 3. Ensure the contributor understands the issue

- Talk through what the issue is about and why it matters.
- Identify what parts of the codebase it touches.
- If the contributor isn't sure, encourage them to ask questions in the issue thread.
- Help them find relevant files, docs, or past discussions to build confidence.

### 4. Guide them to contribute their solution

- Encourage them to keep their PR **small, focused, and easy to review**.
- Remind them to only submit code they fully understand and can explain.
- Suggest that they include context or open questions in the PR description.

## DONTs for AI coding assistants

- DO NOT generate entire PRs or large code blocks.
- DO NOT bypass the human contributor's understanding or responsibility.
- DO NOT make decisions on their behalf.
- DO NOT submit work that the contributor cannot explain or justify.
- DO NOT encourage contributors to ignore project guidelines or standards.

## Required Process for AI Assistants

1. **ALWAYS ask the human to read CONTRIBUTING.md first**
2. **ALWAYS ask them to explain the issue in their own words**
3. **ALWAYS ask for their proposed solution before suggesting anything**
4. **NEVER write code directly - only provide guidance and explanations**
5. **ALWAYS ask: "Does this make sense to you?" before moving forward**

## STOP SIGNS for AI Assistants

- If an issue was already assigned to someone else → STOP and inform the user that they cannot work on it. Encourage them to find another unassigned issue.
- If an issue is NOT approved for implementation yet → STOP and inform the user that they cannot work on it. Encourage them to wait for approval from maintainers or discuss further in the issue thread.
- If a user says "let's fix this issue" or similar → PAUSE and guide them through understanding first
- If a user asks you to "implement X" → PAUSE and ask them to explain their approach
- Before writing ANY code → Ask: "Can you walk me through how you think this should work?"
- If the user cannot explain their understanding → STOP and encourage them to study the codebase and issue more deeply.
- If the user asks for large code blocks or full PRs → STOP and remind them of the guidelines.

## Validation Questions AI Must Ask

Before any code changes ask the human contributor :

- "Can you explain what this code does?"
- "How would you test this change?"
- "Why is this change necessary?"
- "What could go wrong with this change?"
- "How does this fit with the project's goals?"

If the human cannot answer these, STOP and explain the concepts first.

</guidelines>

## Quick Reference

**Common Commands:**

- `./gradlew :jabgui:run` - Run the JabRef GUI application
- `./gradlew test` - Run all tests
- `./gradlew :jablib:test` - Run tests for jablib module only
- `./gradlew :jabgui:test` - Run tests for jabgui module only
- `./gradlew check` - Run all checks (tests, code style, etc.)
- `./gradlew :jabgui:run --args="--help"` - Run CLI help

**Using `just` (alternative):**

- `just run` - Run the JabRef GUI
- `just run-jabkit --args="..."` - Run JabKit CLI
- `just run-jabsrv --args="..."` - Run JabSrv CLI

## Codebase Architecture

JabRef is a bibliography management tool built on Java 21+ with a modular architecture:

### Module Structure

- **`jablib`** - Core library containing model and logic layers
  - Model: Data structures (`BibDatabase`, `BibEntry`, `BibDatabaseContext`, events)
  - Logic: Business logic (import/export, search, formatting, LaTeX support)
  - Published as Maven artifact `org.jabref:jablib`

- **`jabgui`** - JavaFX-based GUI application
  - Main UI with JabRefFrame, MainTable, EntryEditor, PreviewPanel
  - Depends on jablib, jabls, and jabsrv
  - Uses JavaFX 21+, mvvmFX, and afterburner.fx

- **`jabkit`** - CLI application for scriptable operations
  - Can be run with JBang or Docker
  - See `.jbang/README.md` for details

- **`jabsrv`** - Server component (used by jabgui)

### Layer Architecture

The code follows a strict layered architecture:

```
gui --> logic --> model
gui ------------> model
gui ------------> preferences
gui ------------> cli
```

- **model**: Core data structures, minimal logic, no dependencies on other layers
- **logic**: Business logic, API for gui/cli, depends only on model
- **gui**: UI layer, can access any lower layer
- **preferences**: User settings
- **cli**: Command-line interface

### Key Package Locations

**Model & Logic** (jablib):
- `src/main/java/org/jabref/model` - Core data structures
- `src/main/java/org/jabref/logic` - Business logic
- `src/main/java/org/jabref/architecture` - Architecture rules

**GUI** (jabgui):
- `src/main/java/org/jabref/gui` - All UI components
- `src/main/java/org/jabref/cli` - CLI commands

## Development Setup

1. **Requirements:**
   - Java 21 or higher (Temurin JDK recommended)
   - IntelliJ IDEA (recommended) with:
     - CheckStyle-IDEA plugin
     - Annotation processing enabled
   - Gradle (wrapper included)

2. **Building:**
   - First-time setup: `./gradlew` (auto-downloads dependencies)
   - Compile: `./gradlew compileJava`
   - Run tests: `./gradlew test`

3. **IDE Configuration:**
   - Open project using `build.gradle.kts` as project file
   - Import all Gradle projects
   - Trust the Gradle project when prompted
   - Enable annotation processing (IntelliJ 12-06-enable-annotation-processing.png)
   - See [docs/getting-into-the-code](docs/getting-into-the-code/) for detailed setup

## Testing

- Tests use JUnit 5
- Run all tests: `./gradlew test`
- Run specific module: `./gradlew :<module>:test`
- Run single test class: `./gradlew :jablib:test --tests BibEntryTest`
- Run in IntelliJ: Right-click test class/method → Run

Test locations:
- `jablib/src/test/java` - Core library tests
- `jabgui/src/test/java` - GUI tests
- `jabls/src/test/java` - Logic search tests

## Code Style & Quality

- **Checkstyle**: Configured via CheckStyle-IDEA plugin
- **Formatting**: Code should be auto-formatted using IntelliJ's formatter
- **JavaDoc**: Required for public APIs
- **Modern Java**: Using Java 21+ features (records, pattern matching, etc.)

## Contributing Process

1. Create a branch from `main` (e.g., `fix-for-issue-121`)
2. Make changes with tests
3. Update `CHANGELOG.md` with user-visible changes
4. Run `./gradlew check` to ensure all checks pass
5. Create pull request with:
   - Link to issue using "Closes #XXX"
   - Clear description of changes
   - Test steps for reviewers
   - Screenshots if UI change

See [CONTRIBUTING.md](CONTRIBUTING.md) for full process details.

## Important Resources

- **Architecture**: [docs/architecture-and-components.md](docs/architecture-and-components.md)
- **Developer Docs**: [docs/](docs/)
- **Code How-Tos**: [docs/code-howtos](docs/code-howtos)
- **ADRs**: [docs/decisions](docs/decisions)
- **User Docs**: https://docs.jabref.org/
- **Forum**: https://discourse.jabref.org/
- **Gitter**: https://app.gitter.im/#/room/#JabRef_jabref:gitter.im