# Genealogy Rendering Rules (Source of Truth)

Updated: 2026-02-24
Scope: `/Users/oyloo/.openclaw/workspace/genealogy-site/`

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

## 7) Release gate
If any check fails, release is blocked until corrected.
