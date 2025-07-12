# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a fully prompt-based HSEARL research paper survey system. HSEARL (Human Structural Understanding and Translation) is a 6-parameter model for understanding human personality structure. The system automatically surveys AI/LLM papers related to HSEARL using Claude Code execution.

## Development Commands

### Package Management (uv required)
```bash
# Install dependencies
uv sync

# Add new package
uv add package_name

# Add dev dependency
uv add --dev package_name --upgrade-package package_name

# FORBIDDEN: uv pip install, @latest syntax
```

### Code Quality
```bash
# Format code
uv run --frozen ruff format .

# Check linting
uv run --frozen ruff check .

# Auto-fix linting issues
uv run --frozen ruff check . --fix

# Run tests
uv run --frozen pytest
```

### Pre-commit
```bash
# Install pre-commit hooks
uv run pre-commit install

# Pre-commit runs automatically on git commit with Ruff
```

### Docker Development
```bash
# Build and run
./docker/build.sh
./docker/run.sh

# Or with Docker Compose
docker compose build
docker compose up
```

## System Architecture

### Core Concept
This system is **completely prompt-based** - no Python automation scripts exist. All research tasks are executed by Claude Code following detailed prompt instructions:

1. **ArXiv Paper Search** → Claude Code execution
2. **Paper Summarization** → Claude Code execution  
3. **HSEARL Relevance Analysis** → Claude Code execution
4. **Innovative Idea Generation** → Claude Code execution

### Directory Structure
```
docs/
├── base/HSEARL（ハール）.md          # HSEARL framework definition
├── surveys/                          # Generated paper summaries
├── idea/                             # Generated innovative ideas
├── prompts/                          # Execution instruction prompts
│   ├── arxiv_search_prompt.md        # Paper search instructions
│   ├── paper_summary_prompt.md       # Summary generation instructions
│   ├── idea_generation_prompt.md     # Idea generation instructions
│   └── hsearl_research_pipeline.md   # Integrated execution pipeline
├── サーベイ予定論文リスト.md          # Pending papers queue
├── searched_papers.json              # Searched paper IDs tracking
├── processed_ideas.json              # Processed summaries tracking
└── search_stats.json                 # Search statistics
```

### HSEARL Framework
HSEARL consists of 6 hierarchical parameters:
- **H**ead (認知型): Cognitive/information processing style (MBTI-based)
- **S**elf (動機型): Motivation/fear patterns (Enneagram-based)  
- **E**motion (反応型): Emotional/thinking/instinct priorities (Tritype-based)
- **A**daptation (適応状態): Stress tolerance/self-awareness (Health levels)
- **R**oots (育ち): Early emotional wiring/family dynamics
- **L**ayer (ロール): External role performance/social positioning

## Claude Code Execution Instructions

### Primary Execution (Recommended)
```
docs/prompts/hsearl_research_pipeline.mdの統合実行手順書に従って、
HSEARL研究調査パイプラインを実行してください。

1. ArXiv論文検索
2. 論文サマリー生成
3. アイデア創出
4. 結果報告

各フェーズで適切なツール（WebSearch、WebFetch、Read、Write、Edit）を使用し、
HSEARLとの関連性を重視した高品質なアウトプットを生成してください。
```

### Individual Task Execution
#### Paper Search Only:
```
docs/prompts/arxiv_search_prompt.mdの手順書に従って、
HSEARL関連論文をArXivから検索し、サーベイ予定リストを更新してください。
```

#### Paper Summary Only:
```
docs/prompts/paper_summary_prompt.mdの手順書に従って、
サーベイ予定リストから1件の論文サマリーを生成してください。
```

#### Idea Generation Only:
```
docs/prompts/idea_generation_prompt.mdの手順書に従って、
未処理のサマリーからHSEARLアイデアを創出してください。
```

## Automation System

### GitHub Actions Flow
```
GitHub Actions (every 20 min) → System State Check → Issue Creation → Claude Code Execution
```

The system runs automatically every 20 minutes, checking for pending tasks and creating GitHub Issues with execution instructions when Claude Code intervention is needed.

### Quality Standards
#### Required:
- Clear HSEARL relevance analysis for all outputs
- Concrete, implementable proposals
- Technical accuracy and innovation
- Proper file management

#### Recommended:
- Quantitative effect predictions
- Staged implementation plans
- Differentiation from existing research
- Practical application possibilities

## Development Guidelines

### Code Quality Requirements
- Type hints required for all Python code
- Follow existing patterns exactly
- Use Google style for docstrings
- Conventional Commits style for git messages

### Testing
- Use `uv run --frozen pytest` for all testing
- New features require tests
- Bug fixes require regression tests
- Test edge cases and error conditions

### Important Notes
- **ONLY use uv for package management, NEVER pip**
- This system is completely prompt-based - no Python automation scripts
- All processing is done by Claude Code following prompt instructions
- VS Code devcontainer support available for development environment