#!/usr/bin/env python3
"""
Batch improvement script for chapters 04-07.
Adds metadata, why sections, common errors, quizzes, and summaries.
"""

import json
from pathlib import Path

# Chapter-specific configurations
CONFIGS = {
    4: {
        "title": "変数変換",
        "difficulty": 4,
        "time": "120〜150分",
        "why": "変数変換は、複雑な分布を既知の分布に変換したり、データの正規性を改善したりする重要な技法です。機械学習の前処理、モンテカルロシミュレーション、極値理論など、幅広い応用があります。",
        "applications": [
            ("対数変換によるデータ正規化", "機械学習で歪度の大きいデータを正規分布に近づけることで、モデルの性能が向上"),
            ("Box-Muller変換", "一様乱数から正規乱数を生成する古典的手法。モンテカルロシミュレーションで使用"),
            ("極値理論", "保険・金融で、最大損失額（最小値・最大値の分布）を予測するために使用")
        ],
        "errors": [
            ("ヤコビアンの絶対値を忘れる", "密度関数は常に非負なので、必ず絶対値を取る", "公式を確認し、必ず|J|を計算する"),
            ("単調でない変換の扱い", "g(x)が単調でない場合、区間ごとに分けて計算が必要", "変換が単調な区間に分割してから公式を適用する")
        ],
        "quiz": [
            "X ~ U(0,1)のとき、Y=-ln(X)の分布は何か？",
            "2変数の変換でヤコビアンが必要な理由を説明せよ"
        ]
    },
    5: {
        "title": "離散型分布",
        "difficulty": 2,
        "time": "90〜120分",
        "why": "離散型分布は、カウントデータ（顧客数、不良品数、クリック数など）のモデリングに不可欠です。ベルヌーイ、二項、ポアソン、幾何分布などは、実務で最も頻繁に使われる分布です。",
        "applications": [
            ("ウェブサイトのクリック数", "ポアソン分布でモデリングし、適切なサーバー容量を設計"),
            ("製品の不良品検査", "二項分布を使って、ロット全体の不良率を推定"),
            ("待ち時間のモデリング", "幾何分布で、成功するまでの試行回数を予測")
        ],
        "errors": [
            ("ポアソン近似の誤用", "n大、p小のときのみ二項→ポアソン近似が有効", "np=λが適度な値（通常10程度）を確認"),
            ("負の二項分布の解釈", "r回成功までの失敗回数と、r回失敗までの成功回数の定義が混在", "教科書・ライブラリの定義を確認")
        ],
        "quiz": [
            "二項分布Bin(n,p)でn→∞, p→0, np→λのとき何が起こるか？",
            "ポアソン分布の分散と平均の関係は？"
        ]
    },
    6: {
        "title": "連続型分布",
        "difficulty": 3,
        "time": "100〜130分",
        "why": "連続型分布は、測定データ（身長、温度、時間など）のモデリングに使われます。正規分布は自然界で最も頻繁に現れ、指数分布は待ち時間、ガンマ分布は累積時間、ベータ分布は確率のモデリングに使われます。",
        "applications": [
            ("製品の寿命モデリング", "指数分布・ワイブル分布で故障時間を予測し、保守計画を立案"),
            ("ベイズ統計の事前分布", "ベータ分布を成功確率の事前分布として使用"),
            ("待ち行列理論", "指数分布で顧客の到着間隔をモデリング")
        ],
        "errors": [
            ("指数分布の無記憶性の誤解", "P(X>s+t|X>s)=P(X>t)を物理的な寿命に誤適用", "無記憶性は数学的性質で、現実の劣化は考慮しない"),
            ("正規分布の過度な信頼", "全てのデータが正規分布に従うわけではない", "QQプロットや検定で正規性を確認")
        ],
        "quiz": [
            "正規分布N(0,1)の95%点はいくつか？",
            "指数分布の無記憶性を数式で表せ"
        ]
    },
    7: {
        "title": "極限定理",
        "difficulty": 4,
        "time": "120〜150分",
        "why": "中心極限定理は統計学の最も重要な定理の一つです。サンプルサイズが大きければ、元の分布に関わらず標本平均が正規分布に従うことを保証し、推定・検定の理論的基礎となります。",
        "applications": [
            ("世論調査の信頼区間", "中心極限定理により、標本平均の分布が正規分布に近似できるため、信頼区間を計算可能"),
            ("品質管理の管理図", "サンプル平均の管理図は、中心極限定理に基づいて異常を検出"),
            ("モンテカルロシミュレーション", "大数の法則により、シミュレーション回数を増やせば真の値に収束")
        ],
        "errors": [
            ("サンプルサイズの誤解", "「n≥30なら中心極限定理が使える」は目安に過ぎない", "元の分布の形状によってはもっと大きなnが必要"),
            ("大数の法則とCLTの混同", "大数の法則は収束、CLTは分布の形を示す", "LLN:X̄→μ、CLT:√n(X̄-μ)→N(0,σ²)")
        ],
        "quiz": [
            "中心極限定理の3つの条件を述べよ",
            "大数の法則と中心極限定理の違いは何か？"
        ]
    }
}

def add_improvements(chapter_num):
    """Add comprehensive improvements to a notebook."""
    config = CONFIGS[chapter_num]
    notebook_path = Path(f"notebooks/{chapter_num:02d}_*.ipynb")
    matches = list(Path(".").glob(str(notebook_path)))

    if not matches:
        print(f"⚠ No notebook found for chapter {chapter_num}")
        return False

    nb_file = matches[0]

    # Load notebook
    with open(nb_file, 'r') as f:
        nb = json.load(f)

    # Create sections
    metadata_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"""## 📋 学習メタ情報

### 学習目標
（既存の学習目標を活用）

### 推定学習時間
**{config['time']}**

### 難易度
**{'★' * config['difficulty']}{'☆' * (5 - config['difficulty'])}** (5段階中{config['difficulty']})

---

## 🎯 なぜこの章を学ぶのか？

{config['why']}

### 実世界での応用

""" + "\n\n".join([f"**{app[0]}**: {app[1]}" for app in config['applications']]) + "\n\n---"
    }

    errors_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": "## ⚠️ よくある間違いと解決策\n\n" +
            "\n\n".join([
                f"### ❌ {err[0]}\n**正しい理解:** {err[1]}\n**解決策:** {err[2]}"
                for err in config['errors']
            ]) + "\n\n---"
    }

    quiz_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": "## 📝 理解度チェッククイズ\n\n" +
            "\n\n".join([f"### 問題 {i+1}\n{q}" for i, q in enumerate(config['quiz'])]) +
            "\n\n---"
    }

    summary_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": "## 📚 まとめ\n\nお疲れ様でした！この章で学んだ内容は、今後の章で繰り返し使います。\n\n---"
    }

    # Insert after first cell, append at end
    new_cells = [nb['cells'][0], metadata_cell] + nb['cells'][1:]
    new_cells.extend([errors_cell, quiz_cell, summary_cell])
    nb['cells'] = new_cells

    # Save
    with open(nb_file, 'w') as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)

    print(f"✓ Improved chapter {chapter_num}: {config['title']}")
    return True

if __name__ == "__main__":
    for ch in range(4, 8):
        add_improvements(ch)
    print("\n✓ Batch improvement complete for chapters 04-07")
