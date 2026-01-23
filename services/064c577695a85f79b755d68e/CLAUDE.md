# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is **Awesome-AGI**, a curated knowledge repository focused on Large Language Models (LLMs), AGI, RAG (Retrieval-Augmented Generation), Agent frameworks, and LLM application development. The repository contains:

- Curated links to papers, blogs, and code resources
- Jupyter notebooks with practical implementation examples
- Python code examples for LLM APIs, RAG pipelines, and Agent applications
- Framework-specific tutorials (LangChain, LlamaIndex, etc.)

## Repository Structure

| Directory | Purpose |
|-----------|---------|
| `LLM API/` | API calling examples for various LLMs (OpenAI, Qwen, LLaMA, Baichuan, Gemini, etc.) |
| `LLM Pipeline/` | Model fine-tuning (LLaMA_Factory, trl), deployment (FastChat, Xinference), evaluation |
| `LangChain/` | LangChain tutorials, LangGraph, LangServe, LangSmith, LangFuse integration examples |
| `LlamaIndex/` | LlamaIndex implementation examples and tutorials |
| `RAG/` | RAG implementations (LangChain_RAG, LlamaIndex_RAG), vector databases, chunking strategies, embedding models, RAG evaluation |
| `Agent/` | Agent frameworks: AutoGen, MetaGPT, LangChain_Agent, LangGraph_Agent, Swarm |
| `Prompt/` | Prompt engineering resources and techniques |
| `MCP/` | Model Context Protocol implementations |
| `NL2SQL/` | Text-to-SQL resources and examples |
| `WEB Framework/` | Web frameworks for building LLM applications |
| `DataSet/` | Dataset resources for LLM pre-training and fine-tuning |

## Key Patterns

- **No traditional build/test commands**: This is primarily a knowledge curation repository with implementation examples
- **Framework-centric**: Most code examples use LangChain, LlamaIndex, or similar LLM application frameworks
- **Notebook-first**: Many practical examples are provided as Jupyter notebooks (`.ipynb`)
- **External resources**: The repository references external papers, blogs, and code repositories rather than containing original implementations

## Primary Use Cases

1. **Learning LLM development** - Understanding how to build LLM applications with popular frameworks
2. **RAG implementation** - Building retrieval-augmented generation systems with various vector databases and chunking strategies
3. **Agent development** - Creating autonomous agents using frameworks like AutoGen, MetaGPT, LangGraph
4. **Model fine-tuning** - Fine-tuning LLMs using PEFT techniques (LoRA, QLoRA, etc.)
5. **LLM API integration** - Calling various LLM APIs (OpenAI-compatible, domestic models like Qwen, Baichuan, etc.)

## Language

This repository contains predominantly **Chinese documentation** and resource links, with some English code comments and examples.