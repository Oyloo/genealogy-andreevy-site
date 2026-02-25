# Genealogy Site (Custom Renderer)

A lightweight, mobile-first genealogy visualizer for the Andreevy family tree.

## 📁 Project Structure

- **`index.html`**: The entire application logic (JS + CSS + HTML). No build step required.
- **`data.json`**: Pre-processed family tree data (generated from GEDCOM).
- **`docs/`**: Project documentation (PRD, Solution, Debugging, Decisions).
- **`scripts/`**: Utility scripts (layout checks).

## 🚀 Quick Start

1.  **Serve Locally:**
    ```bash
    python3 -m http.server 8089
    ```
2.  **Open in Browser:**
    Navigate to `http://localhost:8089`.

## 🛠️ Development

- **No Frameworks:** Vanilla JS + SVG.
- **Mobile First:** Designed for iOS Safari (PWA-like feel).
- **Debugging:** See `docs/DEBUGGING.md` for local layout checks.

## 📚 Documentation

- [Product Requirements (PRD)](docs/PRD.md)
- [Architecture & Solution](docs/SOLUTION.md)
- [Debugging Guide](docs/DEBUGGING.md)
- [Decision Log](docs/DECISIONS.md)
- [Rendering Rules](RENDERING-RULES.md)
