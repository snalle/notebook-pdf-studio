"""Data models used by Notebook PDF Studio.

This module defines the document blocks created when a Jupyter notebook
is parsed into the application's internal document representation.
"""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class MarkdownBlock:
    """Represent a Markdown block."""

    id: str
    source: str


@dataclass
class CodeBlock:
    """Represent a source-code block and its layout settings."""

    id: str
    source: str
    language: str = "python"
    font_size: float = 9.0

    pagination: Literal[
        "auto",
        "keep-together",
        "allow-split",
        "manual",
    ] = "auto"

    manual_breaks: list[int] = field(default_factory=list)


@dataclass
class TextOutputBlock:
    """Represent plain-text output from a notebook cell."""

    id: str
    text: str


@dataclass
class FigureBlock:
    """Represent a static figure produced by a notebook cell."""

    id: str
    mime_type: str
    data: str


type DocumentBlock = (
    MarkdownBlock
    | CodeBlock
    | TextOutputBlock
    | FigureBlock
)