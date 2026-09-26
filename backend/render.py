"""Render Notebook PDF Studio document blocks as HTML."""

from html import escape
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from backend.models import (
    CodeBlock,
    DocumentBlock,
    FigureBlock,
    MarkdownBlock,
    TextOutputBlock,
)


TEMPLATE_DIR = Path(__file__).parent / "templates"


def render_html(
    blocks: list[DocumentBlock],
    output_path: str | Path,
) -> Path:
    """Render document blocks to an HTML file.

    Args:
        blocks: Document blocks to render.
        output_path: Location where the generated HTML file is written.

    Returns:
        Path to the generated HTML file.
    """
    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = environment.get_template("document.html")

    markdown = MarkdownIt("commonmark")
    code_formatter = HtmlFormatter(cssclass="highlight")

    rendered_blocks: list[dict[str, str | float]] = []

    for block in blocks:
        if isinstance(block, MarkdownBlock):
            rendered_blocks.append(
                {
                    "kind": "markdown",
                    "content": markdown.render(block.source),
                }
            )

        elif isinstance(block, CodeBlock):
            rendered_blocks.append(
                {
                    "kind": "code",
                    "content": highlight(
                        block.source,
                        PythonLexer(),
                        code_formatter,
                    ),
                    "font_size": block.font_size,
                    "pagination": block.pagination,
                }
            )

        elif isinstance(block, TextOutputBlock):
            rendered_blocks.append(
                {
                    "kind": "output",
                    "content": f"<pre>{escape(block.text)}</pre>",
                }
            )

        elif isinstance(block, FigureBlock):
            rendered_blocks.append(
                {
                    "kind": "figure",
                    "content": (
                        f'<img src="data:{block.mime_type};base64,'
                        f'{block.data}" alt="Notebook figure">'
                    ),
                }
            )

    document_css = (
        TEMPLATE_DIR / "document.css"
    ).read_text(encoding="utf-8")

    html = template.render(
        blocks=rendered_blocks,
        document_css=document_css,
        pygments_css=code_formatter.get_style_defs(".highlight"),
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    return output_path