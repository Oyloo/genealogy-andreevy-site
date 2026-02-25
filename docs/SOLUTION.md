# Genealogy Site - Technical Solution & Architecture

## 🏗️ Architecture Overview

- **Core:** Vanilla JS (Single Page App within `index.html`).
- **Data:** Pre-processed `data.json` (from GEDCOM).
- **Renderer:** Custom SVG engine (D3-like data binding, but simpler) + HTML DOM for nodes.
- **Layout:** Custom DAG (Directed Acyclic Graph) algorithm.
- **Testing:** Local Playwright (`scripts/check_layout.py`) + GitHub Pages deployment.

## 🖼️ Rendering Pipeline

1. **Load Data:** `init()` fetches `data.json`.
2. **Build Graph:** `buildGraphModel()` processes people/families into:
   - `PEOPLE` array (nodes).
   - `FAMS` array (edges/families).
   - `occupancy` grid (for collision avoidance).
3. **Layout Calculation:**
   - **Generation:** Place nodes on Y-axis based on generation.
   - **Spouse Pairing:** Align partners horizontally.
   - **Collision:** Iterate through levels to minimize X-overlap.
   - **Routing:** Compute edge paths avoiding node rects.
4. **Draw:** `drawGraph()` renders SVG elements:
   - **Nodes:** `<g>` groups with `<rect>` + `<text>`.
   - **Edges:** Colored `<path>` or `<line>` elements (polylines).
   - **Marriage Dots:** Circular hubs connecting parents -> children.

## 📱 Mobile-First Layout Strategy

### Viewport & CSS
- **Meta:** `viewport-fit=cover` ensures content extends into the "notch" area on iPhone X+.
- **Body:** `min-height: 100vh` + `min-height: 100dvh` (dynamic viewport height) handles address bar show/hide.
- **Touch:** `touch-action: manipulation` disables browser double-tap zoom, allowing custom gesture handlers.
- **Reset:** `* { margin:0; padding:0; box-sizing:border-box }` ensures full control.

### Gestures (Custom Implementation)
- **Pan:** `touchstart` + `touchmove` tracks 1 finger (delta X/Y).
- **Zoom:** Tracks 2 fingers (distance change).
- **Inertia:** `requestAnimationFrame` loop decays velocity after release.
- **Double Tap:** Custom timer (<300ms) triggers smart zoom to tapped point.

## 🖥️ Desktop Layout Fix (2026-02-25)

- **Problem:** Graph canvas would disappear (turn black) or grow indefinitely on desktop.
- **Solution:**
  - Desktop (`>1100px`): `body { height: 100dvh; overflow: hidden }`.
  - Layout: `display: grid; grid-template-rows: minmax(0, 1fr)`.
  - Graph Container: `flex: 1` to fill available vertical space.
  - This forces the SVG to have a fixed pixel dimension, allowing correct rendering.

## 📦 Data Structure (`data.json`)
```json
{
  "meta": { ... },
  "people": [
    {
      "id": "I1",
      "name": "Given Name",
      "surname": "FamilyName",
      "sex": "M",
      "birth": [{ "date": "...", "place": "..." }],
      "death": [...],
      "famc": "F1", // Child of family
      "fams": ["F2"] // Spouse in family
    }
  ],
  "families": [
    {
      "id": "F1",
      "husb": "I1",
      "wife": "I2",
      "children": ["I3", "I4"]
    }
  ]
}
```
