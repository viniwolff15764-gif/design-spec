# Performance measurements · 1.1.0

Measured on 2026-11-10. These are helper-level measurements, not a live Claude Code end-to-end benchmark.

| Measurement | Before | After | Scope |
|---|---:|---:|---|
| Entry instruction words | 1,349 | 1,128 | Whitespace word count, not model tokens |
| Compact probe output | 71,742 bytes | 10,982 bytes | 80 synthetic DOM nodes, 79 visible, repeated styles and generated pseudo-elements |
| Build annotations + Markdown | Not measured | 0.435 s | Six-item bundled example, three 1440×900 annotated outputs, one VPS run |

The old workflow additionally required early reads of inspection, output and motion references (3,392 words including its entrypoint). Version 1.1 loads references at the point of need; the output contract is still required to construct the inventory. This is not a claimed 67% total token reduction.

## Reproduce

```sh
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
node tests/probe_test.cjs
```

The Node fixture compares compact and expanded results property-for-property after dictionary expansion, and checks hidden nodes and truncation. It is a synthetic DOM adapter, not a browser integration test. Compression depends on style repetition and is smaller on highly varied pages.

To time the builder, copy `examples/sample-report` to a temporary folder, remove only its copied `report.md` and copied annotated PNGs, then time `python3 skills/design-spec/scripts/finish.py <copy>/inventory.json`. Preserve the copied originals and marks. Browser load, screenshots, model generation, and dependency installation are excluded.

## What changed

- One traversal per viewport, representative checks per variant, reuse of evidence.
- A 300-second default target with a 30% delivery reserve and explicit uncovered scope.
- Scoped probe default reduced from 600 to 80 nodes, with truncation still reported.
- Lossless style dictionary; one-invocation computed-style and ancestor-visibility caches.
- One JSON inventory drives annotation, validation and report generation.
- No default subagents, redundant source dumps, broad term searches or custom report UI.

## What is not established

There is no measured Claude Code speedup, dollar saving, or universal five-minute guarantee. An instruction skill cannot preempt a hanging tool call. A proper end-to-end comparison needs the same URL, model, browser tools, permissions and warm/cold conditions, with wall-clock time, billed tokens and evidence coverage compared. Names and measured claims retain the same evidence rules; coverage can be lower when the deadline is reached and must be disclosed.
