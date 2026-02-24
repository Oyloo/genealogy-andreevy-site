# Genealogy Rendering Rules (Source of Truth)

Updated: 2026-02-25
Scope: `/Users/oyloo/.openclaw/workspace/genealogy-site/`
Current Version: `20260225_0035` (intersection-aware coloring + thick lines + no-pink-blue palette)

## 1) Semantics first
- Visual routing must never change genealogical meaning.
- Parent-child meaning is strict: `parent -> family hub -> child`.
- No visual pattern may imply that siblings are parents of each other.

## 2) Generation direction
- Parents are one generation above children.
- Child links must visually originate from family routing, not sibling cards.
- Entry/exit points from person cards must use nearest valid side and never run through card body.

## 3) Collision and overlap rules
- Lines must not pass through person cards.
- Horizontal bars must not cut through person cards.
- Vertical segments must not cut through person cards.
- Route around occupied lanes and existing routed segments.

## 4) Crossing policy
- Avoid line-line crossings whenever possible.
- Allowed junctions are only deliberate family routing joins.
- Random X-crossings that introduce ambiguity are forbidden.

## 5) Layering policy
- Cards stay visually readable.
- Edge layering is allowed only if semantics remain unambiguous and no card-cuts occur.

## 6) Required pre-release checks
- Automated: zero line-card intersections.
- Automated: no forbidden line-line crossings.
- Automated: every child path resolves through a family hub.
- Manual: inspect known sensitive cluster around Minadora and siblings.

## 7) Family line coloring (v0035)
- **Goal**: Intersecting/overlapping family lines must be distinguishable. Lines must not blend with node colors.
- **Algorithm**: Intersection-aware graph coloring:
  1. Calculate Y-range for each family (parent level to deepest child).
  2. Build conflict graph: families with overlapping Y-ranges are "conflicting" (potential line crossing).
  3. Greedy coloring: assign colors ensuring no two conflicting families share a color.
  4. Families sorted by X position for deterministic ordering.
  
- **Palette exclusions**: Removed all colors similar to node colors:
  - **Excluded**: Light pink (#f8b4d8, female nodes), light blue (#9cc8ff, male nodes)
  - **Included**: Dark greens, reds, purples, teals (Tailwind palette)
  - **Result**: Lines visually distinct from both male and female nodes
  
- **Line styling**:
  - Stroke width: 2.5px (increased from 1.8 for visibility)
  - Linecap/linejoin: round
  - Opacity: opaque

## 8) Release gate
If any check fails, release is blocked until corrected.
