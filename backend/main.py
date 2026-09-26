"""Run the Notebook PDF Studio proof of concept."""

from pathlib import Path

from backend.models import CodeBlock
from backend.notebook.loader import load_notebook
from backend.pdf import export_pdf
from backend.render import render_html


notebook_path = Path("examples/poc_pagination_test.ipynb")

html_path = Path("build/poc_pagination_test.html")
pdf_path = Path("build/poc_pagination_test.pdf")

blocks = load_notebook(notebook_path)

code_blocks = [
    block
    for block in blocks
    if isinstance(block, CodeBlock)
]

# Short first code block stays automatic.
code_blocks[0].pagination = "auto"

# Long code block: manually force a page break after source line 40.
code_blocks[1].pagination = "manual"
code_blocks[1].manual_breaks = [40]

# Medium code block should remain on one page when possible.
code_blocks[2].pagination = "keep-together"

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