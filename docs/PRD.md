# Genealogy Site - Product Requirements Document (PRD)

## 🎯 Goal
Create a **fast, immersive, mobile-first genealogy visualizer** for the family tree.
- **Experience:** Feel like a native app on iOS/Android.
- **Data Source:** Raw GEDCOM data (processed into JSON).
- **Renderer:** Custom SVG engine (no heavy external libraries like Graphviz/D3-dag).
- **Aesthetic:** Dark mode only (OLED-friendly), minimal chrome, full-screen.

## 👤 Audience
- **Primary:** Family members (Ed, Tanya, parents, kids).
- **Secondary:** Extended family (sharing link).
- **Devices:** 80% Mobile (iPhone/Safari), 20% Desktop (Chrome/Arc).

## ✨ Key Features

### 1. Visualization
- **Strict Layout:** Parents above children. Generations aligned horizontally.
- **Family Grouping:** Color-coded connection lines for different nuclear families.
- **Collision Avoidance:** Lines must not cross cards (nodes).
- **Spouse Alignment:** Partners placed next to each other.
- **Marriage Indicators:** Distinct "marriage dots" (hubs) with direct vertical descent lines.

### 2. Mobile Experience (Critical)
- **Viewport:** `viewport-fit=cover` to use full screen (including notch area).
- **Gestures:**
  - 1-finger pan (native feel).
  - 2-finger pinch zoom.
  - Double-tap to smart zoom/center.
  - Kinetic scrolling (inertia).
- **Address Bar:** Content must flow naturally under the address bar (no fixed footers blocking view).

### 3. Desktop Experience
- **Layout:** 3-column dashboard (List | Graph | Details).
- **Interactivity:** Mouse drag/zoom, scroll wheel support.
- **Responsiveness:** Adapts to window resize without reload.

### 4. Data & Privacy
- **Source:** `data.json` (static export from GEDCOM parser).
- **Security:** No backend database. Client-side rendering only.
- **Search:** Instant fuzzy search by name/surname.

## 🚫 Non-Goals
- Editing data (read-only visualization).
- Social features (comments, likes).
- Light mode (dark only).
