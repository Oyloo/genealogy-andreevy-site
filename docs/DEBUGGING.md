# Genealogy Site - Debugging Guide (Local)

## 🐛 Local Development & Testing

We **DO NOT use tunnels** (Cloudflare/localtunnel) for local debugging due to flaky connections and security blocks. We use **local Playwright**.

### 1. Start Local Server
```bash
cd /Users/oyloo/.openclaw/workspace/genealogy-site
python3 -m http.server 8089
```

### 2. Run Visual Layout Check (Playwright)
Use `scripts/check_layout.py` to verify mobile vs desktop layouts:
```bash
cd /Users/oyloo/.openclaw/workspace/genealogy-site
python3 scripts/check_layout.py
```
This generates:
- `verify-mobile-local.png` (iPhone dimensions)
- `verify-desktop-local.png` (Large screen dimensions)

Inspect these screenshots with the `image` tool to confirm layout correctness.

### 3. Common Issues

#### Mobile Layout
- **Issue:** Address bar covers bottom content or adds white gap.
- **Fix:** Ensure `viewport-fit=cover` meta tag is present.
- **Fix:** Avoid fixed-position footers (`bottom: 0`). Let content flow naturally.

#### Desktop Layout (Black Graph Bug)
- **Symptom:** Graph area is completely black/empty, but controls are visible.
- **Cause:** `.layout` container grows infinitely (e.g., `2800px+`) due to unconstrained grid/flex height, confusing the SVG renderer or causing layout thrashing.
- **Fix:** On desktop (`>1100px`), ensure `body` has fixed height (`100dvh`) and `overflow: hidden`, while `.layout` uses `flex: 1` and `minmax(0, 1fr)` to constrain the graph container.

#### Graph Rendering
- **Debug:** Check browser console logs for `drawGraph start` / `drawGraph finished OK`.
- **Force Redraw:** Resize window or toggle mobile emulation to trigger `resize` event.

## 🛠️ Tools
- **Playwright:** Installed in Python environment. Used for screenshot verification.
- **Python:** Simple HTTP server for static files.
- **Git:** Commit often (`git add . && git commit -m "fix: ..." && git push`).
