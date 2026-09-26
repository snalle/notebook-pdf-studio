"""Load Jupyter notebooks into the internal document model."""

import nbformat

from backend.models import (
    CodeBlock,
    DocumentBlock,
    FigureBlock,
    MarkdownBlock,
    TextOutputBlock,
)


def load_notebook(path: str) -> list[DocumentBlock]:
    """Load a Jupyter notebook and convert it into document blocks.

    Args:
        path: Path to the Jupyter notebook file.

    Returns:
        Document blocks representing supported notebook content.
    """
    notebook = nbformat.read(path, as_version=4)
    blocks: list[DocumentBlock] = []

    for index, cell in enumerate(notebook.cells):
        block_id = cell.get("id", f"cell-{index}")

        if cell.cell_type == "markdown":
            blocks.append(
                MarkdownBlock(
                    id=block_id,
                    source=cell.source,
                )
            )

        elif cell.cell_type == "code":
            blocks.append(
                CodeBlock(
                    id=block_id,
                    source=cell.source,
                )
            )

            for output_index, output in enumerate(
                cell.get("outputs", [])
            ):
                output_id = f"{block_id}-output-{output_index}"

                if output.output_type == "stream":
                    blocks.append(
                        TextOutputBlock(
                            id=output_id,
                            text=output.text,
                        )
                    )

                elif "data" in output:
                    data = output["data"]

                    if "image/png" in data:
                        blocks.append(
                            FigureBlock(
                                id=output_id,
                                mime_type="image/png",
                                data=data["image/png"],
                            )
                        )

    return blocks