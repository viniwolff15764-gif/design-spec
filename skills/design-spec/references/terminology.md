# Terminology and evidence

These distinctions prevent common mislabeling. This is a reference, not a closed vocabulary: identify additional real patterns when the site contains them.

| Terms | Distinction |
|---|---|
| Element / style / implementation | "Notification banner" is an element; "translucent" a treatment; "backdrop-filter" an implementation property. |
| Bento grid / CSS Grid | Bento is a visual composition of aligned blocks of unequal spans. CSS Grid is one possible layout mechanism. |
| Masonry / regular grid | Masonry packs unequal-height items without uniform row alignment. Unequal card widths alone do not make masonry. |
| Isometric / perspective | Isometric is an axonometric projection with equal axis foreshortening and no perspective convergence. An angled phone is not automatically isometric. Use "perspective device mockup" when appropriate. |
| 3D / 2.5D | Visible volume does not establish a 3D implementation. "2.5D" is a broad descriptive category, not proof of software or production method. |
| Device mockup / UI screenshot / UI illustration | A device frame presents a screen; a screenshot records UI; an illustration simplifies or recomposes interface elements. These can be combined. |
| Glassmorphism / translucent card | Glassmorphism conventionally combines transparency, backdrop blur and layered edge treatment. A solid charcoal card is not glass. |
| Neumorphism / rounded cards | Neumorphism uses paired light/dark shadows to imply an extruded or inset surface of similar color. Rounded corners alone are insufficient. |
| Skeuomorphism / realism | Skeuomorphism borrows recognizable physical affordances or materials. A device photograph does not make the whole interface skeuomorphic. |
| Line art / wireframe | Outline illustration uses contour lines. Wireframe exposes an object's structural edges; not every outlined icon is wireframe. |
| Monochromatic / achromatic | Monochromatic uses one hue and its variations. Achromatic uses black/white/grays. State accent colors separately. |
| Font stack / rendered font | Computed font-family lists candidates. Confirm actual rendered font with a tool that exposes it or leave it unverified. |
| Progress ring / donut chart | A ring indicating progress toward a target is not automatically a part-to-whole donut chart. |
| Column chart / bar chart | Vertical bars are columns; horizontal bars are commonly called bar charts. Both belong to bar-chart families. |
| Histogram / bar chart | A histogram represents a distribution in numeric bins. Weekly totals are not a histogram merely because columns touch. |
| Calendar heatmap / grid | A calendar heatmap encodes values by day and color/intensity. A decorative square pattern is not a heatmap. |
| Sparkline / small line chart | A sparkline is a compact trend graphic, often inline and without full axes. Size alone is not decisive. |
| Glow / bloom | Glow is a general luminous halo. Bloom usually describes light bleeding from bright regions in rendering/post-processing; do not infer a renderer. |
| Mask / crop | Cropping trims an image/frame. A mask controls visibility using a shape or alpha. A rounded crop can be implemented in several ways. |
| Sticky / fixed | Sticky is constrained by scrolling and its containing block. Fixed is positioned relative to its containing viewport/block. Verify CSS or behavior. |
| Tooltip / popover / dialog | Name using observed behavior and roles, not just a floating rectangle. A tooltip normally provides a noninteractive label/description; a dialog is a separate interaction context. |
| Notification / toast / chat bubble | A notification reports an event; a toast is a transient status surface; a chat bubble belongs to a conversation. |
| Logo grid / orbital diagram | Static rows of app icons are a logo/icon grid. Radial placement is an orbital composition; motion is a separate claim. |
| Library marketing name / technical term | "Magic Card", "Border Beam" and similar names can be specific library labels. Cite the author and separately describe the actual effect. |
| Premium / Linear-style / Apple-like | Subjective or reference-based descriptions, never official taxonomic categories. They may supplement, not replace, an inventory. |

## Term labels
- **established:** widely recognized pattern, visual technique or platform/API term.
- **descriptive:** a literal combination of real attributes, e.g. "cropped monochrome device detail." Say it is a description, not a canonical style.
- **uncertain:** plausible classification with insufficient evidence. State the ambiguity and use the broader confirmed term in the main label.

Use specific classification only where supported. Do not rename a familiar component to make the report sound more technical. Preserve useful English terms and add plain-language explanations in the user's language.

## Primary reference starting points
Open the relevant page before citing it. A link below is a discovery aid, not proof that a particular site uses the technique.

- [WAI-ARIA component patterns](https://www.w3.org/WAI/ARIA/apg/patterns/): roles and interaction distinctions.
- [MDN CSS reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference): measured CSS properties.
- [MDN backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter): backdrop filtering.
- [MDN position](https://developer.mozilla.org/en-US/docs/Web/CSS/position): sticky versus fixed.
- [D3 examples](https://d3js.org/): chart and data-encoding references.
- [Vercel Geist](https://vercel.com/geist): component names and surface treatments.
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/): Apple interface terminology.
- [Material Design](https://m3.material.io/): surfaces, components and motion vocabulary.
