# Genealogy Rendering Rules (Source of Truth)

Updated: 2026-02-25
Scope: `/Users/oyloo/.openclaw/workspace/genealogy-site/`
Current Version: `20260225_0015` (multi-neighbor aware color allocation)

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

## 7) Family line coloring
- **Goal**: Intersecting/overlapping family lines should not share the same color.
- **Algorithm**: Multi-neighbor aware greedy coloring:
  1. Families sorted by horizontal position (parent center X).
  2. Each family assigned a color that is not used by left or right neighbor.
  3. Palette ordered for maximum perceptual contrast.
- **Current palette** (v0015): Orange → Bright Blue → Red → Green → Yellow → Purple → Turquoise → ...
- **Fallback**: If all neighbors use colors from palette (rare), use prime offset `(idx * 3) % length`.

## 8) Release gate
If any check fails, release is blocked until corrected.
