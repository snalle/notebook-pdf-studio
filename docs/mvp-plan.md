# MVP Plan

## Purpose

The MVP turns the validated Proof of Concept into a usable application for converting Jupyter notebooks into polished digital and printable PDFs through a visual interface.

The MVP assumes that the PoC has already proven:

- `.ipynb` parsing works
- notebook content can be rendered as paginated HTML
- code blocks can be kept together or split across pages
- manual code-line page breaks work
- browser preview and PDF export can use the same rendering system
- Chromium / Playwright can generate the final PDF reliably

The MVP is therefore not about proving the rendering architecture.

It is about making the workflow useful, repeatable, and easy to use.

---

## Core MVP Goal

A user should be able to:

```text
Open a Jupyter notebook
    ↓
See it as paginated pages
    ↓
Select notebook blocks visually
    ↓
Customize layout and styling
    ↓
Control code pagination
    ↓
Resize figures and adjust spacing
    ↓
Switch between Digital and Print views
    ↓
Save the layout configuration
    ↓
Export a polished PDF
```

The user should not need to use the terminal, edit JSON manually, or write CSS.

---

## Primary User

The MVP is initially designed for a single local user.

No account system, cloud backend, collaboration system, or multi-user support is required.

The application should run locally.

---

## MVP User Experience

The main interface should contain three areas:

```text
┌──────────────────────────────────────────────────────────────┐
│ Open   Save         Digital / Print          Export PDF      │
├──────────────┬─────────────────────────────┬─────────────────┤
│              │                             │                 │
│ DOCUMENT     │       PAGE PREVIEW          │    INSPECTOR    │
│              │                             │                 │
│ Introduction │       ┌─────────────┐       │ Selected block  │
│  Markdown    │       │   Page 1    │       │                 │
│  Code        │       │             │       │ Controls        │
│  Figure      │       └─────────────┘       │                 │
│              │                             │                 │
│ Results      │       ┌─────────────┐       │                 │
│  Table       │       │   Page 2    │       │                 │
│              │       └─────────────┘       │                 │
└──────────────┴─────────────────────────────┴─────────────────┘
```

The interface should feel like a lightweight document-layout editor rather than a notebook editor.

---

# 1. Notebook Input

The MVP must be able to open local `.ipynb` files.

The notebook should be parsed into the application's own document model.

The source notebook must not be modified.

Supported notebook content should include:

- Markdown cells
- Python code cells
- plain text output
- images
- Matplotlib-style plots
- SVG output
- basic HTML output
- basic DataFrame / table output

Unsupported output types should fail gracefully rather than breaking the document.

---

# 2. Internal Document Model

Notebook content should be converted into block types such as:

```text
Document
├── MarkdownBlock
├── CodeBlock
├── OutputBlock
├── FigureBlock
├── TableBlock
├── PageBreak
└── SpacerBlock
```

The document model should be independent of both React and the original notebook.

This allows layout settings to be changed without modifying `.ipynb` content.

---

# 3. Document Navigation

The frontend should include a document outline or block navigator.

The user should be able to:

- select a block
- identify its type
- show or hide the block
- show or hide code separately from output
- move between sections quickly
- see which block is currently selected

Optional reordering may be included if it is simple to implement, but it is not required for MVP completion.

---

# 4. Page Preview

The main preview should display actual paginated pages.

The preview should support:

- A4
- Letter
- portrait
- landscape
- zoom
- visible page boundaries
- multiple pages
- page numbers in the editor

The preview and PDF export must continue to use the same underlying rendering system established in the PoC.

---

# 5. Digital and Print Profiles

The MVP should support two document profiles:

```text
Digital
Print
```

## Digital

Optimized for:

- screen reading
- clickable links
- efficient use of page space
- slightly more compact layout
- digital navigation

## Print

Optimized for:

- physical printing
- safer page margins
- stable pagination
- high-quality figures
- code blocks that do not split awkwardly
- page numbering
- predictable A4 / Letter output

The user should be able to switch between the two from the interface.

---

# 6. Global Page Controls

The document-level inspector should allow the user to configure:

- page size
- orientation
- margins
- default body font size
- default code font size
- default line spacing
- page numbers
- basic header / footer settings

Advanced publishing options are not required.

---

# 7. Styling System

The MVP should use a hierarchy:

```text
Built-in theme
      ↓
Document defaults
      ↓
Block-type defaults
      ↓
Individual block overrides
```

This allows most of the notebook to be styled globally while still permitting exceptions.

The user should not need to edit CSS or JSON directly.

---

# 8. Basic Themes

The MVP should include a small number of built-in themes.

Suggested themes:

```text
Minimal
Technical Report
Academic
```

Themes should control:

- body typography
- heading typography
- code styling
- figure spacing
- table styling
- page spacing

The user can override theme defaults through the UI.

A large theme library is not required.

---

# 9. Code Block Controls

Code blocks are a core MVP feature.

For a selected code block, the user should be able to configure:

- show / hide code
- show / hide output
- font size
- line height
- line numbers
- syntax highlighting theme
- background
- padding
- line wrapping
- spacing before / after
- width
- page-break behavior

Code must remain selectable text.

---

# 10. Code Pagination

The MVP should provide a polished version of the pagination controls proven in the PoC.

Supported modes:

```text
Automatic
Keep together
Allow splitting
Manual splitting
Start on new page
```

## Automatic

The layout engine decides based on available page space and block size.

## Keep Together

If the block fits on one page, it should not be split unnecessarily.

## Allow Splitting

Long code blocks may span multiple pages.

Splits must happen between code lines.

## Manual Splitting

The user should be able to place a manual page break between selected lines.

The MVP should improve on the PoC's numeric input and provide a more visual interaction where practical.

Example:

```text
29  model.fit(...)
30
31  predictions = model.predict(...)

────────────── PAGE BREAK ──────────────

32  accuracy = ...
33  print(accuracy)
```

---

# 11. Code Continuation Options

When a code block spans multiple pages, the user should optionally be able to enable:

- continued line numbering
- repeated code-block header
- "continued" label
- repeated cell identifier

Example:

```text
Code Cell 12 · continued
```

These should be simple optional controls.

---

# 12. Markdown Controls

The user should be able to configure:

- visibility
- spacing before / after
- width
- alignment
- page break before
- page break after
- keep heading with following content

The MVP does not need to become a Markdown editor.

The notebook remains the source of truth for content.

---

# 13. Figure Controls

For figures and static images, the user should be able to configure:

- width
- alignment
- spacing before / after
- keep together
- page break before
- page break after
- basic caption text
- keep caption with figure

Figure resizing should be visually simple.

---

# 14. Table Controls

Basic table support should include:

- font size
- width
- alignment
- page splitting
- repeat header row when spanning pages where practical
- overflow warning for overly wide tables

Advanced spreadsheet-like formatting is not required.

---

# 15. Manual Page Breaks

The user should be able to insert page breaks between document blocks.

A page break should be visible in the editor.

Example:

```text
Markdown block

──────────── PAGE BREAK ────────────

Code block
```

The break should exist only in the layout configuration.

---

# 16. Layout Configuration

All document customizations should be saved separately from the notebook.

Example:

```text
analysis.ipynb
analysis.nbpdf.json
```

The configuration file should include:

- document profile
- page settings
- theme
- block-type defaults
- individual block overrides
- manual page breaks
- code split positions
- figure sizing
- visibility settings

The original notebook should remain unchanged.

---

# 17. Configuration Persistence

The user should be able to:

```text
Open notebook
    ↓
Customize layout
    ↓
Save
    ↓
Close application
    ↓
Open notebook later
    ↓
Previous layout returns
```

This is a required MVP capability.

---

# 18. Basic / Advanced Controls

The UI should avoid overwhelming users.

The inspector should provide:

```text
Basic
Advanced
```

## Basic

Show common controls such as:

- visibility
- font size
- alignment
- page-break behavior
- code split mode
- figure width
- spacing

## Advanced

Show more detailed controls such as:

- exact line height
- exact padding
- continuation labels
- per-side spacing
- block-specific overrides

The majority of common tasks should be possible in Basic mode.

---

# 19. Export

The user should be able to export the current document as PDF.

The export flow should be simple:

```text
Export PDF
    ↓
Choose Digital or Print
    ↓
Generate
```

The exported PDF should preserve:

- selectable text
- syntax highlighting
- links where supported
- page breaks
- code split locations
- figures
- tables
- page numbers
- headers / footers where enabled

---

# 20. Local Application

The MVP can run locally as:

```text
React frontend
       ↓
localhost
       ↓
FastAPI backend
```

Desktop packaging is not required for MVP completion.

The user may still need to start the development server during MVP development.

A fully packaged desktop application belongs to a later milestone.

---

# 21. Error Handling

The application should fail gracefully.

Examples:

```text
Unsupported Jupyter output
→ show placeholder or warning

Missing image
→ show visible error block

Very wide table
→ show layout warning

Code block cannot fit
→ show pagination warning
```

One problematic notebook cell should not cause the whole document to fail.

---

# 22. Example Notebooks

The repository should contain multiple test notebooks covering common cases.

Suggested examples:

```text
examples/
├── simple.ipynb
├── code-heavy.ipynb
├── figures.ipynb
├── tables.ipynb
└── mixed-report.ipynb
```

These notebooks should be used during development to prevent regressions.

---

# 23. MVP Success Criteria

The MVP is considered successful when a user can complete the following workflow without manually editing code, JSON, or CSS:

- [ ] Open a real `.ipynb` notebook.
- [ ] View it as actual paginated pages.
- [ ] Navigate through notebook blocks.
- [ ] Select a block visually.
- [ ] Hide or show code and output independently.
- [ ] Change code styling.
- [ ] Keep a code block on one page.
- [ ] Allow a long code block to span multiple pages.
- [ ] Manually split a code block between chosen lines.
- [ ] Insert a page break between notebook blocks.
- [ ] Resize a figure.
- [ ] Adjust page size and margins.
- [ ] Switch between Digital and Print profiles.
- [ ] Apply a built-in theme.
- [ ] Override an individual block's styling.
- [ ] Save the layout configuration.
- [ ] Reopen the notebook and recover the saved layout.
- [ ] Export a PDF.
- [ ] Confirm that the PDF closely matches the preview.

---

# 24. Real-Notebook Validation

Before declaring the MVP complete, test it against several different notebooks rather than only the PoC notebook.

At minimum:

```text
1 code-heavy notebook
1 notebook with many plots
1 notebook with tables
1 mixed analysis/report notebook
```

The goal is not to support every possible Jupyter notebook.

The goal is to handle common Python analysis notebooks reliably.

---

# 25. Explicitly Out of Scope

The MVP will not include:

- editing notebook source code
- executing notebook cells
- kernel management
- real-time collaboration
- user accounts
- cloud synchronization
- cloud notebook storage
- comments
- version-history UI
- arbitrary Jupyter widget support
- every possible MIME output type
- commercial print / CMYK workflows
- crop marks
- bleed
- Word export
- PowerPoint export
- presentation mode
- mobile editor
- plugin marketplace
- desktop application packaging
- AI layout generation

These may be considered after the MVP.

---

# 26. Features Deferred to v1+

Features that may be added after the MVP include:

- undo / redo
- multi-select
- copy / paste styling
- drag-and-drop block reordering
- richer theme customization
- theme import / export
- table of contents
- PDF bookmarks
- advanced headers / footers
- duplex binding margins
- section breaks
- title-page designer
- sophisticated table pagination
- visual margin dragging
- keyboard shortcuts
- desktop packaging
- recent-project list
- automatic layout recommendations

---

# 27. MVP Completion Rule

The MVP is complete when the core workflow is pleasant and reliable.

Do not delay MVP completion solely to add more styling options.

A feature should only be added during MVP development if it materially improves this workflow:

```text
Open
→ Customize
→ Preview
→ Save
→ Export
```

Everything else can wait.

---

# 28. Relationship to the PoC

The project stages are:

```text
PoC
│
│ Proves rendering architecture
│ and controllable pagination
▼
MVP
│
│ Turns the proven renderer into
│ a usable visual application
▼
v1+
│
│ Adds polish, advanced workflows,
│ packaging, and broader capabilities
▼
```

The PoC should not grow into the MVP.

The MVP should reuse or refactor the successful PoC rendering approach rather than rebuilding it unnecessarily.

---

## Final MVP Definition

The MVP succeeds when Notebook PDF Studio is something the user can genuinely use to turn an existing Jupyter notebook into a polished digital or printable PDF through an intuitive visual interface, without manually editing the notebook, CSS, JSON, or PDF files.