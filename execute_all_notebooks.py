#!/usr/bin/env python3
"""Execute all notebooks and save outputs."""

import subprocess
import sys
from pathlib import Path

def execute_notebook(notebook_path):
    """Execute a single notebook and save outputs."""
    try:
        output_name = f"{notebook_path.stem}_executed{notebook_path.suffix}"
        cmd = [
            "python3", "-m", "nbconvert",
            "--to", "notebook",
            "--execute", str(notebook_path),
            "--output", output_name,
            "--ExecutePreprocessor.timeout=600"
        ]

        print(f"Executing: {notebook_path.name}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=700)

        if result.returncode == 0:
            output_path = notebook_path.parent / output_name
            print(f"  ✓ Success: {output_path.name}")
            # Replace original with executed version
            if output_path.exists():
                output_path.replace(notebook_path)
            return True
        else:
            print(f"  ✗ Failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:200]}")
        return False

def main():
    notebooks_dir = Path("notebooks")

    # Find all notebooks (03-32)
    notebooks = []
    for i in range(3, 33):
        pattern = f"{i:02d}_*.ipynb"
        matches = list(notebooks_dir.glob(pattern))
        if matches:
            # Filter out any _executed versions
            matches = [m for m in matches if "_executed" not in m.name]
            if matches:
                notebooks.append(matches[0])

    print(f"Found {len(notebooks)} notebooks to execute\n")

    success_count = 0
    for nb in notebooks:
        if execute_notebook(nb):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"Execution complete: {success_count}/{len(notebooks)} successful")

if __name__ == "__main__":
    main()
