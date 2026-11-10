# Motion inspection

A still image proves appearance, not movement.

## Capture protocol
For each distinct effect record:
1. Target and location.
2. Trigger: page entry, elapsed time, hover, focus, click, scroll entry, continuous scroll, swipe, drag, state change.
3. Before, intermediate if needed, and after frames at the same viewport/zoom. Use the same ID on the target in each frame. An inspected recording can replace the pair.
4. Visible property changes: opacity, position, scale, rotation, shape, color, blur, clipping, content, number or camera.
5. Direction, sequence/stagger, repeat/reverse behavior and whether it persists after the trigger.
6. Duration, delay, easing and iteration only when measured. Distinguish declared CSS values from effective playback. If timing is visual estimation, mark it estimated and do not turn it into an exact specification.
7. Reduced-motion behavior if tested; otherwise "not tested." Restore settings.

Watch a normal-speed pass before using frame stepping or slow playback. Repeat a trigger once when distinguishing a reversible state from a one-time entrance. Do not wait indefinitely for an effect that may not exist.

## Frequently confused names
- **Scroll-triggered:** entering a region starts a time-based animation.
- **Scroll-linked / scroll-driven:** progress follows scroll position. A sticky scene is not sufficient proof.
- **Scrollytelling:** a narrative composition controlled/revealed through scrolling; an experience pattern, not a CSS property.
- **Parallax:** layers move at different relative rates with scrolling or pointer movement. A single translate-on-scroll is insufficient.
- **Fade:** opacity change. Blur is not a fade.
- **Stagger:** otherwise related elements begin at different offsets.
- **Morph:** shape changes continuously. A crossfade between two images is not morphing.
- **Shared-element transition:** a persistent visual element transitions between layouts/states. Observed continuity does not prove a particular framework.
- **Spring animation:** physical-model or spring-like behavior; report the latter as observed unless a spring configuration is inspected. Do not invent stiffness/damping.
- **Skeleton:** content-shaped loading placeholders. **Shimmer:** a moving highlight that may be applied to a skeleton.
- **Marquee:** continuous content travel. **Carousel:** a sequence of slides/items navigated or advanced in steps.
- **Typewriter:** progressive character appearance. Whole-word clipping can be a text reveal instead.
- **SVG stroke reveal:** path appears progressively. Confirm stroke properties before naming stroke-dasharray as its implementation.
- **Count-up:** numeric display increments toward a value; it may also count down.
- **Video/GIF animation:** prerecorded media. Do not identify it as a CSS animation merely because it moves inside a card.

## Runtime limits
getAnimations() reveals active CSS/Web Animations effects but misses many JS frame loops, canvas/WebGL renderers, embedded video, inactive transitions and animations in inaccessible trees. An empty result does not prove absence of motion.
getComputedTiming() values may include Infinity or percentage-based timeline values. Serialize explicit unknowns, never convert a non-finite value into a fabricated number.
Cross-origin CSS, closed shadow roots and iframes may be inaccessible. Record those limits.
Do not change animation styles, force reduced motion or inject transitions for the evidence capture.

## Primary references
- [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API)
- [Element.getAnimations](https://developer.mozilla.org/en-US/docs/Web/API/Element/getAnimations)
- [CSS animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline)
- [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
