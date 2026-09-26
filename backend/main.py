"""Run the Notebook PDF Studio proof of concept."""

from pathlib import Path
from backend.notebook.loader import load_notebook

notebook_path = Path("examples/poc.ipynb")
blocks = load_notebook(str(notebook_path))

for block in blocks:
    print(type(block).__name__)
    print(block)
    print("-" * 50)