"""Run the Notebook PDF Studio proof of concept."""

from pathlib import Path

from backend.notebook.loader import load_notebook
from backend.render import render_html


notebook_path = Path("examples/poc.ipynb")
output_path = Path("build/poc.html")

blocks = load_notebook(notebook_path)

rendered_path = render_html(
    blocks=blocks,
    output_path=output_path,
)

print(f"Rendered HTML: {rendered_path.resolve()}")