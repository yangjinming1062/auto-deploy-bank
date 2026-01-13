# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚀 Quick Start Commands

### Installation & Setup
```bash
# Clone and setup
git clone https://github.com/itsOwen/CyberScraper-2077.git
cd CyberScraper-2077

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Set API keys (choose based on model preference)
export OPENAI_API_KEY="your-api-key"
export GOOGLE_API_KEY="your-api-key"
```

### Running the Application
```bash
# Start Streamlit web interface
streamlit run main.py

# App will be available at http://localhost:8501
```

### Docker Development
```bash
# Build Docker image
docker build -t cyberscraper-2077 .

# Run container
docker run -p 8501:8501 -e OPENAI_API_KEY="your-key" cyberscraper-2077
```

### Using Ollama
```bash
# Install and setup Ollama
pip install ollama
ollama pull llama3.1  # or other model

# Run with host network access to Ollama
docker run -e OLLAMA_BASE_URL=http://host.docker.internal:11434 -p 8501:8501 cyberscraper-2077
```

## 🏗️ High-Level Architecture

### Core Components

**Main Entry Point: `main.py`**
- Streamlit application entry point
- Handles OAuth callbacks for Google Sheets integration
- Manages chat history serialization
- Initializes WebScraperChat instance

**Streamlit UI Layer: `app/`**
- `streamlit_web_scraper_chat.py`: Main Streamlit handler that bridges UI and WebExtractor
- `ui_components.py`: UI components and data formatting
- `utils.py`: Loading animations and UI utilities

**Core Engine: `src/web_extractor.py`**
- Central orchestrator class (`WebExtractor`)
- Handles URL parsing, multi-page scraping, and AI model integration
- Implements caching (LRU) for API responses
- Supports multiple scraping strategies:
  - PlaywrightScraper (JavaScript-rendered pages)
  - HTMLScraper (static HTML)
  - JSONScraper (API endpoints)
  - TorScraper (.onion sites)

**Scraper Implementations: `src/scrapers/`**
- `base_scraper.py`: Abstract base class defining scraper interface
- `playwright_scraper.py`: Primary scraper using Playwright with stealth mode
- `html_scraper.py`: Simple HTML content extraction
- `json_scraper.py`: JSON API endpoint scraping
- `tor/`: Tor network integration
  - `tor_scraper.py`: Tor-based scraping for .onion sites
  - `tor_config.py`: Tor configuration management
  - `tor_manager.py`: Tor process lifecycle management

**AI Models: `src/models.py` & `src/ollama_models.py`**
- Factory pattern for AI model instantiation
- Support for OpenAI (GPT-4, GPT-3.5), Google Gemini, and local Ollama models
- Dynamic model selection via string names

**Prompt Templates: `src/prompts.py`**
- Model-specific prompt templates for data extraction
- Customizable prompts for different AI backends

**Utilities: `src/utils/`**
- `markdown_formatter.py`: Data formatting and export
- `proxy_manager.py`: Proxy configuration
- `google_sheets_utils.py`: Google Sheets API integration

### Data Flow

1. **User Input** → Streamlit UI (`main.py`, `streamlit_web_scraper_chat.py`)
2. **URL/Query Processing** → `WebExtractor.process_query()` (`src/web_extractor.py`)
3. **Content Fetching** → Appropriate scraper (Playwright/HTML/JSON/Tor)
4. **Content Preprocessing** → HTML cleaning, text extraction, chunking
5. **AI Extraction** → LangChain chains with model-specific prompts (`src/prompts.py`)
6. **Response Formatting** → JSON/CSV/Excel/Google Sheets export

### Key Configuration Classes

**ScraperConfig** (`src/scrapers/playwright_scraper.py`): Configures browser behavior
```python
use_stealth: bool = True        # Bypass bot detection
simulate_human: bool = False    # Human-like interactions
use_custom_headers: bool = True # Custom request headers
hide_webdriver: bool = True     # Hide automation signs
bypass_cloudflare: bool = True  # Cloudflare bypass
```

**TorConfig** (`src/scrapers/tor/tor_config.py`): Tor network settings
```python
socks_port: int = 9050          # Tor SOCKS proxy port
circuit_timeout: int = 10       # Circuit creation timeout
auto_renew_circuit: bool = True # Auto-renew Tor circuits
verify_connection: bool = True  # Verify Tor before scraping
```

### Multi-Page Scraping (BETA)

Supports paginated content extraction:
- **Format**: `URL 1-5` or `URL 1-5,7,9-12` or custom ranges
- **Pattern Detection**: Automatic URL pattern detection for common pagination formats
- **Manual Patterns**: Use `{page}` placeholder for custom structures

## 🎯 Development Notes

### Project Structure
```
CyberScraper-2077/
├── main.py                     # Streamlit entry point
├── app/                        # Streamlit UI layer
│   ├── streamlit_web_scraper_chat.py
│   ├── ui_components.py
│   └── utils.py
├── src/                        # Core scraping engine
│   ├── web_extractor.py        # Main orchestrator
│   ├── models.py               # AI model factory
│   ├── ollama_models.py        # Ollama integration
│   ├── prompts.py              # AI prompts
│   ├── scrapers/               # Scraping implementations
│   │   ├── base_scraper.py
│   │   ├── playwright_scraper.py
│   │   ├── html_scraper.py
│   │   ├── json_scraper.py
│   │   └── tor/
│   └── utils/                  # Utilities
│       ├── markdown_formatter.py
│       ├── proxy_manager.py
│       └── google_sheets_utils.py
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Full documentation
```

### Key Dependencies
- **Streamlit**: Web UI framework
- **Playwright**: Browser automation for JavaScript rendering
- **LangChain**: AI model integration and prompt chains
- **OpenAI/Gemini**: Primary AI models for data extraction
- **Ollama**: Local LLM support
- **BeautifulSoup**: HTML parsing
- **Pandas**: Data manipulation and export
- **PySocks/requests[socks]**: Tor network support

### Testing
No formal test suite detected. Follow patterns in `CONTRIBUTING.md`:
- Write tests for new features
- Follow conventional commit messages
- PEP 8 compliance with type hints

### Common Development Tasks

**Adding New Scraper:**
1. Inherit from `BaseScraper` (`src/scrapers/base_scraper.py`)
2. Implement `fetch_content()` and `extract()` methods
3. Register in `WebExtractor` initialization (`src/web_extractor.py`)

**Adding New AI Model:**
1. Add to `Models.get_model()` factory (`src/models.py`)
2. Create prompt template in `src/prompts.py`
3. Update model selection UI

**Configuration Changes:**
- Modify `ScraperConfig` class in `playwright_scraper.py` for browser settings
- Modify `TorConfig` in `tor/tor_config.py` for Tor settings

### Environment Variables
Required:
- `OPENAI_API_KEY`: OpenAI API key
- `GOOGLE_API_KEY`: Google/Gemini API key

Optional:
- `OLLAMA_BASE_URL`: Ollama server URL (for Docker)
- `SCRAPELESS_API_KEY`: Scrapeless SDK key (for Scrapeless branch)

### Important Files to Review
- `src/web_extractor.py`: Main logic and multi-page scraping
- `src/scrapers/playwright_scraper.py`: Primary scraping logic with stealth features
- `src/prompts.py`: Data extraction prompts (customizable for better results)
- `src/utils/google_sheets_utils.py`: Google Sheets upload functionality
- `main.py`: Streamlit entry point and OAuth handling

### Security Considerations
- Tor integration automatically handles .onion URLs
- Stealth mode enabled by default in PlaywrightScraper
- CAPTCHA bypass available via `-captcha` URL parameter
- Custom headers mimic legitimate browsers

### Troubleshooting
- **Bot Detection**: Adjust `ScraperConfig` settings (stealth, simulate_human)
- **CAPTCHA Issues**: Use current browser mode or `-captcha` parameter
- **Tor Issues**: Ensure Tor service is running (`service tor start`)
- **Ollama Connection**: Verify `OLLAMA_BASE_URL` in Docker
- **Multi-Page Failures**: Try explicit URL patterns with `{page}` placeholder