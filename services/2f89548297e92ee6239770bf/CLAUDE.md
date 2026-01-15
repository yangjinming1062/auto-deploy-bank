# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-enhanced stock analysis system supporting A-shares, Hong Kong, and US stocks. Provides technical analysis, fundamental analysis (25 financial indicators), sentiment analysis, and AI-powered investment recommendations. Available as both desktop GUI (PyQt6) and web application (Flask with SSE streaming).

## Development Commands

### Web Application (Primary)

```bash
cd "2.6 webapp（流式传输测试版）"  # Most stable web version
pip install -r requirements.txt
python flask_web_server.py        # Access at http://localhost:5000
```

### Latest Web Version (v3.1)

```bash
cd "3.1 webapp"
pip install -r requirements.txt
python enhanced_flask_server.py    # Has more features but may have bugs
```

### Desktop GUI

```bash
cd "2.0 win app"
pip install -r requirements.txt
python gui2.py
```

### Docker Deployment

```bash
cd "2.6 webapp（流式传输测试版）"
docker-compose up -d
# Or for production with gunicorn:
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_web_server:app
```

## Architecture

### Codebase Structure

Multiple parallel version directories exist (1.0, 2.0, 2.5, 2.6, 3.1). The 2.6 webapp is the current stable production version. The 3.1 webapp adds multi-market support but has known bugs.

```
├── 2.0 win app/              # Desktop GUI (PyQt6)
│   ├── gui2.py               # Main GUI application
│   └── stock_analyzer.py     # Core analysis engine
├── 2.6 webapp（流式传输测试版）/  # Stable web version
│   ├── flask_web_server.py  # Flask server with SSE
│   └── web_stock_analyzer.py # Web-optimized analyzer
└── 3.1 webapp/               # Latest version (has bugs)
    ├── enhanced_flask_server.py
    └── enhanced_web_stock_analyzer.py
```

### Key Components

**Flask Server** (`flask_web_server.py` / `enhanced_flask_server.py`):
- SSE (Server-Sent Events) manager for real-time streaming of analysis progress
- ThreadPoolExecutor (4 workers) for concurrent task processing
- Password authentication via session management
- Task queue system with `analysis_tasks` and `task_results` dictionaries
- API endpoints: `/api/status`, `/api/sse`, `/api/analyze_stream`, `/api/batch_analyze_stream`

**Stock Analyzers** (`*_stock_analyzer.py`):
- `EnhancedStockAnalyzer` (desktop) / `WebStockAnalyzer` (2.6) / `EnhancedWebStockAnalyzer` (3.1)
- Multi-tier caching: `price_cache`, `fundamental_cache`, `news_cache` with configurable TTL
- Configurable analysis weights for technical, fundamental, and sentiment scoring
- Supports custom prompts with template variable substitution

**Data Sources**:
- Market data via `akshare` library
- AI providers: OpenAI (GPT), Anthropic (Claude), 智谱AI (ChatGLM)
- Fallback to rule-based analysis when AI is unavailable

### Configuration

All configuration is in `config.json`. Key sections:
- `api_keys`: AI provider keys
- `ai`: Model preferences, temperature, max_tokens
- `analysis_weights`: Technical/fundamental/sentiment ratios
- `markets`: A-stock/HK-stock/US-stock settings
- `cache`: Price/fundamental/news cache duration in hours
- `streaming`: SSE behavior (enabled, delay, show_thinking)
- `web_auth`: Password protection settings

Custom prompt templates use variables like `{{stock_code}}`, `{{stock_name}}`, `{{technical_score}}`, `{{financial_text}}`, `{{news_content}}`, etc.

## Important Notes

- 3.1 webapp has known bugs; use 2.6 webapp for production
- Mirror PyPI: `https://pypi.tuna.tsinghua.edu.cn/simple/`
- SSE events: `connected`, `log`, `progress`, `scores_update`, `final_result`, `ai_stream`
- NaN values must be cleaned before JSON serialization
- API keys should never be committed; use environment variables or local config