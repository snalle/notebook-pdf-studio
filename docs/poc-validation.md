# PoC Validation

This document records the results of the Notebook PDF Studio proof of concept.

The PoC focused on validating the core technical assumptions behind notebook parsing, HTML/PDF rendering, code-block pagination, per-block customization, API integration, and a minimal React frontend.

## PoC validation results

The proof of concept successfully validated the core technical assumptions behind Notebook PDF Studio.

### Notebook parsing

Validated support for reading saved Jupyter notebooks and converting supported content into an internal document model.

Confirmed support for:

- Markdown cells
- Python code cells
- Plain-text outputs
- Static PNG figure outputs

### HTML rendering

Validated conversion of document blocks into styled HTML.

Confirmed that:

- Markdown renders correctly
- Python code is syntax highlighted
- Code remains selectable text
- Text outputs render separately from code
- Static notebook figures render correctly

### PDF rendering

Validated PDF export using Chromium through Playwright.

Confirmed that:

- The rendered HTML can be exported to A4 PDF
- Syntax highlighting and layout are preserved
- Text remains selectable in the PDF
- Static figures are preserved
- The same HTML renderer is used as the basis for preview and PDF export

### Code pagination

Validated the three planned code-block pagination behaviors:

- `allow-split`: long code blocks can continue across page boundaries
- `keep-together`: code blocks that fit on one page can be moved intact to the next page
- `manual`: a code block can be split after a specified source-code line

Manual pagination was tested by inserting a forced break after source line 40. The rendered PDF resumed with the following source line on the next page.

The remaining portion of a manually split code block can still be automatically paginated by Chromium when required.

### Per-block customization

Validated per-code-block rendering overrides.

Confirmed that individual code blocks can receive:

- Code font size
- Pagination mode
- Manual break line positions

These settings are represented in the internal document model and affect the rendered HTML and PDF.

### API

Validated a minimal FastAPI layer.

Confirmed that the API can:

- Load notebook block metadata
- Expose block IDs to the frontend
- Accept block-specific rendering overrides
- Return rendered HTML
- Export a PDF using the same overrides

### React frontend

Validated a minimal React frontend.

Confirmed that a user can:

- Load a notebook
- View its code blocks
- Select a code block
- Change its font size
- Select a pagination mode
- Enter a manual break line
- Update the HTML preview
- Export a PDF using the selected settings

### PoC conclusion

The main technical risk has been validated: Notebook PDF Studio can treat notebook code cells as layout-aware document objects and give users explicit control over how those code blocks behave across PDF page boundaries.

The PoC is therefore considered complete.

The main usability limitation remaining is that the browser preview does not yet display true visual page boundaries. Building a paginated, WYSIWYG-style preview is deferred to the MVP.

## Conclusion

The proof of concept successfully validated the core rendering and pagination approach.

The PoC is considered complete.

The main usability gap is the lack of a true paginated browser preview with visible page boundaries. That work is deferred to the MVP.