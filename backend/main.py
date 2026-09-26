"""Run the Notebook PDF Studio proof of concept."""

from pathlib import Path

from backend.notebook.loader import load_notebook
from backend.pdf import export_pdf
from backend.render import render_html


notebook_path = Path("examples/poc_figure_test.ipynb")

html_path = Path("build/poc_figure_test.html")
pdf_path = Path("build/poc_figure_test.pdf")

blocks = load_notebook(notebook_path)

rendered_html = render_html(
    blocks=blocks,
    output_path=html_path,
)

rendered_pdf = export_pdf(
    html_path=rendered_html,
    output_path=pdf_path,
)

print(f"Rendered HTML: {rendered_html.resolve()}")
print(f"Rendered PDF:  {rendered_pdf.resolve()}")