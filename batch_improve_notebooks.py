#!/usr/bin/env python3
"""
Batch improvement script for statistics notebooks.
Adds metadata, why sections, comments, quizzes, and summaries to all notebooks.
"""

import json
import sys
from pathlib import Path

# Metadata configurations for each chapter
CHAPTER_CONFIGS = {
    3: {
        "title": "分布の特性値",
        "objectives": [
            "期待値・分散の定義と性質を理解する",
            "積率・中心積率を計算できる",
            "歪度・尖度の意味を理解する",
            "共分散・相関係数を使いこなせる"
        ],
        "prerequisites": ["確率分布の基礎（第1-2章）", "微分積分学", "線形代数の基礎"],
        "time": "100〜130分",
        "difficulty": 3,
        "category": "確率論の数理的基礎",
        "why": "分布の特性値は、複雑な確率分布を数値的に要約し比較するための重要なツールです。実務では、データの中心傾向、ばらつき、非対称性、外れ値の傾向を定量的に把握することで、適切な統計手法の選択やリスク管理が可能になります。",
        "real_world": [
            {"title": "金融リスク管理", "desc": "投資ポートフォリオのリターン分布の歪度（正か負か）により、損失リスクの非対称性を評価"},
            {"title": "品質管理", "desc": "製品の寸法分布の尖度が高い場合、規格外品が多発する可能性を示唆"},
            {"title": "機械学習", "desc": "特徴量の分散が大きすぎる場合、モデルの学習が不安定になるため正規化が必要"}
        ],
        "errors": [
            {
                "title": "期待値と最頻値の混同",
                "wrong": "期待値が「最も起こりやすい値」だと考える",
                "correct": "期待値は重み付き平均であり、最頻値（mode）とは異なる",
                "solution": "離散分布で具体的に計算して違いを確認する"
            },
            {
                "title": "相関と因果の混同",
                "wrong": "相関係数が高いから因果関係がある",
                "correct": "相関は関連性を示すが、因果関係は別途検証が必要",
                "solution": "「アイスクリーム売上と溺死者数」のような疑似相関の例を学ぶ"
            }
        ],
        "quiz": [
            {"q": "正規分布の歪度と尖度はいくつか？", "a": "歪度=0, 尖度=3（超過尖度=0）", "exp": "正規分布は左右対称（歪度0）で、基準となる尖度3を持つ"},
            {"q": "共分散が0なら独立か？", "a": "No。無相関だが独立とは限らない", "exp": "Y=X²の場合、Cov(X,Y)=0だが独立ではない"}
        ],
        "summary": {
            "points": ["期待値は加法的、分散は独立なら加法的", "標準化により比較可能に", "歪度・尖度で分布の形状を定量化"],
            "formulas": [
                {"name": "期待値", "formula": "E[X] = \\sum x p(x) \\text{ or } \\int x f(x)dx"},
                {"name": "分散", "formula": "Var(X) = E[(X-\\mu)^2] = E[X^2] - (E[X])^2"},
                {"name": "共分散", "formula": "Cov(X,Y) = E[(X-\\mu_X)(Y-\\mu_Y)]"}
            ],
            "next": ["第4章で変数変換を学ぶ", "第5-6章で具体的な分布の特性値を計算"]
        }
    },
    # Additional chapters would be configured here...
}

def create_metadata_section(config):
    """Create metadata markdown cell."""
    objectives_md = "\n".join([f"- ☑ {obj}" for obj in config["objectives"]])
    prereq_md = "\n".join([f"- {p}" for p in config["prerequisites"]])

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"""## 📋 学習メタ情報

### 学習目標
{objectives_md}

### 前提知識
{prereq_md}

### 推定学習時間
**{config["time"]}**（コード実行と練習問題を含む）

### 難易度
**{'★' * config["difficulty"]}{'☆' * (5 - config["difficulty"])}** (5段階中{config["difficulty"]})

### カテゴリー
**{config["category"]}**

---"""
    }

def create_why_section(config):
    """Create 'why' section."""
    examples = "\n\n".join([
        f"**例{i+1}: {ex['title']}**\n{ex['desc']}"
        for i, ex in enumerate(config["real_world"])
    ])

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"""## 🎯 なぜこの章を学ぶのか？

### この章の重要性

{config["why"]}

### 実世界での応用

{examples}

---"""
    }

def create_errors_section(config):
    """Create common errors section."""
    errors_md = "\n\n".join([
        f"### ❌ よくある間違い {i+1}: {err['title']}\n\n"
        f"**間違った考え方:**\n{err['wrong']}\n\n"
        f"**正しい理解:**\n{err['correct']}\n\n"
        f"**解決策:**\n{err['solution']}"
        for i, err in enumerate(config["errors"])
    ])

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"""## ⚠️ よくある間違いと解決策

{errors_md}

---"""
    }

def create_quiz_section(config):
    """Create quiz section."""
    quiz_md = ""
    for i, q in enumerate(config["quiz"], 1):
        quiz_md += f"""### 問題 {i}
{q['q']}

<details>
<summary>解答を見る</summary>

**解答:** {q['a']}

**解説:**
{q['exp']}

</details>

"""

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"""## 📝 理解度チェッククイズ

{quiz_md}---"""
    }

def create_summary_section(config):
    """Create summary section."""
    points = "\n".join([f"{i+1}. {p}" for i, p in enumerate(config["summary"]["points"])])
    formulas = "\n".join([f"- **{f['name']}**: ${f['formula']}$" for f in config["summary"]["formulas"]])
    next_steps = "\n".join([f"- {s}" for s in config["summary"]["next"]])

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"""## 📚 まとめ

### 重要ポイント
{points}

### 重要な公式
{formulas}

### 次のステップ
{next_steps}

お疲れ様でした！次の章に進む準備ができています。

---"""
    }

def improve_notebook(notebook_path, chapter_num):
    """Improve a notebook by adding educational sections."""
    if chapter_num not in CHAPTER_CONFIGS:
        print(f"⚠ No configuration for chapter {chapter_num}, skipping")
        return False

    config = CHAPTER_CONFIGS[chapter_num]

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']
    new_cells = []

    # Insert metadata and why sections after title
    new_cells.append(cells[0])  # Keep original title
    new_cells.append(create_metadata_section(config))
    new_cells.append(create_why_section(config))

    # Add remaining cells
    new_cells.extend(cells[1:])

    # Add error, quiz, and summary sections at end
    new_cells.append(create_errors_section(config))
    new_cells.append(create_quiz_section(config))
    new_cells.append(create_summary_section(config))

    nb['cells'] = new_cells

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)

    print(f"✓ Improved chapter {chapter_num}: {config['title']}")
    return True

def main():
    notebooks_dir = Path("notebooks")

    # Process chapters 3-32
    improved_count = 0
    for chapter_num in range(3, 33):
        # Find notebook file for this chapter
        pattern = f"{chapter_num:02d}_*.ipynb"
        matches = list(notebooks_dir.glob(pattern))

        if matches:
            if improve_notebook(matches[0], chapter_num):
                improved_count += 1
        else:
            print(f"⚠ No notebook found for chapter {chapter_num}")

    print(f"\n✓ Total notebooks improved: {improved_count}")

if __name__ == "__main__":
    main()
