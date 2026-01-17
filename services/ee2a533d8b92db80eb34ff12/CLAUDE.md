# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Podcast Copilot is a demo application that generates LinkedIn social media posts for podcast episodes. It orchestrates multiple ML models via LangChain in an 8-step pipeline:

1. **Whisper** (local) - Transcribe podcast audio to text
2. **Dolly 2** (local) - Extract guest name from transcript
3. **Bing Search API** (cloud) - Retrieve guest biography
4. **GPT-4** (Azure OpenAI) - Generate social media copy from transcript + bio
5. **GPT-4** (Azure OpenAI) - Create DALL-E image prompt
6. **DALL-E 2** (Azure OpenAI) - Generate promotional image
7. **LinkedIn Plugin** - Post to LinkedIn (requires plugin-capable model)

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the podcast copilot
python PodcastSocialMediaCopilot.py
```

## Architecture

- **PodcastSocialMediaCopilot.py**: Main entry point orchestrating the LangChain pipeline. Uses TransformChain, LLMChain, and SequentialChain components.
- **instruct_pipeline.py**: Custom HuggingFace pipeline wrapper for Dolly 2 instruction-following model. Handles special token parsing for "### Instruction:" / "### Response:" / "### End" markers.
- **dalle_helper.py**: ImageClient class wrapping DALL-E REST API with async polling for image generation completion.

## Configuration Required

Before running, edit `PodcastSocialMediaCopilot.py` and set:
- `bing_subscription_key`: Azure Bing Search API key
- `openai_api_base`: Azure OpenAI endpoint (e.g., `https://RESOURCE_NAME.openai.azure.com/`)
- `openai_api_key`: Azure OpenAI API key
- `gpt4_deployment_name`: GPT-4 deployment name
- `podcast_audio_file`: Path to podcast MP3 (defaults to `./PodcastSnippet.mp3`)

## Dependencies

Key libraries: torch, transformers, optimum, onnx, openai-whisper, langchain, pydub, openai, ffmpeg-python, onnxruntime-directml.

## Local vs Cloud Models

- Whisper and Dolly 2 run locally using ONNX Runtime DirectML
- Bing Search, GPT-4, DALL-E, and LinkedIn plugin use Azure cloud APIs