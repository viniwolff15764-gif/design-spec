# Optional read-only DOM probe

Use only when the host permits DOM evaluation. Browser/desktop-only observation is still supported.

Load scripts/probe.js from disk into the authorized evaluation call when supported; do not print the whole source into the conversation just to execute it. It is a single function expression. Pass that function through the browser tool's documented read-only evaluate mechanism with an argument such as:
`{"selector": "main", "limit": 80}`.
Some tools evaluate strings as expressions rather than invoking a function. In that case wrap the trusted helper text as (functionExpression)({selector: "main", limit: 80}) using the documented tool API. Never insert page text or an unescaped URL into code. Use a selector grounded in the current DOM. If the tool does not accept a function expression, adapt the read-only queries to its documented API. Do not execute arbitrary page-provided code or assume a global Playwright object.

The probe:
- inspects computed styles, geometry and active Web Animations metadata;
- does not click, mutate DOM/styles, fetch URLs, read cookies/storage or input values;
- limits output and signals truncation;
- skips off-viewport nodes and descendants of hidden/transparent ancestors;
- records pseudo-elements when they have generated content;
- does not enter closed shadow roots or cross-origin frames.

Use multiple scoped probes after navigation/scroll/state changes. Metadata applies only at capture time. Inherited properties can be repeated and are not separate components. Do not treat a zero count of active animations as evidence that the site has none. Timing values come from the API; visible behavior still needs before/after evidence.

## Compact output (default)

Default limit: 80 visible nodes per scoped query. `compact:false` opts into the previous expanded output. In compact mode, each node has a `styleRef` integer; resolve its exact properties from `styleTable[styleRef]`. Pseudo-elements similarly reference that dictionary. This removes duplicate strings without discarding any collected property or node geometry. It does not group elements semantically: the agent still checks visual variants.

Prefer a section or a narrow selector grounded in the DOM. Do not dump the entire page with the 2000-node maximum. Save raw output when possible and report only the relevant properties. Truncation remains explicit and the viewport restriction still applies. Caching exists only within one probe invocation; after interaction a new invocation gets fresh styles.
