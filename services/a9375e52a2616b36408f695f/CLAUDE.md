# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**myGPTReader** is a ChatGPT-powered Slack bot that reads and summarizes web content, documents, and videos. It features voice interaction, daily news aggregation, and multi-language support (Chinese, English, German, Japanese).

**Architecture**: Python Flask backend (Slack bot) + React marketing site, deployed on Fly.io with GitHub Actions CI/CD.

## Common Development Commands

### Python Backend (app/)

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app/server.py

# Run with production server (as configured in Procfile)
gunicorn app.server:app
```

### React Frontend (web/landing/www/)

```bash
cd web/landing/www

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Lint and format code
npm run format

# Run tests (React standard - no backend tests exist)
npm test
```

### Deployment

The app is deployed on **Fly.io** via GitHub Actions (`.github/workflows/fly.yml`). Push to `main` triggers automatic deployment.

## Code Architecture

### Backend Structure (app/)

| File | Purpose |
|------|---------|
| **server.py** (542 lines) | Main Flask app initialization, Slack bot setup, thread history management, scheduled jobs |
| **gpt.py** (220 lines) | Core AI functionality - ChatGPT integration, LLaMA index management, web scraping, voice processing |
| **daily_hot_news.py** | Scheduled news aggregation from RSS feeds with ChatGPT summarization |
| **slash_command.py** | Slack slash command handlers (/read, /ask, etc.) |
| **user.py** | User access control, rate limiting, premium user management |
| **rate_limiter.py** | API rate limiting to control costs |
| **fetch_web_post.py** | Web scraping utilities (requests, PhantomJS Cloud, YouTube transcripts) |
| **prompt.py** | ChatGPT prompt templates |
| **ttl_set.py** | TTL cache implementation |
| **util.py** | Utility functions (MD5, language detection, etc.) |
| **data/** | Configuration files (RSS feeds, prompts) |

### Key AI Workflows

1. **Web Content Summarization** (`gpt.py:64-84`):
   - Extract URLs from Slack message → scrape web content → build LLaMA index → query with ChatGPT

2. **Document Processing** (`gpt.py:94+`):
   - Upload file → extract text → build LLaMA index → query with ChatGPT
   - Supports: PDF, EPUB, DOCX, MD, TXT

3. **Voice Interaction** (`gpt.py:150+`):
   - Voice message → Whisper STT → ChatGPT → Azure TTS → respond with audio

4. **Daily News** (`daily_hot_news.py`):
   - Scheduled job (daily 1:30 AM) → aggregate RSS feeds → ChatGPT summarize → post to #daily-news

### Thread Context System (`server.py:88-100`)

The bot maintains conversation context by:
- Storing last 10 messages per thread
- Extracting URLs from messages
- Passing context to ChatGPT queries for contextual responses

### Index Caching (`gpt.py:24-35`)

```
/tmp/myGPTReader/cache_web/  - Web content indexes
/data/myGPTReader/file/      - File content indexes (persistent)
/tmp/myGPTReader/voice/      - Voice processing temp files
```

Indexes are cached by MD5 hash to avoid reprocessing same content.

## Configuration

### Required Environment Variables

```bash
OPENAI_API_KEY           # OpenAI API key
SLACK_TOKEN              # Slack Bot User OAuth Token
SLACK_SIGNING_SECRET     # Slack app signing secret
SPEECH_KEY               # Azure Speech Service key
SPEECH_REGION            # Azure Speech region
CF_ACCESS_CLIENT_ID      # Cloudflare Access (for web scraper)
CF_ACCESS_CLIENT_SECRET  # Cloudflare Access secret
PHANTOMJSCLOUD_API_KEY   # For JavaScript-heavy sites
```

See `.env_sample` for full list.

### Key Configurable Values

- **Channel whitelists** (`server.py`): `temp_whitelist_channle_id` for PDF access
- **File size limits** (`server.py`): `max_file_size` parameter
- **Rate limits** (`rate_limiter.py`): Configurable per-user daily limits
- **News schedule** (`server.py:60`): `hour=1, minute=30` for daily news

## Testing

**No automated tests exist for the Python backend** - this is a known gap. Only React has standard Create React App tests (`App.test.js`).

## Feature Roadmap

See `docs/TODO.md` for complete roadmap. Key incomplete items:
- Auto-collect good prompts to #gpt-prompt channel
- Fine-tune chunk size for cost optimization
- Image processing (GPT-4 Vision)
- User statistics and premium membership
- Azure OpenAI integration
- TypeScript migration
- GPT-4 model upgrade
- Slack marketplace publication

## Deployment Notes

- **Primary region**: Singapore (SIN)
- **Port**: 8080 (configured in `fly.toml`)
- **Persistent storage**: `/data/myGPTReader` mounted volume for file indexes
- **Health checks**: TCP checks every 10s
- **Concurrency**: 25 hard limit, 20 soft limit

## Documentation

- **README.md** - Main project documentation with feature showcase
- **docs/CDDR.md** (384KB) - Detailed development diary (AI-assisted development process)
- **docs/TODO.md** - Feature checklist and progress (114 items, ~85% complete)
- **docs/how-to-install/docker.md** - Docker deployment guide
- **docs/how-to-install/nigdaemon.md** - Additional deployment instructions

## Cost Optimization Features

The codebase implements several cost-saving measures:
- LLaMA index caching (avoid reprocessing same content)
- Rate limiting per user
- User whitelist for expensive features (file uploads)
- Premium user tiers for heavy usage
- Embedding caching (though OpenAI embeddings are used for quality)

## Web Scraping Strategy

The app uses multiple scraping methods:
1. **trafilatura/requests** - Standard websites
2. **PhantomJS Cloud** - JavaScript-heavy sites
3. **YouTube Transcript API** - Videos with subtitles
4. **Cloudflare Access** - Protected web scraper endpoint

## Important Development Notes

1. **Thread context is critical** - Bot reads thread history, so responses should maintain conversational continuity
2. **File access is restricted** - PDF and file uploads require channel/user whitelisting
3. **Cache first approach** - Always check existing LLaMA index before reprocessing
4. **Multilingual support** - Code handles Chinese/English/Japanese/German (see `insert_space()` in `server.py:70-86`)
5. **No Python tests** - Add test coverage for backend features when modifying
6. **Production uses gunicorn** - `Procfile` configures this, not Flask dev server