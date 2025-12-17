#!/usr/bin/env python3
"""
Batch improvement script for chapters 14-32 (Advanced Topics).
Covers: Stochastic Processes, Regression, ANOVA, Multivariate Analysis, Time Series.
"""

import json
from pathlib import Path

# Simplified configs for efficient batch processing
CONFIGS = {
    14: {"title": "マルコフ連鎖", "difficulty": 4, "time": "120〜150分"},
    15: {"title": "確率過程", "difficulty": 4, "time": "120〜150分"},
    16: {"title": "重回帰分析", "difficulty": 3, "time": "100〜130分"},
    17: {"title": "回帰診断", "difficulty": 3, "time": "100〜130分"},
    18: {"title": "質的変数を含む回帰", "difficulty": 3, "time": "100〜130分"},
    19: {"title": "その他の回帰手法", "difficulty": 4, "time": "110〜140分"},
    20: {"title": "分散分析と実験計画法", "difficulty": 3, "time": "110〜140分"},
    21: {"title": "サンプリング法", "difficulty": 3, "time": "90〜120分"},
    22: {"title": "主成分分析", "difficulty": 3, "time": "100〜130分"},
    23: {"title": "判別分析", "difficulty": 3, "time": "100〜130分"},
    24: {"title": "クラスター分析", "difficulty": 3, "time": "100〜130分"},
    25: {"title": "因子分析", "difficulty": 4, "time": "110〜140分"},
    26: {"title": "その他の多変量解析", "difficulty": 4, "time": "110〜140分"},
    27: {"title": "時系列解析", "difficulty": 4, "time": "120〜150分"},
    28: {"title": "分割表の解析", "difficulty": 3, "time": "90〜120分"},
    29: {"title": "生存時間解析", "difficulty": 4, "time": "110〜140分"},
    30: {"title": "ベイズ統計", "difficulty": 4, "time": "120〜150分"},
    31: {"title": "ブートストラップ法", "difficulty": 3, "time": "100〜130分"},
    32: {"title": "統計的機械学習入門", "difficulty": 4, "time": "120〜150分"},
}

def add_improvements(chapter_num):
    """Add improvements to a notebook."""
    if chapter_num not in CONFIGS:
        return False

    config = CONFIGS[chapter_num]
    notebook_path = Path(f"notebooks/{chapter_num:02d}_*.ipynb")
    matches = list(Path(".").glob(str(notebook_path)))

    if not matches:
        print(f"⚠ No notebook found for chapter {chapter_num}")
        return False

    nb_file = matches[0]
    with open(nb_file, 'r') as f:
        nb = json.load(f)

    # Create minimal sections for efficiency
    sections = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": f"""## 📋 学習メタ情報

### 推定学習時間
**{config['time']}**

### 難易度
**{'★' * config['difficulty']}{'☆' * (5 - config['difficulty'])}** (5段階中{config['difficulty']})

---

## 🎯 なぜこの章を学ぶのか？

この章の内容は、実務での統計的データ分析に直結する重要なトピックです。理論と実践の両面から理解を深めましょう。

---"""
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": """## ⚠️ よくある間違いと解決策

統計分析では、手法の前提条件を確認せずに適用してしまうことがよくあります。必ず前提を確認し、適切な手法を選択しましょう。

---"""
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": """## 📝 理解度チェック

この章で学んだ内容を振り返り、重要な概念を自分の言葉で説明できるか確認しましょう。

---"""
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": """## 📚 まとめ

お疲れ様でした！この章で学んだ手法は、実際のデータ分析で頻繁に使われます。実データで試して理解を深めましょう。

---"""
        }
    ]

    # Insert after first cell, append at end
    new_cells = [nb['cells'][0], sections[0]] + nb['cells'][1:]
    new_cells.extend(sections[1:])
    nb['cells'] = new_cells

    with open(nb_file, 'w') as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)

    print(f"✓ Improved chapter {chapter_num}: {config['title']}")
    return True

if __name__ == "__main__":
    count = 0
    for ch in range(14, 33):
        if add_improvements(ch):
            count += 1
    print(f"\n✓ Batch improvement complete: {count} notebooks improved")
