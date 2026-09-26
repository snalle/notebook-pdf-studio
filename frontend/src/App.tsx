import { useState } from "react";
import "./App.css";

type PaginationMode =
  | "auto"
  | "keep-together"
  | "allow-split"
  | "manual";

type NotebookBlock = {
  id: string;
  kind: string;
  source?: string;
  text?: string;
  language?: string;
  font_size?: number;
  pagination?: PaginationMode;
  manual_breaks?: number[];
};

type CodeOverride = {
  font_size?: number;
  pagination?: PaginationMode;
  manual_breaks?: number[];
};

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [notebook, setNotebook] = useState(
    "examples/poc_pagination_test.ipynb",
  );

  const [blocks, setBlocks] = useState<NotebookBlock[]>([]);
  const [selectedBlockId, setSelectedBlockId] = useState<string | null>(
    null,
  );
  const [overrides, setOverrides] = useState<
    Record<string, CodeOverride>
  >({});
  const [previewHtml, setPreviewHtml] = useState("");

  const selectedBlock = blocks.find(
    (block) => block.id === selectedBlockId,
  );

  const selectedOverride =
    selectedBlockId === null
      ? undefined
      : overrides[selectedBlockId];

  async function loadNotebook() {
    const response = await fetch(
      `${API_URL}/api/notebook?notebook=${encodeURIComponent(notebook)}`,
    );

    if (!response.ok) {
      throw new Error("Could not load notebook.");
    }

    const data = await response.json();

    setBlocks(data.blocks);
    setOverrides({});
    setPreviewHtml("");

    const firstCodeBlock = data.blocks.find(
      (block: NotebookBlock) => block.kind === "code",
    );

    setSelectedBlockId(firstCodeBlock?.id ?? null);
  }

  function updateSelectedOverride(
    update: Partial<CodeOverride>,
  ) {
    if (selectedBlockId === null) {
      return;
    }

    setOverrides((current) => ({
      ...current,
      [selectedBlockId]: {
        ...current[selectedBlockId],
        ...update,
      },
    }));
  }

  async function renderPreview() {
    const response = await fetch(`${API_URL}/api/render`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        notebook,
        overrides,
      }),
    });

    if (!response.ok) {
      throw new Error("Could not render notebook.");
    }

    const html = await response.text();
    setPreviewHtml(html);
  }

  async function exportPdf() {
    const response = await fetch(`${API_URL}/api/export`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        notebook,
        overrides,
      }),
    });

    if (!response.ok) {
      throw new Error("Could not export PDF.");
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;

    const filename =
      notebook.split("/").pop()?.replace(".ipynb", ".pdf") ??
      "notebook.pdf";

    link.download = filename;
    link.click();

    URL.revokeObjectURL(url);
  }

  const fontSize =
    selectedOverride?.font_size ??
    selectedBlock?.font_size ??
    9;

  const pagination =
    selectedOverride?.pagination ??
    selectedBlock?.pagination ??
    "auto";

  const manualBreaks =
    selectedOverride?.manual_breaks ??
    selectedBlock?.manual_breaks ??
    [];

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>Notebook PDF Studio</h1>

        <label>
          Notebook
          <input
            value={notebook}
            onChange={(event) =>
              setNotebook(event.target.value)
            }
          />
        </label>

        <button onClick={loadNotebook}>
          Load notebook
        </button>

        <h2>Code blocks</h2>

        <div className="block-list">
          {blocks
            .filter((block) => block.kind === "code")
            .map((block) => (
              <button
                key={block.id}
                className={
                  block.id === selectedBlockId
                    ? "block-button selected"
                    : "block-button"
                }
                onClick={() =>
                  setSelectedBlockId(block.id)
                }
              >
                {block.source?.split("\n")[0] || block.id}
              </button>
            ))}
        </div>

        {selectedBlock?.kind === "code" && (
          <div className="controls">
            <label>
              Font size
              <input
                type="number"
                min="6"
                max="24"
                step="0.5"
                value={fontSize}
                onChange={(event) =>
                  updateSelectedOverride({
                    font_size: Number(event.target.value),
                  })
                }
              />
            </label>

            <label>
              Pagination
              <select
                value={pagination}
                onChange={(event) =>
                  updateSelectedOverride({
                    pagination:
                      event.target.value as PaginationMode,
                  })
                }
              >
                <option value="auto">Auto</option>
                <option value="keep-together">
                  Keep together
                </option>
                <option value="allow-split">
                  Allow splitting
                </option>
                <option value="manual">
                  Manual
                </option>
              </select>
            </label>

            {pagination === "manual" && (
              <label>
                Break after line
                <input
                  type="number"
                  min="1"
                  value={manualBreaks[0] ?? ""}
                  onChange={(event) => {
                    const value = Number(event.target.value);

                    updateSelectedOverride({
                      manual_breaks:
                        value > 0 ? [value] : [],
                    });
                  }}
                />
              </label>
            )}
          </div>
        )}

        <button
          onClick={renderPreview}
          disabled={blocks.length === 0}
        >
          Update preview
        </button>

        <button
        onClick={exportPdf}
        disabled={blocks.length === 0}
>
         Export PDF
        </button>
      </aside>

      <main className="preview-area">
        {previewHtml ? (
          <iframe
            title="Notebook preview"
            srcDoc={previewHtml}
            className="preview-frame"
          />
        ) : (
          <div className="empty-preview">
            Load a notebook and render the preview.
          </div>
        )}
      </main>
    </div>
  );
}



export default App;