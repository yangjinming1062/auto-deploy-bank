# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Microsoft's **Generative AI for Beginners** educational course - a 21-lesson curriculum teaching how to build Generative AI applications. Each lesson is self-contained with theory (README.md), code examples (Python/TypeScript), and Jupyter notebooks.

## Build, Test, and Run Commands

### Python Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Python examples
python <lesson-dir>/python/<example-name>.py
```

### TypeScript Setup
```bash
# Navigate to lesson app directory
cd 06-text-generation-apps/typescript/recipe-app

# Install dependencies and build
npm install
npm run build

# Run the application
npm start
```

### Jupyter Notebooks
```bash
# Start Jupyter from repository root
jupyter notebook
```

### Dev Container (Recommended)
Open in GitHub Codespaces or VS Code with Dev Containers extension - dependencies install automatically.

## Architecture

**Lesson Structure** (00-course-setup through 21-meta):
- Each numbered directory contains a `README.md` with theory and walkthroughs
- Code examples organized by language: `python/`, `typescript/`
- Prefix convention: `aoai-` (Azure OpenAI), `oai-` (OpenAI), `githubmodels-` (GitHub Models)
- Some lessons include `.ipynb` Jupyter notebooks

**API Providers Supported**:
- Azure OpenAI Service (`AZURE_OPENAI_*` env vars)
- OpenAI API (`OPENAI_API_KEY`)
- GitHub Models (`GITHUB_TOKEN`)

**Environment Variables**:
Copy `.env.copy` to `.env` and fill in API keys. Key variables:
- `OPENAI_API_KEY`
- `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`
- `AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT`

## Contribution Guidelines

**Markdown Formatting Rules** (enforced by GitHub Actions):
- All URLs: `[text](url)` format with no extra spaces
- Relative links: must start with `./` or `../` and include tracking ID: `./path?WT.mc_id=academic-105485-koreyst`
- Microsoft domain URLs (`github.com`, `microsoft.com`, `aka.ms`, etc.): must include tracking ID
- No country locale in URLs (avoid `/en-us/`, `/en/`)
- Images: `./images/` folder, English characters in filenames

**Pull Request Workflow**:
1. Fork repository before making changes
2. PRs auto-validate: broken links, missing tracking IDs, country locale
3. Keep PRs focused - one logical change per PR
4. Sign Microsoft CLA (automatic on first PR)

## Key Files

- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies for TypeScript examples
- `.env.copy` - Environment variable template
- `AGENTS.md` - Detailed development guide (reference this for comprehensive info)