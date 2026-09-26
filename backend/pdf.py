"""Export rendered HTML documents to PDF."""

from pathlib import Path
from playwright.sync_api import sync_playwright


def export_pdf(
    html_path: str | Path,
    output_path: str | Path,
) -> Path:
    """Export an HTML document to an A4 PDF.

    Args:
        html_path: Path to the rendered HTML document.
        output_path: Path where the generated PDF should be written.

    Returns:
        Path to the generated PDF file.
    """
    html_path = Path(html_path).resolve()
    output_path = Path(output_path).resolve()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.goto(
            html_path.as_uri(),
            wait_until="networkidle",
        )

        page.emulate_media(media="print")

        page.pdf(
            path=str(output_path),
            format="A4",
            print_background=True,
        )

        browser.close()

    return output_path