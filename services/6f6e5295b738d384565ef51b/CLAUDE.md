# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Botright is an undetectable browser automation framework built on Playwright. It provides fingerprint spoofing, browser stealth techniques, and automated captcha solving (hCaptcha, reCaptcha). The project uses a Chromium-based browser from the local system to maximize stealth.

## Common Commands

```bash
# Install dependencies and project in development mode
pip install -r requirements-test.txt
pip install -e .

# Install Chromium for Playwright
python -m playwright install chromium

# Run all tests
pytest

# Run specific test file
pytest tests/test_recaptcha.py

# Run with coverage
pytest --cov=botright --cov-report=term-missing

# Linting
isort . --check-only          # Check import order
flake8 .                      # PEP8 linting
mypy botright                 # Type checking
black . --check               # Code formatting check
```

## Architecture

### Core Components

- **Botright** (`botright/botright.py`): Main entry point that manages Playwright lifecycle, browser launch options, and configuration. Uses `async_class` for async object lifecycle management.

- **Faker** (`botright/modules/faker.py`): Generates fake browser fingerprints using `chrome-fingerprints` library. Creates user agent, GPU info, screen dimensions, and locale data based on proxy location.

- **ProxyManager** (`botright/modules/proxy_manager.py`): Handles proxy configuration and country-based locale mapping.

- **playwright_mock** (`botright/playwright_mock/`): Wraps Playwright's native classes to inject stealth features:
  - `Page`: Extends Playwright Page with captcha solving methods (`solve_hcaptcha`, `solve_recaptcha`) and modified mouse/keyboard for human-like behavior
  - `BrowserContext`: Custom browser context with fingerprint injection
  - `Locator`, `Frame`, `FrameLocator`: Stealth-aware element interactions

### Captcha Solving

- **hCaptcha** (`botright/modules/hcaptcha.py`): Uses `hcaptcha_challenger` agent to solve challenges via image classification
- **reCaptcha**: Uses `recognizer.agents.playwright.AsyncChallenger` for visual reCaptcha solving

### Fingerprint Stealth

The framework applies multiple layers of stealth:
1. Modifies browser launch flags (~120 Chrome flags to disable automation signals)
2. Spoofs navigator properties via CDP (User-Agent, platform, brands)
3. Fingerprint masking using `chrome-fingerprints` library
4. Canvas image data noise injection
5. Mouse movement simulation for user action layers

### Key Configuration Options

```python
await botright.Botright(
    headless=False,           # Run browser in headless mode
    block_images=False,       # Block image loading
    user_action_layer=False,  # Enable human-like mouse movements
    scroll_into_view=True,    # Auto-scroll elements into view
    spoof_canvas=True,        # Canvas fingerprint protection
    mask_fingerprint=True,    # Apply fingerprint masking
)
```

## Development Notes

- All async code uses `async_class` - implement `__ainit__` instead of `__init__`
- The project follows Python 3.8+ compatibility
- Imports are managed via isort with multi_line_output=7 (vertical hanging indent)
- Line length limit is 200 characters
- Contributions should follow conventional commit messages
- New captcha solving methods should be added to `Page` class in `playwright_mock/page.py`