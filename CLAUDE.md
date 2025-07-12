# Development Guidelines

This document contains critical information about working with this codebase.
Follow these guidelines precisely.

## Rules

1. Package Management
   - ONLY use uv, NEVER pip
   - Installation: `uv add package`
   - Upgrading: `uv add --dev package --upgrade-package package`
   - FORBIDDEN: `uv pip install`, `@latest` syntax

2. Code Quality
   - Type hints required for all code
   - Follow existing patterns exactly
   - Use Google style for docstring

3. Testing Requirements
   - Framework: `uv run --frozen pytest`
   - Coverage: test edge cases and errors
   - New features require tests
   - Bug fixes require regression tests

4. Git
   - Follow the Conventional Commits style on commit messages.

## Code Formatting and Linting

1. Ruff
   - Format: `uv run --frozen ruff format .`
   - Check: `uv run --frozen ruff check .`
   - Fix: `uv run --frozen ruff check . --fix`
2. Pre-commit
   - Config: `.pre-commit-config.yaml`
   - Runs: on git commit
   - Tools: Ruff (Python)

## HSEARL研究論文調査システム

### 概要

このプロジェクトは、HSEARL（人間の構造的理解と翻訳のための6つの指標モデル）に関連するAI/LLM論文を自動的に調査・整理するシステムです。GitHub Actionsにより20分ごとに以下のタスクを自動実行します：

1. ArXivから関連論文を検索（Python自動化）
2. 論文サマリーを落合フォーマットで生成（Claude Code実行）
3. HSEARLとの関連性を分析（Claude Code実行）
4. 新しいアイデアを創出（Claude Code実行）

### ディレクトリ構造

```
├── docs/
│   ├── base/
│   │   └── HSEARL（ハール）.md    # HSEARLの定義
│   ├── surveys/                    # 論文サマリー保存先
│   ├── idea/                       # アイデア保存先
│   ├── prompts/                    # Claude Code用手順書
│   │   ├── paper_summary_prompt.md    # サマリー生成手順
│   │   └── idea_generation_prompt.md  # アイデア生成手順
│   └── サーベイ予定論文リスト.md    # 処理待ち論文リスト
├── scripts/
│   ├── search_papers.py            # ArXiv論文検索
│   └── main_pipeline.py            # メインパイプライン
└── .github/workflows/
    └── hsearl-research.yml         # GitHub Actions設定
```

### 手動実行方法

1. 依存関係のインストール：
   ```bash
   uv add feedparser
   ```

2. パイプライン全体の実行：
   ```bash
   uv run python scripts/main_pipeline.py
   ```

3. 個別スクリプトの実行：
   ```bash
   # 論文検索のみ
   uv run python scripts/search_papers.py
   ```

### Claude Code実行手順

#### 論文サマリー生成手順

**実行条件**: `docs/サーベイ予定論文リスト.md`に処理待ちの論文がある

**手順**:
1. `docs/prompts/paper_summary_prompt.md`を読み込む
2. 手順書に従って論文サマリーを生成
3. 落合フォーマット + HSEARLとの関連性分析
4. `docs/surveys/[ArXiv ID]_[タイトル].md`として保存
5. 処理した論文を`docs/サーベイ予定論文リスト.md`から削除

**重要事項**:
- WebFetchツールでArXivページから詳細取得
- HSEARLの6つの観点すべてから関連性を分析
- 具体的で実装可能な応用可能性を記述

#### アイデア生成手順

**実行条件**: `docs/surveys/`に未処理のサマリーファイルがある

**手順**:
1. `docs/prompts/idea_generation_prompt.md`を読み込む
2. `docs/base/HSEARL（ハール）.md`でHSEARLの理解を深める
3. 未処理のサマリーから革新的アイデアを生成
4. HSEARLの各観点（認知型、動機型、反応型、適応状態、育ち、ロール）から最低1つずつ
5. `docs/idea/[日時]_[観点]_[タイトル].md`として保存
6. 処理済みファイルを`docs/processed_ideas.json`に記録

**重要事項**:
- 抽象的ではなく具体的で実装可能なアイデア
- 既存技術との明確な差別化
- 技術的実現可能性と段階的実装計画
- 定量的な効果予測

### 自動実行の設定

GitHub Actionsは以下の条件で自動実行されます：

- 20分ごと（cronスケジュール）
- masterブランチへのプッシュ時
- 手動トリガー（Actions タブから）

### 検索キーワード

以下の観点でArXivから論文を検索します：

- 人格・パーソナリティモデリング
- 認知・感情処理
- ロール・コンテキスト適応
- 階層的モデリング
- 個人差・適応

### トラブルシューティング

- 論文が見つからない場合：検索キーワードを`scripts/search_papers.py`で調整
- サマリーが生成されない場合：`docs/サーベイ予定論文リスト.md`を確認
- アイデアが生成されない場合：`docs/surveys/`と`docs/processed_ideas.json`を確認
- GitHub Actionsが失敗する場合：Actionsタブでログを確認
