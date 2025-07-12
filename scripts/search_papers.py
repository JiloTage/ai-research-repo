#!/usr/bin/env python3
"""ArXiv論文検索スクリプト - HSEARL関連論文の自動検索."""

import feedparser
import re
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set


def get_hsearl_search_keywords() -> Dict[str, List[str]]:
    """HSEARL 6つの観点に基づく検索キーワードを取得.
    
    Returns:
        Dict[str, List[str]]: 各観点とそのキーワードリスト
    """
    return {
        "認知型": [
            "cognitive models", "personality types", "MBTI", "cognitive functions",
            "information processing", "thinking styles", "decision making",
            "cognitive assessment", "psychological types"
        ],
        "動機型": [
            "personality motivation", "enneagram", "motivation theory",
            "behavioral drives", "personality dynamics", "core motivations",
            "fear and desire", "personality assessment"
        ],
        "反応型": [
            "emotional response", "tritype", "emotional intelligence",
            "stress response", "coping mechanisms", "emotional regulation",
            "behavioral patterns", "response styles"
        ],
        "適応状態": [
            "psychological health", "adaptation", "mental health levels",
            "stress tolerance", "resilience", "psychological well-being",
            "adaptive behavior", "coping strategies"
        ],
        "育ち": [
            "developmental psychology", "childhood development", "family dynamics",
            "early experiences", "attachment theory", "parenting styles",
            "developmental trauma", "family systems"
        ],
        "ロール": [
            "social roles", "role theory", "social identity", "role adaptation",
            "social masks", "persona", "social performance", "role flexibility"
        ]
    }


def search_arxiv_papers(keywords: List[str], days_back: int = 7) -> List[Dict]:
    """ArXivで論文を検索.
    
    Args:
        keywords: 検索キーワードのリスト
        days_back: 何日前からの論文を検索するか
        
    Returns:
        List[Dict]: 見つかった論文の情報リスト
    """
    papers = []
    
    # 日付フィルター (YYYY-MM-DD形式)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    for keyword in keywords:
        # ArXiv APIクエリを構築
        query = f'all:"{keyword}" AND (cat:cs.AI OR cat:cs.CL OR cat:cs.LG OR cat:stat.ML)'
        encoded_query = urllib.parse.quote(query)
        
        # ArXiv API URL
        url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending"
        
        try:
            # フィードを取得
            feed = feedparser.parse(url)
            
            for entry in feed.entries:
                # 論文情報を抽出
                paper_info = {
                    "id": entry.id.split("/")[-1],
                    "title": entry.title.replace("\n", " ").strip(),
                    "authors": [author.name for author in getattr(entry, "authors", [])],
                    "summary": entry.summary.replace("\n", " ").strip(),
                    "published": entry.published,
                    "arxiv_url": entry.id,
                    "pdf_url": entry.id.replace("abs", "pdf"),
                    "search_keyword": keyword,
                    "categories": [tag.term for tag in getattr(entry, "tags", [])]
                }
                papers.append(paper_info)
                
        except Exception as e:
            print(f"警告: キーワード '{keyword}' の検索でエラー: {e}")
            continue
    
    return papers


def filter_relevant_papers(papers: List[Dict], existing_ids: Set[str]) -> List[Dict]:
    """関連性の高い論文をフィルタリング.
    
    Args:
        papers: 検索された論文のリスト
        existing_ids: 既に処理済みの論文IDのセット
        
    Returns:
        List[Dict]: フィルタリングされた論文のリスト
    """
    # 重複除去
    seen_ids = set()
    unique_papers = []
    
    for paper in papers:
        paper_id = paper["id"]
        if paper_id not in seen_ids and paper_id not in existing_ids:
            seen_ids.add(paper_id)
            unique_papers.append(paper)
    
    # HSEARL関連性でフィルタリング
    hsearl_keywords = [
        "personality", "cognitive", "emotional", "motivation", "development",
        "adaptation", "social", "psychological", "behavior", "individual differences",
        "mental health", "assessment", "modeling", "human factors"
    ]
    
    relevant_papers = []
    for paper in unique_papers:
        # タイトルと要約を小文字で結合
        text = (paper["title"] + " " + paper["summary"]).lower()
        
        # 関連キーワードが含まれているかチェック
        if any(keyword in text for keyword in hsearl_keywords):
            relevant_papers.append(paper)
    
    return relevant_papers


def load_existing_paper_ids(todo_file: Path) -> Set[str]:
    """既存のサーベイ予定論文リストからIDを読み込み.
    
    Args:
        todo_file: サーベイ予定論文リストファイルのパス
        
    Returns:
        Set[str]: 既存の論文IDのセット
    """
    existing_ids = set()
    
    if todo_file.exists():
        content = todo_file.read_text(encoding="utf-8")
        # ArXiv IDパターンを検索 (例: 2301.12345)
        pattern = r"arxiv\.org/abs/(\d{4}\.\d{4,5})"
        matches = re.findall(pattern, content)
        existing_ids.update(matches)
    
    return existing_ids


def update_survey_todo_list(papers: List[Dict], todo_file: Path) -> None:
    """サーベイ予定論文リストを更新.
    
    Args:
        papers: 新しい論文のリスト
        todo_file: サーベイ予定論文リストファイルのパス
    """
    if not papers:
        print("新しい論文は見つかりませんでした。")
        return
    
    # 既存のコンテンツを読み込み
    if todo_file.exists():
        content = todo_file.read_text(encoding="utf-8")
    else:
        content = """# サーベイ予定論文リスト

このファイルは、HSEARL研究に関連する論文のサーベイ待ちリストです。
Claude Codeによって論文サマリーが生成されると、該当項目がチェックされます。

## 処理待ち論文

"""
    
    # 新しい論文を追加
    new_entries = []
    for paper in papers:
        entry = f"""
### {paper['title']}
- **ArXiv ID**: {paper['id']}
- **URL**: {paper['arxiv_url']}
- **著者**: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}
- **公開日**: {paper['published'][:10]}
- **検索キーワード**: {paper['search_keyword']}
- **カテゴリ**: {', '.join(paper['categories'][:3])}
- **要約**: {paper['summary'][:200]}...

**サマリー生成**: [ ] 未処理

---
"""
        new_entries.append(entry)
    
    # "処理待ち論文"セクションの後に新しいエントリを挿入
    if "## 処理待ち論文" in content:
        parts = content.split("## 処理待ち論文")
        if len(parts) >= 2:
            # 既存の処理待ち論文セクションの後に新しい論文を追加
            updated_content = parts[0] + "## 処理待ち論文\n" + "".join(new_entries) + parts[1]
        else:
            updated_content = content + "".join(new_entries)
    else:
        updated_content = content + "\n## 処理待ち論文\n" + "".join(new_entries)
    
    # ファイルに書き込み
    todo_file.write_text(updated_content, encoding="utf-8")
    print(f"✅ {len(papers)}件の新しい論文をサーベイ予定リストに追加しました。")


def main() -> None:
    """メイン処理."""
    print("🔍 HSEARL関連論文検索を開始...")
    
    # パスの設定
    project_root = Path(__file__).parent.parent
    todo_file = project_root / "docs" / "サーベイ予定論文リスト.md"
    
    # 既存の論文IDを読み込み
    existing_ids = load_existing_paper_ids(todo_file)
    print(f"📋 既存の論文数: {len(existing_ids)}件")
    
    # HSEARL観点での検索
    keywords_by_aspect = get_hsearl_search_keywords()
    all_papers = []
    
    for aspect, keywords in keywords_by_aspect.items():
        print(f"🔍 {aspect}関連論文を検索中...")
        papers = search_arxiv_papers(keywords, days_back=14)  # 2週間分
        print(f"   {len(papers)}件の論文を発見")
        all_papers.extend(papers)
    
    # 関連性フィルタリング
    print(f"📊 合計 {len(all_papers)}件の論文を発見")
    relevant_papers = filter_relevant_papers(all_papers, existing_ids)
    print(f"✨ そのうち {len(relevant_papers)}件が新規で関連性が高い論文です")
    
    # サーベイ予定リストを更新
    if relevant_papers:
        update_survey_todo_list(relevant_papers, todo_file)
        
        # Claude Codeタスク生成のためのメッセージ
        print("\n🤖 Claude Codeさん、以下を実行してください:")
        print("1. docs/prompts/paper_summary_prompt.mdの手順に従って論文サマリーを生成")
        print("2. HSEARLとの関連性を分析")
        print("3. docs/surveys/に保存")
        print(f"4. 対象論文数: {len(relevant_papers)}件")
    else:
        print("新しい関連論文は見つかりませんでした。")


if __name__ == "__main__":
    main()