# ArXiv論文検索手順書

## 目的
HSEARL関連のAI/LLM論文をArXivから検索し、サーベイ予定リストに追加する

## 実行手順

### 1. 既存の検索済み論文の確認
1. `docs/searched_papers.json`を読み込み、既に検索済みの論文IDを確認
2. ファイルが存在しない場合は空のリストとして扱う

### 2. 検索キーワードの設定
以下のHSEARL関連キーワードでArXivを検索：

#### 人格・パーソナリティモデリング関連
- `all:"personality modeling" AND (LLM OR "language model" OR AI)`
- `all:"persona" AND "language model" AND (adaptation OR generation)`
- `all:"psychological traits" AND ("neural network" OR LLM)`

#### 認知・感情処理関連
- `all:"emotion recognition" AND "language model"`
- `all:"cognitive modeling" AND (AI OR LLM)`
- `all:"theory of mind" AND "language model"`

#### ロール・コンテキスト適応関連
- `all:"role playing" AND LLM`
- `all:"context adaptation" AND "language generation"`
- `all:"behavioral modeling" AND AI`

#### 階層的モデリング関連
- `all:"hierarchical modeling" AND personality`
- `all:"multi-layer" AND "psychological model"`

#### 個人差・適応関連
- `all:"individual differences" AND "language model"`
- `all:"adaptive behavior" AND AI`
- `all:"personalization" AND LLM`

### 3. 論文検索の実行
各キーワードについて：

1. **WebSearchツールを使用**してArXivから検索
   - 検索クエリ：`site:arxiv.org [キーワード]`
   - 最新の論文（2024年以降）を優先
   - 各キーワードで最大10件まで

2. **結果の抽出**
   各論文から以下の情報を抽出：
   - ArXiv ID (例: 2301.12345)
   - タイトル
   - 著者名
   - アブストラクト
   - 公開日
   - カテゴリ

3. **重複チェック**
   - 既に`docs/searched_papers.json`に記録済みの論文IDは除外
   - 同一タイトルの論文も除外

### 4. 論文の詳細取得
各新規論文について：

1. **WebFetchツールを使用**してArXivページにアクセス
   - URL: `https://arxiv.org/abs/[ArXiv ID]`
   - 詳細なメタデータを取得

2. **関連性の判定**
   HSEARLとの関連性を以下の観点で評価：
   - 認知型（MBTI）への応用可能性
   - 動機型（エニアグラム）への応用可能性
   - 反応型（トライタイプ）への応用可能性
   - 適応状態（健康度）への応用可能性
   - 育ち（初期情緒配線）への応用可能性
   - ロール（外的演技構造）への応用可能性

3. **関連度スコア付け**
   - 高関連（3点）：直接的にHSEARLの複数要素に応用可能
   - 中関連（2点）：HSEARLの特定要素に応用可能
   - 低関連（1点）：間接的にHSEARLに関連
   - 無関連（0点）：HSEARLとの関連性なし

### 5. サーベイ予定リストの更新

#### 5.1 既存リストの読み込み
`docs/サーベイ予定論文リスト.md`を読み込み、既存の論文URLを抽出

#### 5.2 新規論文の追加
関連度スコア1点以上の論文を以下の形式で追加：

```markdown
## 追加日: [YYYY-MM-DD HH:MM]

### [論文タイトル]
- **著者**: [著者名（最大3名、それ以上は"他"）]
- **カテゴリ**: [ArXivカテゴリ]
- **公開日**: [公開日]
- **関連度**: [★★★/★★/★]
- **関連要素**: [該当するHSEARL要素]
- **リンク**: https://arxiv.org/abs/[ArXiv ID]
- **概要**: [アブストラクトの抜粋（200文字程度）]

**HSEARL関連性**:
[具体的な関連性の説明]

---
```

#### 5.3 ファイルが存在しない場合の初期化
```markdown
# サーベイ予定論文リスト

HSEARLに関連する論文のリストです。各論文は調査後に削除されます。

## 検索ポリシー
- 関連度★★★：最優先で調査
- 関連度★★：次優先で調査  
- 関連度★：時間があれば調査

---
```

### 6. 検索済み論文の記録更新

#### 6.1 `docs/searched_papers.json`の更新
新規検索した論文IDをリストに追加：
```json
[
  "2301.12345",
  "2302.67890",
  ...
]
```

#### 6.2 検索統計の記録
`docs/search_stats.json`に検索統計を記録：
```json
{
  "last_search_date": "2025-01-XX",
  "total_papers_found": 150,
  "high_relevance": 25,
  "medium_relevance": 45,
  "low_relevance": 80,
  "search_keywords_used": [
    "personality modeling AND LLM",
    "emotion recognition AND language model",
    ...
  ]
}
```

### 7. 品質チェック

#### 7.1 必須チェック項目
- [ ] 全ての新規論文がHSEARLとの関連性を持つ
- [ ] 重複論文が含まれていない
- [ ] ArXivリンクが正しい形式
- [ ] 関連度スコアが適切

#### 7.2 推奨チェック項目
- [ ] 各キーワードから均等に論文が選ばれている
- [ ] 最新の論文（2024年以降）が優先されている
- [ ] 多様な著者・研究機関からの論文が含まれている

## 実行結果の報告

検索完了後、以下の形式で結果を報告：

```
=== ArXiv論文検索結果 ===
実行日時: [YYYY-MM-DD HH:MM]
検索キーワード数: [N]個
発見論文総数: [N]件
新規論文数: [N]件

関連度別内訳:
- 高関連（★★★）: [N]件
- 中関連（★★）: [N]件  
- 低関連（★）: [N]件

追加済み論文: [N]件
スキップ済み論文: [N]件（重複・無関連）

次回優先調査論文: [N]件
=== 検索完了 ===
```

## 注意事項
- API制限を避けるため、検索間隔を適切に調整
- 論文の質と新規性を重視
- HSEARLとの関連性を厳密に判定
- 検索キーワードは定期的に見直し・更新