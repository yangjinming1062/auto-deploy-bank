# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Paper-to-Podcast transforms academic research papers into engaging three-person podcast discussions. It uses LLMs to generate scripts and OpenAI's TTS API to produce audio.

## Commands

### Setup
```bash
# Install dependencies with Poetry
poetry install

# Or with pip
pip install -r requirements.txt
```

### Running the App
```bash
python paper_to_podcast.py path/to/research_paper.pdf
```

Requires an `OPENAI_API_KEY` in `.env` file.

## Architecture

The project uses a **3-chain LangChain pipeline** to generate podcast scripts:

1. **Plan Chain** (`plan_prompt`) - Generates a structural plan of the paper with sections and bullet points
2. **Discussion Chain** (`discuss_prompt_template`) - RAG-based chain that generates dialogue for each section using Chroma vectorstore for context retrieval
3. **Enhance Chain** (`enhance_prompt`) - Removes redundancies, audio effects, and refines transitions

### Core Files

- **`paper_to_podcast.py`**: Entry point. Initializes LLM chains, orchestrates script generation, and calls TTS.
- **`templates.py`**: Defines all LangChain prompt templates for the three-chain pipeline.
- **`utils/script.py`**: Handles PDF parsing, script generation orchestration, and RAG chain setup.
- **`utils/audio_gen.py`**: TTS generation using OpenAI API (voices: alloy=Host, nova=Learner, fable=Expert).

### Three-Persona Structure

- **Host**: Professional, warm introductions and transitions (voice: alloy)
- **Learner**: Asks questions, curious and friendly (voice: nova)
- **Expert**: Provides deep insights, speaks less (voice: fable)

### Processing Flow

1. PDF text is extracted up to content after "Conclusion"
2. Plan chain generates paper outline
3. Initial dialogue generated from paper head (before "Introduction")
4. For each section: RAG chain generates dialogue using retrieved context
5. Enhance chain cleans up the full script
6. TTS generates per-speaker audio files and merges them

## Dependencies

- **langchain**: LLM orchestration with prompt templates and chains
- **langchain_chroma**: Vectorstore for RAG context retrieval
- **openai**: LLM and TTS API access
- **pydub**: Audio file merging
- **PyPDF2**: PDF text extraction

## Notes

- Uses `gpt-4o-mini` as the default LLM for cost efficiency
- Temporary files (`text_paper_*.txt`, `podcast_*/`) are gitignored
- The RAG retriever is rebuilt each run from the parsed PDF text