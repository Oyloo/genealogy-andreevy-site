# Genealogy Site - Decision Log

## 2026-02-25: Desktop Black Screen Fix

### Context
On desktop (`>1100px`), the graph area ("Связи") was rendering completely black/empty, while mobile layout was fine.

### Diagnosis
The `.layout` container had `height: auto` on desktop, causing it to grow infinitely (2800px+) based on the people list height. The graph SVG was rendered based on `100%` of this infinite container, creating a massive SVG that failed to draw correctly or clipped out of view.

### Decision
- **Fixed Height for Desktop:** Enforced `height: 100dvh` and `overflow: hidden` on `body` for desktop (`>1100px`).
- **Flexible Layout:** Used `grid-template-rows: minmax(0, 1fr)` and `flex: 1` on `.layout` to constrain the graph container to the available viewport height.
- **Result:** The graph container now has a fixed pixel height, allowing the SVG to render correctly and fit the screen.

## 2026-02-25: Remove Duplicate Surname

### Context
The people list displayed names like:
```
👨 Иван Петров
petrov
```
The surname was duplicated below the name in small text.

### Decision
Removed the secondary surname display. Most names already include the surname, so the duplication added visual noise without value.

## 2026-02-25: Remove Fixed Footer

### Context
A fixed black `div` at the bottom was intended to handle safe area insets on mobile but caused scrolling issues and blocked content under the address bar.

### Decision
Removed the fixed footer element entirely. Rely on `viewport-fit=cover` and natural document flow. The black background of `body` handles the safe area appearance seamlessly.

## 2026-02-24: Custom Renderer over Graphviz

### Context
Initial attempts used Graphviz (via Viz.js) for layout.

### Problem
- Heavy WASM dependency.
- Rigid node placement (hard to customize specific family logic).
- Ugly default styling.
- Difficult to make responsive.

### Decision
Built a custom Vanilla JS + SVG renderer from scratch.
- **Pros:** Full control over every pixel, lightweight (no deps), custom collision logic.
- **Cons:** Must implement layout algorithms (DAG, routing) manually.

## 2026-02-24: Mobile First Strategy

### Context
User primarily views the site on iPhone.

### Decision
- **Viewport:** `viewport-fit=cover` meta tag.
- **Touch:** Custom gesture handling (pan/zoom/inertia) instead of browser defaults.
- **Layout:** Stacked panels on mobile, 3-column dashboard on desktop.
- **Dark Mode:** Default and only theme (OLED friendly).
