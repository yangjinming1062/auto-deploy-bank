# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is an **Awesome-llm-and-aigc** collection - a curated repository of Large Language Model (LLM) and AI Generated Content resources. It contains links, documentation, and example code related to:
- LLM frameworks and libraries (LangChain, LlamaIndex, vLLM, etc.)
- RAG (Retrieval-Augmented Generation) systems
- Agent frameworks (AutoGen, CrewAI, etc.)
- Model fine-tuning and deployment
- Vector databases and embeddings
- Multimodal models and applications
- Papers, blogs, videos, and learning resources

## Repository Structure

```
/                      # Root directory
├── README.md          # Main curated list (~2000 lines, categorized resources)
├── *.md               # ~145+ topic-specific markdown files
├── langchain/         # LangChain examples and patterns
├── llama-index/       # LlamaIndex examples and patterns
├── RAG/               # RAG-related code and notebooks
├── transformers/      # Hugging Face transformers examples
├── Autogen/           # AutoGen agent framework examples
├── crew-ai-examples/  # CrewAI agent examples
├── and ~50 other topic directories with code examples
```

## Content Types

1. **Root markdown files** (e.g., `vLLM.md`, `langchain.md`): Curated links to articles, tutorials, and resources about specific topics
2. **Topic directories**: Contain Python example code for working with LLM frameworks
3. **README.md**: Main index with categorized links to projects, papers, blogs, and videos

## No Build/Test Commands

This is a **documentation and resource collection repository**, not a software project. There are no:
- Build commands
- Test commands
- Package.json or requirements.txt for the repository itself
- Linting/formatting commands

Each example directory may have its own dependencies if you need to run specific code.

## Working with This Repository

- **Adding new resources**: Create or update markdown files with relevant links, using the existing format (one link per line with description)
- **Topic organization**: Resources are organized by technology/framework (e.g., `vLLM.md` for vLLM topics, `RAG.md` may not exist - check root)
- **Example code**: Python code in topic directories demonstrates practical implementations using LLM libraries

## File Format Conventions

- Markdown files use simple link lists: `[Description](URL)` on individual lines
- No frontmatter or special formatting required in markdown files
- Example code uses standard Python with libraries like LangChain, LlamaIndex, etc.