# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Chain-of-Thought Hub is a comprehensive evaluation framework for measuring Large Language Models' reasoning performance across complex benchmarks. It focuses on evaluating models' capabilities on reasoning-intensive tasks like mathematics, symbolic reasoning, knowledge questions, and coding.

The repository is organized by benchmark datasets, each with its own evaluation scripts supporting multiple model families (OpenAI GPT, Anthropic Claude, LLaMA, Falcon, etc.).

## Common Development Commands

### Setup
```bash
# Install dependencies (Python 3.8+ recommended)
cd MMLU
pip install -r requirements.txt

# Create outputs directory for results
mkdir outputs
```

### Running Evaluations

**MMLU (Multi-discipline Knowledge)**
```bash
cd MMLU

# OpenAI models
python run_mmlu_gpt_3.5_turbo.py --api_key=${API_KEY}
python run_mmlu_gpt_4_turbo.py --api_key=${API_KEY}

# Anthropic Claude
python run_mmlu_claude.py --api_key=${API_KEY} --engine=claude-v1.3

# Open-source models (LLaMA, Falcon)
python run_mmlu_open_source.py \
  --ckpt_dir ${LLAMA_CKPT_DIR} \
  --param_size 65 \  # 7, 13, 33, or 65
  --model_type llama  # or "falcon"
```

**GSM8K (Grade School Math)**
```bash
cd gsm8k

# Claude evaluation
python run_gsm8k_claude.py \
  --anthropic_key=${API_KEY} \
  --prompt_file=lib_prompt/prompt_original.txt \
  --engine=claude-v1.3 \
  --output_file=outputs/gsm8k_claude_v1.3_original_test.txt

# Jupyter notebooks for other models
jupyter notebook codex_gsm8k_complex.ipynb         # code-davinci-002
jupyter notebook gpt3.5turbo_gsm8k_complex.ipynb   # gpt-3.5-turbo
jupyter notebook flan_t5_11b_gsm8k.ipynb           # FlanT5
```

**BBH (Big-Bench Hard)**
```bash
cd BBH

# Run specific dataset
cd penguins
jupyter notebook gpt3.5trubo_penguins_original.ipynb

# Run all datasets
API_KEY=<your_api_key>
TASK=<all | multiple_choice | free_form>
python run_bbh_gpt_3.5_turbo.py --api_key=${API_KEY} --task=${TASK}
python run_bbh_claude_v1.3.py --api_key=${API_KEY} --model_index=claude-v1.3 --task=${TASK}
```

### Environment Variables
- `API_KEY`: OpenAI API key
- `ANTHROPIC_KEY`: Anthropic API key
- `LLAMA_CKPT_DIR`: Path to LLaMA model checkpoints

## Code Architecture

### Benchmark Structure
Each benchmark directory follows a consistent pattern:
- **MMLU/**: 57 subject knowledge evaluation (`utils.py` for answer extraction)
- **GSM8K/**: Math word problems with chain-of-thought prompting (`lib_prompt/` for standardized prompts)
- **BBH/**: 23 symbolic/text reasoning subsets
- **MATH/**: Competition-level math (notebooks for analysis)
- **spl/**: Standard Prompt Library (see below)

### Model Evaluation Pattern
Most evaluation scripts follow this structure:
1. Load model (via API or local checkpoint)
2. Load benchmark dataset
3. Apply standardized prompt from SPL
4. Generate predictions with chain-of-thought
5. Extract final answer using task-specific utility function
6. Calculate accuracy metrics

### Key Files
- **MMLU/utils.py:1**: Answer extraction utilities (e.g., `test_answer_mmlu_()`)
- **spl/readme.md:1**: Standard Prompt Library documentation
- **spl/spl.py:1**: Prompt loading utilities (`load_prompt()`)
- **gsm8k/lib_prompt/prompt_original.txt:1**: Standard GSM8K few-shot CoT prompt

### Standard Prompt Library (SPL)
The `spl/` directory provides standardized prompts following this schema:

| Format | Model Type | Task Type | Scale | Audience |
|--------|-----------|-----------|-------|----------|
| Few-shot CoT (.chatml) | Chatbot | Reasoning | Large | Developer |
| Zero-shot CoT (.chatml) | Chatbot | Reasoning | Large | User |
| Few-shot Direct (.chatml) | Chatbot | Knowledge | Any | Developer |
| Zero-shot Direct (.chatml) | Chatbot | Knowledge | Any | User |
| Few-shot CoT (.txt) | Completion | Reasoning | Large | Developer |
| Zero-shot CoT (.txt) | Completion | Reasoning | Large | User |

ChatML format follows [OpenAI's specification](https://github.com/openai/openai-python/blob/main/chatml.md).

### Research Extensions
The `research/` directory contains experimental prompting techniques:
- **complexity_based_prompting/**: Advanced prompt engineering methods
- **tree_of_thoughts/**: Tree-based reasoning exploration
- **MATH_tools/**: Math-specific tools and analysis

## Benchmark Categories

**Main Benchmarks** (stable, widely referenced):
- GSM8K: Grade-level math word problems
- MATH: Competition-level math/science
- MMLU: Multi-discipline knowledge (57 subjects)
- BBH: Challenging reasoning (23 subsets)
- HumanEval: Python coding
- C-Eval: Chinese knowledge test

**Experimental Benchmarks**:
- TheoremQA: Theorem proving
- SummEdits: Factual reasoning

**Long-Context Benchmarks**:
- Qspr: Research paper QA
- QALT: Long article questions
- BkSS: Novel summary ordering

## Important Notes

1. **Answer Extraction**: Each benchmark has task-specific answer extraction logic in `utils.py`. Models must follow the prompt format ending with "the answer is (X)" to enable proper extraction.

2. **Prompt Sensitivity**: LLM performance is highly sensitive to prompt formatting. Always use standardized prompts from SPL for reproducibility.

3. **Model Types**:
   - **Base**: Pretrained checkpoints (e.g., LLaMA 65B)
   - **SIFT**: Supervised instruction-finetuned (e.g., Alpaca, Vicuna)
   - **RLHF**: Reinforcement learning from human feedback (e.g., GPT-3.5, Claude)

4. **Performance Considerations**:
   - Open-source models (LLaMA, Falcon) require significant GPU memory
   - API-based evaluations (GPT, Claude) require rate limiting handling
   - Tensor parallelism available via `tensor_parallel` library

5. **Results Directory**: Always create `outputs/` directory before running evaluations to store results.

## Resources

- Main README: `/home/ubuntu/deploy-projects/1a1d5b5db26bf37f2b76562b/readme.md`
- SPL Documentation: `/home/ubuntu/deploy-projects/1a1d5b5db26bf37f2b76562b/spl/readme.md`
- Experimental Research: `/home/ubuntu/deploy-projects/1a1d5b5db26bf37f2b76562b/research/readme_exp.md`
- Literature Review: `/home/ubuntu/deploy-projects/1a1d5b5db26bf37f2b76562b/resources/literature.md`
- TODO List: `/home/ubuntu/deploy-projects/1a1d5b5db26bf37f2b76562b/resources/todo.md`