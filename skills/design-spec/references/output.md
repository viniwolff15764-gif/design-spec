# Output contract

The user should be able to point at a screenshot and connect it to an exact name.

## Human-readable report
Use the user's language; retain English technical names as search terms.

1. **Scope:** URL, time, routes, viewports, states, tools and blockers.
2. **Visual overview:** a short evidence-based description, separating established styles from subjective impressions.
3. **Numbered visual atlas:** annotated screenshots grouped by section; each has a nearby legend mapping E/M IDs to names. Show motion before/after frames together where possible.
4. **Complete inventory:** ID, location, element name, style/treatment, plain explanation, term classification, evidence status and image link. List meaningful variants and repeated locations.
5. **Specifications:** typography, palette, dimensions, spacing, corners, borders, shadows, imagery, compositing and responsive differences. Record units and sources. Use null/unknown rather than guessed exact values.
6. **Motion inventory:** ID, target, trigger, behavior, start/end state, measured timing/easing if available, loop/reverse behavior, reduced-motion observation and linked frames.
7. **Coverage and limits:** every inspected section/state plus blocked, unvisited or untestable portions. Include unsupported DOM/runtime inspection.
8. **Terminology references:** primary references for non-obvious or disputed classifications.

Do not compress the complete inventory into a "top 10." Keep the chat readable using section tables and expandable details if supported; if long, deliver the full report artifact and show the visual atlas plus key findings in chat. Never present an unlinked file path as if it were a visible image.

## Files
Use a fresh folder, following the host's output-directory rules:
```
design-spec-<host>-<timestamp>/
  report.md
  inventory.json
  evidence/
    S01-original.png
    S01-annotated.png
    S01-marks.json
    S02-original.png
    S02-annotated.png
    S02-marks.json
```
Original images may also be JPEG/WebP. Annotated PNGs avoid additional lossy compression. Paths in JSON and Markdown are relative to this folder, never private absolute paths. Keep credentials/query secrets out of filenames and reports. Do not publish private evidence.

Number visuals globally as E01… and motion as M01…. A repeated pattern can use the same ID with all relevant locations listed. A significantly different state or variant merits its own ID or a clear subentry.

## Annotation input
`scripts/annotate.py` expects:
```json
{
  "image_size": [1440, 1000],
  "marks": [
    {"id": "E01", "shape": "rect", "bbox": [480, 20, 480, 64]},
    {"id": "E02", "shape": "ellipse", "bbox": [680, 330, 80, 90]}
  ]
}
```
Coordinates are actual **image pixels**, not CSS pixels. Convert using the actual captured dimensions and crop/scroll offset. Do not assume devicePixelRatio alone describes a resized export. Reject mismatched dimensions; never silently rescale boxes. Mark representative instances and retain meaningful surrounding context. If the automatic label covers text, add optional `"label_xy": [x, y]` to position the ID tag in a clear area; the helper checks that it stays inside the image.

```sh
python3 scripts/annotate.py --image evidence/S01-original.png \
  --marks evidence/S01-marks.json --output evidence/S01-annotated.png
```

## Machine-readable inventory
Use this shape. Arrays can contain more entries; this is a compact illustration, not a completed report:
```json
{
  "version": "1.0",
  "url": "https://example.com",
  "inspected_at": "2026-11-10T12:00:00+00:00",
  "scope": "Supplied page, desktop and mobile",
  "annotation_status": "complete",
  "evidence": [
    {
      "id": "S01",
      "kind": "screenshot",
      "path": "evidence/S01-original.png",
      "annotated_path": "evidence/S01-annotated.png",
      "marks_path": "evidence/S01-marks.json",
      "viewport": "1440x1000 CSS px",
      "state": "Header after scrolling",
      "item_ids": ["E01"]
    }
  ],
  "items": [
    {
      "id": "E01",
      "category": "navigation",
      "name": "Sticky navigation",
      "name_local": "Navegação aderente",
      "location": "Header",
      "description": "Navigation remains at the top while scrolling.",
      "term_kind": "established",
      "status": "measured",
      "evidence": ["S01"],
      "specs": {
        "position": {
          "value": "sticky",
          "unit": null,
          "status": "measured",
          "source": "Computed style of header"
        }
      },
      "motion": null
    }
  ],
  "coverage": [
    {
      "route": "/",
      "section": "Header",
      "viewport": "desktop",
      "state": "scrolled",
      "status": "inspected",
      "evidence": ["S01"],
      "notes": "Position inspected in rendered DOM."
    }
  ],
  "limitations": ["Illustrative schema example, not an audit of example.com."],
  "sources": []
}
```

Categories: foundations, layout, navigation, component, typography, imagery, surface, data-visualization, motion, responsive, other.
Term kind: established, descriptive, uncertain.
Evidence status: measured, observed, inferred, unknown.
Evidence kinds: screenshot, recording, dom, css.
Coverage status: inspected, blocked, not-inspected, not-applicable.

For an M item use category motion and a non-null motion object with:
`trigger`, `behavior`, `properties` (array), `duration_ms` (number or null),
`duration_source` (string or null), `easing` (string or null),
`repeat` (string), `reduced_motion` (string).
Support it with at least two distinct screenshot paths or a recording.
A complete annotated audit links every E/M item to at least one annotated screenshot marking that exact ID; motion frames each mark the moving target. Recordings may supplement marked screenshots.

`sources` entries: `{"url": "...", "supports": "definition of …"}`.
Empty sources are acceptable for common unambiguous terms; specialized labels need actual consulted sources.
When annotation cannot be completed use partial/unavailable, describe why in limitations, and do not call the report complete.

The validator requires Pillow>=10.4 for image checks. It checks fields, IDs, links, marks, real image dimensions and distinct motion frames at matching viewports. It cannot certify terminology, screenshot authenticity, timing accuracy or coverage completeness. Inspect those yourself.
