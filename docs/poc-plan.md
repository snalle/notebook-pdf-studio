# Proof of Concept Plan

## Purpose

The purpose of the PoC is to prove that Notebook PDF Studio can take a Jupyter notebook, render it as real paginated pages, allow basic control over code-block pagination, and export a PDF that closely matches the browser preview.

The PoC is **not** intended to be a polished or complete product.

Its job is to validate the core rendering approach before building the MVP.

---

## Core Question

Can we build this rendering pipeline reliably?

```text
.ipynb
  ↓
Notebook parser
  ↓
Simple document model
  ↓
HTML + CSS
  ↓
Paginated browser preview
  ↓
Chromium
  ↓
PDF
```

The most important requirement is:

> The browser preview and exported PDF should have effectively the same layout.

---

## Scope

The PoC will use **one controlled test notebook**.

It only needs to support:

- Markdown cells
- Python code cells
- Plain text output
- One or more static images/plots

Other notebook content can be ignored for now.

---

## PoC Features

### 1. Open a test notebook

The backend must be able to load a `.ipynb` file using Python.

The notebook should be converted into a small internal document representation.

Required block types:

```text
MarkdownBlock
CodeBlock
OutputBlock
FigureBlock
PageBreak
```

---

### 2. Render Markdown

Markdown cells should render as normal HTML.

The PoC only needs basic support for:

- headings
- paragraphs
- lists
- inline code
- code fences

Advanced Markdown behavior is not required.

---

### 3. Render Python code

Python code must:

- remain selectable text
- preserve indentation
- use syntax highlighting
- use a monospace font
- preserve line boundaries

The code must not be converted into an image.

---

## Code Block Controls

The PoC only needs a small number of code controls.

For one selected code block, the user should be able to change:

### Font size

Example:

```text
Font size

[ 9 pt ]
```

### Pagination mode

The following modes must be demonstrated:

```text
Automatic
Keep together
Allow splitting
Manual split
```

---

## Keep Together

If a code block fits on one page but does not fit in the remaining space on the current page, it should move to the next page.

Example:

```text
Page 1

previous content
previous content


Page 2

entire code block
```

The code block should not split unnecessarily.

---

## Allow Splitting

A long code block may span multiple pages.

It must only split **between code lines**.

For example:

```text
Page 1

21  ...
22  ...
23  ...
24  ...


Page 2

25  ...
26  ...
27  ...
```

The renderer must not visually cut a line in half.

---

## Manual Code Split

The user must be able to specify a line after which a page break should occur.

For the PoC, this can be a simple numeric control.

Example:

```text
Manual page break after line:

[ 31 ]
```

Result:

```text
29  model.fit(...)
30
31  predictions = model.predict(...)

------------- PAGE BREAK -------------

32  accuracy = ...
33  print(accuracy)
```

A visual line-break editor is **not required** for the PoC.

That belongs in the MVP.

---

## Page Layout

The PoC only needs to support:

```text
Paper:       A4
Orientation: Portrait
Margins:     fixed
```

Letter size, landscape mode, and customizable margins are not required yet.

---

## Preview

The browser should display the document as visible A4 pages.

Example:

```text
┌─────────────────────────┐
│                         │
│         Page 1          │
│                         │
│ Markdown                │
│                         │
│ Code                    │
│                         │
└─────────────────────────┘

┌─────────────────────────┐
│                         │
│         Page 2          │
│                         │
│ Code continued          │
│                         │
│ Figure                  │
│                         │
└─────────────────────────┘
```

The preview does not need advanced zoom controls or polished page navigation.

---

## Frontend

Use React and TypeScript.

The PoC frontend should be intentionally simple.

It only needs:

```text
┌────────────────────────────────────────────┐
│ Notebook PDF Studio — PoC                  │
├──────────────────┬─────────────────────────┤
│                  │                         │
│ Selected block   │      A4 Preview         │
│                  │                         │
│ Font size        │                         │
│ [ 9 pt ]         │                         │
│                  │                         │
│ Pagination       │                         │
│ [ Auto ▼ ]       │                         │
│                  │                         │
│ Manual line      │                         │
│ [ 31 ]           │                         │
│                  │                         │
│ [ Export PDF ]   │                         │
│                  │                         │
└──────────────────┴─────────────────────────┘
```

The interface does **not** need to look polished.

---

## Backend

Use Python and FastAPI.

The backend is responsible for:

- reading the notebook
- creating the document model
- rendering HTML
- rendering syntax-highlighted code
- applying pagination rules
- generating the final PDF

---

## PDF Generation

Use Chromium through Playwright.

The same HTML/CSS rendering should be used for both:

```text
browser preview
```

and

```text
PDF export
```

The PoC should avoid having two separate rendering systems.

---

## Suggested Technologies

### Frontend

```text
React
TypeScript
Vite
```

### Backend

```text
Python
FastAPI
nbformat
Pygments
Jinja2
```

### PDF

```text
Playwright
Chromium
```

---

## Test Notebook

Create one notebook specifically for the PoC.

Suggested contents:

```text
Cell 1
Markdown heading and paragraph

Cell 2
Short Python code block

Cell 3
Plain text output

Cell 4
Long Python code block
approximately 50–80 lines

Cell 5
Markdown paragraph

Cell 6
Simple Matplotlib figure
```

The notebook should deliberately contain a long code block so pagination can be tested.

---

## Success Criteria

The PoC is successful when all of the following work:

- [ ] A `.ipynb` file can be loaded.
- [ ] Markdown renders correctly.
- [ ] Python code renders with syntax highlighting.
- [ ] Code remains selectable text.
- [ ] Plain text output renders.
- [ ] A static figure renders.
- [ ] The document is shown as A4 pages.
- [ ] A code block can be kept on one page.
- [ ] A long code block can split between lines.
- [ ] A manual page break can be inserted after a chosen code line.
- [ ] Code font size can be changed from the frontend.
- [ ] The preview updates after changing settings.
- [ ] The document can be exported as a PDF.
- [ ] The PDF layout closely matches the browser preview.

---

## Most Important Validation

The most important PoC test is:

```text
Open notebook
    ↓
Select long code block
    ↓
Set manual split after line 31
    ↓
Preview shows break after line 31
    ↓
Export PDF
    ↓
PDF also breaks after line 31
```

If this works reliably, the core architecture is considered validated.

---

## Explicitly Out of Scope

The PoC will **not** include:

- polished UI
- drag-and-drop
- visual line-break insertion
- notebook editing
- notebook execution
- saved projects
- theme system
- Digital / Print profiles
- Letter page size
- landscape mode
- customizable margins
- headers
- footers
- page numbers
- table of contents
- undo / redo
- multi-select
- copy/paste styles
- reusable themes
- complex DataFrames
- advanced table pagination
- interactive Jupyter widgets
- cloud storage
- authentication
- collaboration
- desktop packaging
- Word export
- PowerPoint export

These belong to later stages.

---

## PoC Completion Rule

Do not expand the PoC just because another feature seems useful.

If a feature is not required to answer:

> “Can notebook content be visually paginated and exported to a matching PDF with controllable code splitting?”

then it should probably wait for the MVP.

---

## What Happens After the PoC

If the PoC succeeds:

```text
PoC
 ↓
Architecture validated
 ↓
Refactor reusable rendering code
 ↓
Build MVP
```

The MVP can then focus on usability:

- proper notebook navigation
- visual block selection
- better inspectors
- page-size controls
- figure resizing
- saved `.nbpdf.json` configuration
- Digital / Print profiles
- themes
- more notebook output types
- better automatic pagination

If the PoC fails to achieve reliable preview/PDF consistency, the rendering architecture should be reconsidered before building the MVP.