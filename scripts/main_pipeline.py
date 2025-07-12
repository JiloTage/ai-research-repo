#!/usr/bin/env python3
"""HSEARL研究システムのメインパイプライン."""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from search_papers import main as search_papers_main


def check_pending_surveys(todo_file: Path) -> List[Dict[str, str]]:
    """サーベイ予定論文リストから未処理の論文を取得.
    
    Args:
        todo_file: サーベイ予定論文リストファイルのパス
        
    Returns:
        List[Dict[str, str]]: 未処理論文の情報リスト
    """
    pending_papers = []
    
    if not todo_file.exists():
        return pending_papers
    
    content = todo_file.read_text(encoding="utf-8")
    
    # "サマリー生成": [ ] 未処理 のパターンを検索
    
    # 論文セクションを分割
    sections = re.split(r"### (.+)", content)
    
    for i in range(1, len(sections), 2):  # タイトルとコンテンツのペア
        if i + 1 < len(sections):
            title = sections[i].strip()
            section_content = sections[i + 1]
            
            # 未処理かチェック
            if "サマリー生成**: [ ] 未処理" in section_content:
                # ArXiv IDを抽出
                arxiv_match = re.search(r"ArXiv ID\*\*: ([^\n]+)", section_content)
                url_match = re.search(r"URL\*\*: ([^\n]+)", section_content)
                
                if arxiv_match and url_match:
                    pending_papers.append({
                        "title": title,
                        "arxiv_id": arxiv_match.group(1).strip(),
                        "url": url_match.group(1).strip()
                    })
    
    return pending_papers


def check_unprocessed_summaries(surveys_dir: Path, processed_file: Path) -> List[Path]:
    """未処理のサマリーファイルを取得.
    
    Args:
        surveys_dir: サーベイディレクトリのパス
        processed_file: 処理済みアイデア記録ファイルのパス
        
    Returns:
        List[Path]: 未処理のサマリーファイルのリスト
    """
    unprocessed_summaries = []
    
    if not surveys_dir.exists():
        return unprocessed_summaries
    
    # 処理済みファイルを読み込み
    processed_summaries = set()
    if processed_file.exists():
        try:
            with open(processed_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                processed_summaries = set(data.get("processed_summaries", []))
        except (json.JSONDecodeError, FileNotFoundError):
            processed_summaries = set()
    
    # サーベイディレクトリ内の.mdファイルをチェック
    for summary_file in surveys_dir.glob("*.md"):
        if summary_file.name not in processed_summaries:
            unprocessed_summaries.append(summary_file)
    
    return unprocessed_summaries


def generate_claude_code_instructions() -> str:
    """Claude Code用の実行指示を生成.
    
    Returns:
        str: Claude Code用の指示文
    """
    instructions = []
    
    # プロジェクトパス
    project_root = Path(__file__).parent.parent
    todo_file = project_root / "docs" / "サーベイ予定論文リスト.md"
    surveys_dir = project_root / "docs" / "surveys"
    processed_file = project_root / "docs" / "processed_ideas.json"
    
    # 未処理の論文サマリータスクをチェック
    pending_papers = check_pending_surveys(todo_file)
    if pending_papers:
        instructions.append(f"""
### 📄 論文サマリー生成タスク
未処理の論文が {len(pending_papers)}件 あります。

**実行手順:**
1. `docs/prompts/paper_summary_prompt.md` を読み込んで手順を確認
2. 以下の論文から1件を選択してサマリーを生成:
""")
        for paper in pending_papers[:3]:  # 最大3件まで表示
            instructions.append(f"   - 📖 {paper['title']}")
            instructions.append(f"     ArXiv ID: {paper['arxiv_id']}")
            instructions.append(f"     URL: {paper['url']}")
        
        if len(pending_papers) > 3:
            instructions.append(f"   - ... 他 {len(pending_papers) - 3}件")
        
        instructions.append("""
3. 落合フォーマット + HSEARLとの関連性分析
4. `docs/surveys/[ArXiv ID]_[タイトル].md` として保存
5. サーベイ予定リストの該当項目を「処理済み」に更新
""")
    
    # 未処理のアイデア生成タスクをチェック
    unprocessed_summaries = check_unprocessed_summaries(surveys_dir, processed_file)
    if unprocessed_summaries:
        instructions.append(f"""
### 💡 アイデア生成タスク
未処理のサマリーが {len(unprocessed_summaries)}件 あります。

**実行手順:**
1. `docs/prompts/idea_generation_prompt.md` を読み込んで手順を確認
2. `docs/base/HSEARL（ハール）.md` でHSEARLの理解を深める
3. 以下のサマリーファイルから革新的アイデアを生成:
""")
        for summary_file in unprocessed_summaries[:3]:  # 最大3件まで表示
            instructions.append(f"   - 📄 {summary_file.name}")
        
        if len(unprocessed_summaries) > 3:
            instructions.append(f"   - ... 他 {len(unprocessed_summaries) - 3}件")
        
        instructions.append("""
4. HSEARLの各観点（認知型、動機型、反応型、適応状態、育ち、ロール）から最低1つずつ
5. `docs/idea/[日時]_[観点]_[タイトル].md` として保存
6. 処理済みファイルを `docs/processed_ideas.json` に記録
""")
    
    if not instructions:
        return "現在、Claude Codeでの処理が必要なタスクはありません。"
    
    return "".join(instructions)


def main() -> None:
    """メインパイプライン実行."""
    print("🚀 HSEARL研究パイプライン開始")
    print(f"⏰ 実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Step 1: ArXiv論文検索
        print("\n" + "="*50)
        print("📚 Step 1: ArXiv論文検索")
        print("="*50)
        
        search_papers_main()
        
        # Step 2: Claude Codeタスクの確認と指示生成
        print("\n" + "="*50)
        print("🤖 Step 2: Claude Codeタスク確認")
        print("="*50)
        
        claude_instructions = generate_claude_code_instructions()
        
        if "現在、Claude Codeでの処理が必要なタスクはありません" in claude_instructions:
            print("✅ すべてのタスクが完了しています。")
        else:
            print("🤖 Claude Codeさん、以下を実行してください:")
            print(claude_instructions)
        
        print("\n" + "="*50)
        print("✅ パイプライン完了")
        print("="*50)
        
    except Exception as e:
        print(f"❌ パイプライン実行中にエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()