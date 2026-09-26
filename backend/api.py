"""Provide the HTTP API for Notebook PDF Studio."""

from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from backend.models import (
    CodeBlock,
    FigureBlock,
    MarkdownBlock,
    TextOutputBlock,
)
from backend.notebook.loader import load_notebook
from backend.render import render_html


class CodeBlockOverride(BaseModel):
    """Define optional layout overrides for a code block."""

    font_size: float | None = None
    pagination: Literal[
        "auto",
        "keep-together",
        "allow-split",
        "manual",
    ] | None = None
    manual_breaks: list[int] | None = None


class RenderRequest(BaseModel):
    """Define a notebook HTML rendering request."""

    notebook: str
    overrides: dict[str, CodeBlockOverride] = Field(
        default_factory=dict
    )


app = FastAPI(
    title="Notebook PDF Studio",
    version="0.1.0",
)


@app.get("/api/health")
def health() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}


@app.get("/api/notebook")
def get_notebook(
    notebook: str,
) -> dict[str, list[dict[str, object]]]:
    """Return the document blocks contained in a notebook.

    Args:
        notebook: Path to the Jupyter notebook file.

    Returns:
        Serializable metadata for the notebook's document blocks.

    Raises:
        HTTPException: If the requested notebook does not exist.
    """
    notebook_path = Path(notebook)

    if not notebook_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Notebook not found: {notebook}",
        )

    blocks = load_notebook(str(notebook_path))
    serialized_blocks: list[dict[str, object]] = []

    for block in blocks:
        if isinstance(block, MarkdownBlock):
            serialized_blocks.append(
                {
                    "id": block.id,
                    "kind": "markdown",
                    "source": block.source,
                }
            )

        elif isinstance(block, CodeBlock):
            serialized_blocks.append(
                {
                    "id": block.id,
                    "kind": "code",
                    "source": block.source,
                    "language": block.language,
                    "font_size": block.font_size,
                    "pagination": block.pagination,
                    "manual_breaks": block.manual_breaks,
                }
            )

        elif isinstance(block, TextOutputBlock):
            serialized_blocks.append(
                {
                    "id": block.id,
                    "kind": "text-output",
                    "text": block.text,
                }
            )

        elif isinstance(block, FigureBlock):
            serialized_blocks.append(
                {
                    "id": block.id,
                    "kind": "figure",
                    "mime_type": block.mime_type,
                }
            )

    return {"blocks": serialized_blocks}


@app.post("/api/render", response_class=HTMLResponse)
def render_notebook(request: RenderRequest) -> HTMLResponse:
    """Render a notebook as HTML with optional code-block overrides.

    Args:
        request: Notebook path and optional block-specific layout settings.

    Returns:
        Rendered notebook HTML.

    Raises:
        HTTPException: If the requested notebook does not exist.
    """
    notebook_path = Path(request.notebook)

    if not notebook_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Notebook not found: {request.notebook}",
        )

    blocks = load_notebook(str(notebook_path))

    for block in blocks:
        if not isinstance(block, CodeBlock):
            continue

        override = request.overrides.get(block.id)

        if override is None:
            continue

        if override.font_size is not None:
            block.font_size = override.font_size

        if override.pagination is not None:
            block.pagination = override.pagination

        if override.manual_breaks is not None:
            block.manual_breaks = override.manual_breaks

    output_path = Path("build/api_preview.html")

    rendered_path = render_html(
        blocks=blocks,
        output_path=output_path,
    )

    html = rendered_path.read_text(encoding="utf-8")

    return HTMLResponse(content=html)