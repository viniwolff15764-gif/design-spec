# Inspection and coverage

Use this as a coverage checklist, not a list of things to claim exist. Record absent/not applicable categories once; do not flood the inventory with imaginary items.

## Scope and collection
- Record requested and final URL, timestamp with timezone, page title, browser/tool, actual viewport, zoom/scale if known, access level, locale and theme.
- Map page sections and safe interactive controls before testing. Keep a ledger: route, section, viewport, state/trigger, status, evidence ID, reason.
- Map all distinct visible page templates when a whole-site audit is requested; inspect within the active time budget and list the unvisited templates. Use the navigation and sitemap when accessible; do not guess routes or crawl indefinitely.
- Capture each section during one scroll pass. Revisit only unresolved evidence. Sticky scenes can span several viewport heights and need intermediate positions.
- Record mobile composition changes, reordered content, hidden/replaced elements, touch controls and responsive typography. Do not claim a breakpoint from only two samples.
- When available, test a keyboard focus state and reduced-motion preference. Restore temporary emulation and theme changes. If unsupported, say so.
- "Not observed in inspected states" is different from "not present anywhere."

## Foundations
Palette and semantic color roles; light/dark surfaces; type families declared versus rendered; sizes, weights, line-height, tracking, alignment, text wrapping, variable font axes; content width, columns, gutters, spacing rhythm, alignment; density, negative space; responsive changes.

## Layout and navigation
Hero, split layout, asymmetric grid, bento grid, masonry, card list, editorial columns, dashboard shell, sidebar, rail, sticky header, floating navigation, tabs, breadcrumbs, pagination, menus/mega menus, drawers, bottom navigation, table of contents, scroll indicator and footer. Do not equate design composition with CSS Grid implementation.

## Components and states
Buttons (filled, outline, text, icon, pill); links; forms, inputs, labels, helper text, select, checkbox, radio, switch, slider; cards, lists, tables, badges, chips, avatars, tooltips, popovers, dialogs, banners, notifications, toasts, accordions, carousels, search/command palettes, media controls.
Inspect available default, hover, focus, active, selected, expanded, disabled, loading, success/error and empty states. Many states are not safely reachable; log those limits instead of simulating a transaction.

## Imagery, illustration and identity
Wordmark, symbol, mascot, pictogram, outline/filled icon, photography, cutout photography, collage, raster/vector illustration, abstract/geometric/flat/outline artwork, perspective/isometric drawing, device mockup, UI screenshot, simplified UI illustration, avatar, icon/logo grid, hero video, animated GIF, canvas/WebGL scene. A browser screenshot rarely proves how the original asset was made.

## Surface and compositing treatments
Border, hairline rule, divider, rounded corner, capsule, outline, inset highlight, drop/inner shadow, glow/bloom, linear/radial/conic/mesh gradient, opacity, backdrop blur versus foreground blur, frosted glass, texture/grain/noise, vignette, clipping, masks, blend modes, layering, perspective, reflections/refraction, color overlay, image crop and object-fit behavior. Separate observed appearance from verified implementation.

## Data visualization
Metric/KPI card, number formatting, unit and delta, line/area/column/bar chart, sparkline, pie/donut, radial gauge, progress ring/bar, calendar heatmap, histogram, scatter plot, treemap, Sankey/network/flow diagram, timeline, legend, axes, ticks, gridlines, annotations, tooltips, series markers, reference lines. Match the data encoding, not just the silhouette.

## Motion and interaction
Entrance/exit, scroll reveal, pinned narratives, parallax, scroll-linked transforms, hover/focus/press feedback, spring/bounce/elastic behavior, layout transition, shared element, morph, carousel, marquee, ticker, number count-up, typewriter, text reveal, stagger, spinner, skeleton/shimmer, pulse, scan line, path drawing, gradient motion, particles, cursor follower, camera motion, background video, animated SVG, Lottie/canvas/WebGL only if implementation evidence supports that name.

## Small details
Cursor shape; link underlines; selected-state marks; focus rings; one-pixel highlights; text gradients; text stroke; decorative rules; corner accents; image aspect ratios; oversize cropped graphics; badge dots; chart endpoints; decorative versus meaningful icons; contrast used to indicate depth.

## Completion pass
For every captured section ask: What has not yet received an inventory ID? Which apparent variants are actually the same pattern? Which naming claim needs verification? Is there an image marking the actual target?
List blocked routes, missing interactions, inaccessible frames/shadow roots, untested preferences and unsupported measurements. Never hide truncation or a tool-imposed limit.
