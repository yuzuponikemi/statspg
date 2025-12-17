#!/usr/bin/env python3
"""
Batch improvement script for chapters 08-13 (Statistical Inference).
"""

import json
from pathlib import Path

CONFIGS = {
    8: {
        "title": "統計的推定の基礎",
        "difficulty": 3,
        "time": "100〜130分",
        "why": "統計的推定は、標本データから母集団のパラメータを推測する手法です。点推定・区間推定の理論は、全ての統計分析の基礎となります。",
        "applications": [
            ("世論調査", "標本調査から母比率を推定し、信頼区間を計算"),
            ("品質管理", "製品のサンプルから全体の不良率を推定"),
            ("臨床試験", "治療効果の平均値を推定し、有効性を評価")
        ],
        "errors": [
            ("点推定と区間推定の混同", "点推定は1つの値、区間推定は範囲", "信頼区間は「母数が含まれる確率95%の区間」"),
            ("不偏性と一致性の混同", "不偏性はE[θ̂]=θ、一致性はn→∞でθ̂→θ", "不偏でも一致しない推定量も存在")
        ],
        "quiz": [
            "最尤推定量の定義を述べよ",
            "不偏推定量とは何か？なぜ重要か？"
        ]
    },
    9: {
        "title": "区間推定",
        "difficulty": 3,
        "time": "90〜120分",
        "why": "区間推定は、推定の不確実性を定量化する手法です。信頼区間により、推定値の信頼性を評価し、意思決定の根拠とします。",
        "applications": [
            ("A/Bテスト", "コンバージョン率の差の信頼区間を計算し、有意性を判断"),
            ("医薬品の効果", "治療効果の95%信頼区間を計算し、承認判断の根拠とする"),
            ("経済指標", "GDPや失業率の信頼区間を公表し、政策判断の材料とする")
        ],
        "errors": [
            ("信頼区間の誤解釈", "「母数が95%の確率で区間内」は誤り", "「同じ方法で100回推定したら95回は母数を含む区間が得られる」"),
            ("サンプルサイズと区間幅", "nが大きいほど信頼区間は狭くなる", "区間幅∝1/√n")
        ],
        "quiz": [
            "95%信頼区間の正しい解釈を述べよ",
            "信頼区間を狭くする方法は？"
        ]
    },
    10: {
        "title": "仮説検定の基礎",
        "difficulty": 3,
        "time": "100〜130分",
        "why": "仮説検定は、データから仮説の妥当性を統計的に判断する手法です。第1種・第2種の誤りを制御しながら、科学的な意思決定を行います。",
        "applications": [
            ("新薬の承認", "プラセボと比較して有意差があるか検定"),
            ("製造工程の異常検知", "平均値が基準値から逸脱していないか検定"),
            ("マーケティング施策", "施策前後で売上に有意差があるか検定")
        ],
        "errors": [
            ("p値の誤解釈", "「p=0.03だから仮説が正しい確率97%」は誤り", "p値は「帰無仮説が正しいとしたとき、これほど極端なデータが得られる確率」"),
            ("有意差と実質差", "統計的に有意でも実務的に無意味な差もある", "効果量（Cohen's dなど）も確認する")
        ],
        "quiz": [
            "第1種の誤りと第2種の誤りを説明せよ",
            "p値の正しい解釈を述べよ"
        ]
    },
    11: {
        "title": "正規分布に関する検定",
        "difficulty": 3,
        "time": "90〜120分",
        "why": "t検定、F検定、カイ二乗検定は、正規分布を前提とした最も基本的な検定手法です。2群比較や分散の検定など、実務で頻繁に使われます。",
        "applications": [
            ("A/Bテストの平均比較", "t検定で2群の平均値の差を検定"),
            ("分散の均一性検定", "F検定で2群の分散が等しいか検定（t検定の前提確認）"),
            ("適合度検定", "カイ二乗検定でデータが理論分布に従うか検定")
        ],
        "errors": [
            ("t検定の前提無視", "正規性・等分散性の前提を確認せず使用", "Shapiro-Wilk検定やLevene検定で前提を確認"),
            ("対応あり・なしの混同", "対応のあるデータに通常のt検定を使う", "paired t-testを使う")
        ],
        "quiz": [
            "t検定の前提条件は？",
            "対応のある t検定と対応のない t検定の違いは？"
        ]
    },
    12: {
        "title": "一般的な分布に関する検定",
        "difficulty": 4,
        "time": "110〜140分",
        "why": "正規性の前提が満たされない場合、尤度比検定やワルド検定などの一般的な手法が必要です。これらは最尤推定に基づく統一的な枠組みを提供します。",
        "applications": [
            ("ロジスティック回帰", "尤度比検定で変数の有意性を検定"),
            ("ポアソン回帰", "カウントデータのモデリングで係数を検定"),
            ("一般化線形モデル", "様々な分布族に対応した検定")
        ],
        "errors": [
            ("サンプルサイズと漸近理論", "nが小さいと漸近理論が成立しない", "n≥30程度が目安だが、分布によって異なる"),
            ("多重検定の問題", "複数の検定を行うと第1種の誤りが増大", "Bonferroni補正などで調整")
        ],
        "quiz": [
            "尤度比検定の統計量は何に従うか？",
            "Wald検定とスコア検定の違いは？"
        ]
    },
    13: {
        "title": "ノンパラメトリック法",
        "difficulty": 3,
        "time": "100〜130分",
        "why": "ノンパラメトリック検定は、分布の形を仮定せずに使える頑健な手法です。正規性の前提が疑わしい場合や、順序データの分析に有用です。",
        "applications": [
            ("満足度調査", "順序尺度のデータに対してMann-Whitney U検定を使用"),
            ("中央値の比較", "外れ値に頑健な中央値の検定"),
            ("適合度検定", "Kolmogorov-Smirnov検定でデータの分布を確認")
        ],
        "errors": [
            ("検出力の低さ", "ノンパラメトリック検定は検出力がやや低い", "可能なら正規性を確認してパラメトリック検定を使う"),
            ("順序情報の損失", "連続データを順位に変換すると情報が失われる", "必要に応じてWilcoxon検定などを選択")
        ],
        "quiz": [
            "Mann-Whitney U検定はどんな時に使うか？",
            "Wilcoxon符号付順位検定と符号検定の違いは？"
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
    with open(nb_file, 'r') as f:
        nb = json.load(f)

    # Create sections
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

{config['why']}

### 実世界での応用

""" + "\n\n".join([f"**{app[0]}**: {app[1]}" for app in config['applications']]) + "\n\n---"
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": "## ⚠️ よくある間違いと解決策\n\n" +
                "\n\n".join([
                    f"### ❌ {err[0]}\n**正しい理解:** {err[1]}\n**解決策:** {err[2]}"
                    for err in config['errors']
                ]) + "\n\n---"
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": "## 📝 理解度チェッククイズ\n\n" +
                "\n\n".join([f"### 問題 {i+1}\n{q}" for i, q in enumerate(config['quiz'])]) +
                "\n\n---"
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": "## 📚 まとめ\n\nお疲れ様でした！この章の内容は統計的推論の核心部分です。\n\n---"
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
    for ch in range(8, 14):
        add_improvements(ch)
    print("\n✓ Batch improvement complete for chapters 08-13")
