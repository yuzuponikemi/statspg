#!/usr/bin/env python3
"""
Script to improve Jupyter notebooks with comprehensive Japanese educational content.
Adds metadata, detailed explanations, comments, quizzes, and real-world examples.
"""

import json
import sys
import re
from pathlib import Path

def create_metadata_cell(chapter_num, title, objectives, prerequisites, time_estimate, difficulty, category):
    """Create a comprehensive metadata cell in Japanese."""

    objectives_md = "\n".join([f"- ☑ {obj}" for obj in objectives])
    prerequisites_md = "\n".join([f"- {prereq}" for prereq in prerequisites])

    metadata = f"""# 第{chapter_num}章: {title}

## 📋 学習メタ情報

### 学習目標
{objectives_md}

### 前提知識
{prerequisites_md}

### 推定学習時間
**{time_estimate}**（コード実行と練習問題を含む）

### 難易度
**{'★' * difficulty}{'☆' * (5 - difficulty)}** (5段階中{difficulty})

### カテゴリー
**{category}**

---"""

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": metadata
    }

def create_why_section(chapter_num, title, why_important, real_world_examples):
    """Create 'Why' section explaining importance."""

    examples_md = "\n\n".join([f"**例{i+1}: {ex['title']}**\n{ex['description']}"
                               for i, ex in enumerate(real_world_examples)])

    why_section = f"""## 🎯 なぜこの章を学ぶのか？

### この章の重要性
{why_important}

### 実世界での応用
{examples_md}

---"""

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": why_section
    }

def create_common_errors_section(errors):
    """Create common errors and solutions section."""

    errors_md = "\n\n".join([
        f"### ❌ よくある間違い {i+1}: {err['title']}\n\n"
        f"**間違った考え方:**\n{err['wrong']}\n\n"
        f"**正しい理解:**\n{err['correct']}\n\n"
        f"**解決策:**\n{err['solution']}"
        for i, err in enumerate(errors)
    ])

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"""## ⚠️ よくある間違いと解決策

{errors_md}

---"""
    }

def create_quiz_section(questions):
    """Create self-assessment quiz section."""

    quiz_md = ""
    for i, q in enumerate(questions, 1):
        quiz_md += f"""### 問題 {i}
{q['question']}

<details>
<summary>解答を見る</summary>

**解答:** {q['answer']}

**解説:**
{q['explanation']}

</details>

"""

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"""## 📝 理解度チェッククイズ

以下の問題に答えて、この章の理解度を確認しましょう。

{quiz_md}

---"""
    }

def create_summary_section(key_points, formulas, next_steps):
    """Create comprehensive summary section."""

    points_md = "\n".join([f"{i+1}. {point}" for i, point in enumerate(key_points)])

    formulas_md = "\n".join([f"- **{f['name']}**: ${f['formula']}$" for f in formulas])

    next_md = "\n".join([f"- {step}" for step in next_steps])

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"""## 📚 まとめ

### 重要ポイント
{points_md}

### 重要な公式
{formulas_md}

### 次のステップ
{next_md}

### 学習を深めるために
- この章の内容を自分の言葉で説明できるか確認しましょう
- 練習問題を再度解いて、理解を定着させましょう
- 実際のデータに適用して、理論と実践を結びつけましょう

お疲れ様でした！次の章に進む準備ができています。

---"""
    }

def add_detailed_comments_to_code(code_cell):
    """Add detailed Japanese comments to code cells."""
    # This is a simplified version - in practice, you'd parse and enhance each code block
    return code_cell

def improve_notebook(notebook_path, metadata_config):
    """Improve a notebook with comprehensive educational content."""

    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    cells = notebook['cells']
    new_cells = []

    # 1. Add metadata cell at the beginning
    new_cells.append(create_metadata_cell(
        metadata_config['chapter_num'],
        metadata_config['title'],
        metadata_config['objectives'],
        metadata_config['prerequisites'],
        metadata_config['time_estimate'],
        metadata_config['difficulty'],
        metadata_config['category']
    ))

    # 2. Add Why section
    new_cells.append(create_why_section(
        metadata_config['chapter_num'],
        metadata_config['title'],
        metadata_config['why_important'],
        metadata_config['real_world_examples']
    ))

    # 3. Add original cells (skip first cell which is typically the title)
    for cell in cells[1:]:
        new_cells.append(cell)

    # 4. Add common errors section before practice problems
    # Find where practice problems start
    practice_idx = len(new_cells)
    for i, cell in enumerate(new_cells):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            if '練習問題' in source or '問題' in source:
                practice_idx = i
                break

    new_cells.insert(practice_idx, create_common_errors_section(metadata_config['common_errors']))

    # 5. Add quiz section after practice problems
    new_cells.append(create_quiz_section(metadata_config['quiz']))

    # 6. Add summary section at the end
    new_cells.append(create_summary_section(
        metadata_config['summary']['key_points'],
        metadata_config['summary']['formulas'],
        metadata_config['summary']['next_steps']
    ))

    notebook['cells'] = new_cells

    return notebook

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python improve_notebook.py <notebook_path>")
        sys.exit(1)

    notebook_path = sys.argv[1]
    # Metadata config would be loaded from a YAML/JSON file or defined per chapter
    # This is a template
    print(f"Improving notebook: {notebook_path}")
