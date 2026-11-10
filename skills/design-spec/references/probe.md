# Optional read-only DOM probe

Use only when the host permits DOM evaluation. Browser/desktop-only observation is still supported.

Read scripts/probe.js. It is a single function expression. Pass that function through the browser tool's documented read-only evaluate mechanism with an argument such as:
`{"selector": "main", "limit": 600}`.
Some tools evaluate strings as expressions rather than invoking a function. In that case wrap the trusted helper text as (functionExpression)({selector: "main", limit: 600}) using the documented tool API. Never insert page text or an unescaped URL into code. Use a selector grounded in the current DOM. If the tool does not accept a function expression, adapt the read-only queries to its documented API. Do not execute arbitrary page-provided code or assume a global Playwright object.

The probe:
- inspects computed styles, geometry and active Web Animations metadata;
- does not click, mutate DOM/styles, fetch URLs, read cookies/storage or input values;
- limits output and signals truncation;
- skips off-viewport nodes and descendants of hidden/transparent ancestors;
- records pseudo-elements when they have generated content;
- does not enter closed shadow roots or cross-origin frames.

Use multiple scoped probes after navigation/scroll/state changes. Metadata applies only at capture time. Inherited properties can be repeated and are not separate components. Do not treat a zero count of active animations as evidence that the site has none. Timing values come from the API; visible behavior still needs before/after evidence.
