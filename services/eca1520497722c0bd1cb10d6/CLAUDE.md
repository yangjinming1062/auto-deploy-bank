# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `zxcvbn-ts`, a complete TypeScript rewrite of the `zxcvbn` password strength estimator. It is organized as a **Lerna/Yarn monorepo**.

### Key Packages

- **`packages/libraries/main`**: Contains `@zxcvbn-ts/core`. This is the main library responsible for scoring, matching, and generating feedback.
- **`packages/libraries/pwned`**: Contains `@zxcvbn-ts/core-pwned`, an optional addon for checking passwords against the HaveIBeenPwned database.
- **`packages/languages/*`**: Individual language packages (e.g., `en`, `de`, `ja`) providing dictionaries and translations.

## Development Commands

The root `package.json` manages common tasks:

- **Build**: `yarn build` - Compiles all packages (main, pwned, languages) using Rollup.
- **Type Check**: `yarn typecheck` - Runs TypeScript compiler without emitting files.
- **Lint**: `yarn lint` - Runs ESLint with fixes.
- **Test**: `yarn test` - Runs Jest with coverage.
- **Docs**: `yarn docs:dev` - Starts Vuepress dev server for local documentation.

## Architecture

The core logic in `@zxcvbn-ts/core` (located in `packages/libraries/main/src/`) follows the `zxcvbn` pattern:

1. **Matching** (`src/Matching.ts`, `src/matcher/`):
   - Matches password against dictionaries, patterns (spatial, sequences, repeats), and regexes.
   - Returns a list of `Match` objects describing the patterns found.
2. **Scoring** (`src/scoring/`, `src/Scoring.ts`):
   - Calculates `guesses` (entropy/cost) for each match.
   - Runs `mostGuessableMatchSequence` to select the optimal combination of matches that reconstructs the password with the minimum guesses.
3. **Time Estimates** (`src/TimeEstimates.ts`):
   - Converts guesses into human-readable time estimates (e.g., "centuries").
4. **Feedback** (`src/Feedback.ts`):
   - Generates warning/suggestions based on the matched patterns and score.

### Customization

- **Options**: Passed to `zxcvbn` configuration to toggle matchers (e.g., disabling spatial matching) or load custom dictionaries.
- **Custom Matchers**: You can provide custom pattern matchers in the options object.