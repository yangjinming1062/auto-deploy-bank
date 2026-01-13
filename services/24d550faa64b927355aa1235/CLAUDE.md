# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

### Run Full Pipeline (Recommended)
```bash
python -m workflow.full_pipeline_runner --objective "your task goal here"
```

Optional flags:
- `--context "additional context"` - Add supplementary context
- `--finish-dir path` - Custom output directory for collaboration forms
- `--template path` - Custom template file path
- `--api-key KEY` - Override DeepSeek API key (otherwise reads from .env)
- `--model MODEL` - Change model (default: deepseek-chat)
- `--reasoning-effort low|medium|high` - Control reasoning intensity
- `--no-strategy-auto-apply` - Disable auto-writing to strategy library
- `--auto-apply-capability` - Enable auto-writing to capability library
- `--tool-catalog "foo,bar"` - Comma-separated tool catalog

### Run Individual Stages (Debugging)
```bash
python -m stage1_agent.main          # Stage 1: Metacognitive Analysis
python -m stage2_candidate_agent.main # Stage 2-A: Candidate Strategy Selection
python -m stage2_agent.main          # Stage 2 (Full 2A→2B→2C pipeline)
python -m stage2_capability_upgrade_agent.main # Stage 2-C: Strategy Library Upgrade
python -m stage3_agent.main          # Stage 3: Execution Step Planning
python -m stage4_agent.main          # Stage 4: Execution & Review
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
pytest test/ -v
```

## Environment Configuration

Create a `.env` file in the project root with:
```env
DEEPSEEK_API_KEY=your_deepseek_key_here
TAVILY_API_KEY=your_tavily_key_here
```

## High-Level Architecture

This is a **document-driven multi-agent framework** that transforms complex problem-solving into a transparent, file-based workflow.

### Core Design Philosophy
- **Context Engineering is File-Based**: All prompts, strategies, capabilities, and execution plans live in Markdown files rather than hardcoded strings
- **Agent Collaboration via Documents**: Agents communicate through shared `finish_form/*.md` files with marker-block sections
- **No Vector Database**: Context retrieval uses file paths, Markdown structure, and marker blocks (not embeddings)
- **Transparent Multi-Stage Pipeline**: Each stage's reasoning is visible in the collaboration form

### Pipeline Flow

1. **Template Generation** (`Document_Checking/template_generation.py`)
   - Ensures sufficient collaboration form templates exist in `finish_form/`
   - Maintains document index for the current task

2. **Stage 1: Metacognitive Analysis** (`stage1_agent/`)
   - Analyzes task requirements and capability needs
   - References `ability_library/core_capabilities.md` (A1–H2 codes)
   - Outputs to collaboration form Stage 1 section

3. **Stage 2-A: Candidate Strategy Selection** (`stage2_candidate_agent/`)
   - Selects 2–3 candidate strategies from `strategy_library/strategy.md`
   - References strategy codes (P1, I2, D1, etc.)

4. **Stage 2-B: Strategy Refinement** (`stage2_agent/`)
   - Critiques and potentially fuses candidate strategies
   - Produces a refined strategy with handover notes

5. **Stage 2-C: Strategy Library Upgrade** (`stage2_capability_upgrade_agent/`)
   - Evaluates whether new strategies should be added to the library
   - Auto-writes to `strategy_library/strategy.md` (if enabled)

6. **Stage 3: Execution Planning** (`stage3_agent/`)
   - Breaks refined strategy into actionable steps
   - Maps tool usage from `tools/tool_catalog.md`
   - References MCP tools in `MCP/` directory

7. **Stage 4: Execution & Review** (`stage4_agent/`)
   - Executes the plan step-by-step
   - Records actual results and deviations
   - Provides final answer and retrospective

8. **Capability Library Upgrade** (`capability_upgrade_agent/`)
   - Evaluates if new capabilities should be added to `ability_library/`
   - Does not auto-write by default

### Key Data Flow Pattern

```
User Input → Template Selection → Stage 1 Analysis
         → Strategy Selection → Stage 2-B Refinement
         → Stage 2-C Library Upgrade (optional)
         → Stage 3 Step Planning
         → Stage 4 Execution & Results
```

All stages write to a single collaboration form (`finish_form/*.md`) using HTML comment markers like `<!-- STAGE1_ANALYSIS_START -->` for section isolation.

## Key Components

### Document-Driven Context
- **Collaboration Forms**: `finish_form/*.md` - Shared workspace for all agents
- **Standard Template**: `form_templates/standard template.md` - Defines form structure
- **Marker Blocks**: HTML comments delimit sections for clean overwrites
- **Document Utils**: `workflow/finish_form_utils.py` - Handles marker-based section updates

### Knowledge Libraries
- **Capability Library**: `ability_library/core_capabilities.md` - Organized A1–H2 capability taxonomy
- **Strategy Library**: `strategy_library/strategy.md` - Strategy patterns (P/I/X/C/F/D/E/L categories)

### Model Abstraction
- **Base Interface**: `model/_model_base.py` - Unified `ChatModelBase` for all models
- **DeepSeek Implementation**: `model/_deepseek_model.py` - Primary backend
- **OpenAI Implementation**: `model/_openai_model.py` - Alternative with tool calling support
- **Response Structure**: `model/_model_response.py` - Standardized output format

### MCP Tools Integration
- **Tavily Search**: `MCP/tavily.py` - Web search capability
- **Code Interpreter**: `MCP/code_interpreter.py` - Code execution
- **Tool Documentation**: `MCP/tool.md` - How to use tools in stages
- **Tool Catalog**: `tools/tool_catalog.md` - Available tools list for Stage 3/4

### Testing
Test files in `test/` directory:
- `test_capability_upgrade_agent.py` - Capability library upgrade tests
- `test_strategy_selection_workflow.py` - Stage 2 workflow tests
- `test_stage2_capability_upgrade_agent.py` - Strategy library upgrade tests
- `test_capability_workflow.py` - General capability workflow tests
- `test_envelope.py` - Agent envelope/integration tests

## Important Notes

- **DeepSeek is Default Model**: Uses `deepseek-chat` with reasoning_effort support
- **Document-First Development**: Modify `.md` files in `ability_library/`, `strategy_library/`, or templates rather than hardcoded prompts
- **Marker Block Discipline**: When editing collaboration forms, respect HTML comment markers to avoid corrupting section isolation
- **Stage Separation**: Each stage has its own agent code, prompt file (`.md`), and CLI entry point
- **MCP Tools Require Configuration**: Tavily and other tools need API keys in `.env`

## Common Development Tasks

### Modify Agent Behavior
1. Find the relevant agent: `stage*_agent/<Name>_agent.py`
2. Update prompt: `stage*_agent/*.md`
3. Test individually: `python -m stage*_agent.main`
4. Test full pipeline: `python -m workflow.full_pipeline_runner`

### Add New Capability/Strategy
1. Run full pipeline with the task
2. Review upgrade suggestions from Stage 2-C or Capability Upgrade Agent
3. Upgrade Agent provides markdown patches ready to apply
4. Or manually edit `ability_library/core_capabilities.md` or `strategy_library/strategy.md`

### Debug Pipeline Issues
1. Run individual stages to isolate problems
2. Check collaboration form output: `finish_form/auto_generated_template_*.md`
3. Verify API keys in `.env`
4. Review stage-specific prompt files for context issues

### Test New Model
1. Update `--model` and `--base-url` flags
2. Ensure model implements `ChatModelBase` interface
3. Test with single stage first: `python -m stage1_agent.main --model your-model`