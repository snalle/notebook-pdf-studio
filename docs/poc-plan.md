# Proof of Concept Plan

## Goal

Prove that Notebook PDF Studio can turn a Jupyter notebook into
a visually editable, paginated document and export a PDF that
closely matches the preview.

## Questions the PoC must answer

1. Can we reliably parse `.ipynb` files into our own document model?
2. Can we render Markdown, Python code, outputs, and figures cleanly?
3. Can code remain selectable text with syntax highlighting?
4. Can code blocks be kept together or split across pages?
5. Can we manually split a code block between specific lines?
6. Can we render real A4/Letter pages in the browser?
7. Can the browser preview and exported PDF use the same layout?
8. Can React modify layout settings and immediately update the preview?

## PoC scope

### Notebook input

Support:

- Markdown cells
- Python code cells
- Plain text output
- PNG/JPEG/SVG output

Ignore initially:

- Interactive widgets
- Complex HTML outputs
- LaTeX edge cases
- Very complex DataFrames

## Document model

Support these block types:

- MarkdownBlock
- CodeBlock
- OutputBlock
- FigureBlock
- PageBreak

## Code block controls

The PoC must demonstrate:

- Font size
- Syntax highlighting
- Line numbers on/off
- Line wrapping
- Keep block together
- Allow block to split
- Manual page break between code lines

## Page controls

Support:

- A4
- Portrait
- Basic margins
- Manual page break

## Frontend

Create a minimal React interface with:

- Notebook block list
- Page preview
- Selected-block inspector

The UI does not need to be polished yet.

## PDF export

Use the same HTML/CSS layout for:

- Browser preview
- PDF generation

Export through Chromium / Playwright.

## PoC success criteria

The PoC succeeds when we can:

1. Open a test `.ipynb`.
2. Display Markdown, code, output, and a figure.
3. Select a code block in the UI.
4. Change its font size.
5. Choose whether it may split across pages.
6. Add a manual split between two code lines.
7. Insert a page break.
8. See the resulting A4 pages in the preview.
9. Export a PDF.
10. Confirm that the PDF closely matches the preview.

## Explicitly not part of the PoC

- Beautiful UI
- Themes
- Undo/redo
- Multi-select
- Tables beyond very basic HTML
- Digital vs Print profiles
- Headers and footers
- TOC
- Saved projects
- Desktop application packaging
- Notebook editing
- Notebook execution

## PoC outcome

If the PoC succeeds, its rendering and document-model code becomes
the foundation of the MVP.

If pagination or preview/PDF consistency fails, solve that architecture
before building the full editor.