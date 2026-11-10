(options = {}) => {
  const root = document.querySelector(options.selector || "body");
  if (!root) return { error: "Selector did not match the current DOM" };
  const limit = Math.min(2000, Math.max(1, Number(options.limit) || 600));
  const properties = [
    "display", "position", "color", "backgroundColor", "backgroundImage",
    "fontFamily", "fontSize", "fontWeight", "fontStyle", "lineHeight",
    "letterSpacing", "textAlign", "borderRadius", "borderTop",
    "boxShadow", "opacity", "filter", "backdropFilter", "mixBlendMode",
    "transform", "perspective", "clipPath", "maskImage", "objectFit",
    "gap", "padding", "margin", "gridTemplateColumns", "cursor",
    "transitionProperty", "transitionDuration", "transitionTimingFunction",
    "animationName", "animationDuration", "animationTimingFunction",
    "animationIterationCount", "animationTimeline"
  ];
  const rect = (r) => ({
    x: r.x, y: r.y, width: r.width, height: r.height
  });
  const identity = (el) => ({
    tag: el.tagName.toLowerCase(), id: el.id || null,
    classes: Array.from(el.classList).slice(0, 8),
    role: el.getAttribute("role")
  });
  const viewportWidth = typeof innerWidth === "number" ? innerWidth : document.documentElement.clientWidth;
  const viewportHeight = typeof innerHeight === "number" ? innerHeight : document.documentElement.clientHeight;
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height || r.bottom <= 0 || r.right <= 0 ||
        r.top >= viewportHeight || r.left >= viewportWidth) return false;
    for (let p = el; p; p = p.parentElement) {
      const s = getComputedStyle(p);
      if (s.display === "none" || s.visibility === "hidden" ||
          s.visibility === "collapse" || Number(s.opacity) === 0) return false;
    }
    return true;
  };
  const serialTime = (v) => {
    if (typeof v === "number") return Number.isFinite(v) ? v : String(v);
    if (typeof v === "string" || v == null) return v ?? null;
    return { value: v.value ?? null, unit: v.unit ?? null };
  };
  const nodes = [];
  let scanned = 0, matched = 0, scanTruncated = false;
  const candidates = [root, ...root.querySelectorAll("*")];
  for (const el of candidates) {
    if (++scanned > 12000) { scanTruncated = true; break; }
    if (visible(el)) {
      matched++;
      if (nodes.length < limit) {
        const style = getComputedStyle(el);
        const pseudos = {};
        for (const pseudo of ["::before", "::after"]) {
          const ps = getComputedStyle(el, pseudo);
          if (ps.content !== "none" && ps.content !== "normal") {
            pseudos[pseudo] = Object.fromEntries(properties.map(p => [p, ps[p] || null]));
          }
        }
        nodes.push({ ...identity(el), rect: rect(el.getBoundingClientRect()),
          styles: Object.fromEntries(properties.map(p => [p, style[p] || null])),
          pseudos });
      }
    }
  }
  const animationList = root.getAnimations ? root.getAnimations({subtree: true}) : [];
  const animations = animationList.slice(0, 100).map(a => {
    const timing = a.effect?.getComputedTiming?.() || {};
    const target = a.effect?.target;
    return {
      target: target?.tagName ? identity(target) : null,
      state: a.playState,
      currentTime: serialTime(a.currentTime),
      duration: serialTime(timing.duration),
      delay: serialTime(timing.delay),
      iterations: serialTime(timing.iterations),
      easing: timing.easing || null,
      direction: timing.direction || null,
      timeline: a.timeline?.constructor?.name || null,
      properties: Array.from(new Set((a.effect?.getKeyframes?.() || [])
        .flatMap(f => Object.keys(f))
        .filter(k => !["offset","computedOffset","easing","composite"].includes(k))))
    };
  });
  return {
    viewport: {width: viewportWidth, height: viewportHeight,
      dpr: typeof devicePixelRatio === "number" ? devicePixelRatio : null,
      scrollX: typeof scrollX === "number" ? scrollX : null,
      scrollY: typeof scrollY === "number" ? scrollY : null},
    capturedAt: new Date().toISOString(), scanned, matched,
    truncated: scanTruncated || matched > limit,
    animationTruncated: animationList.length > 100,
    limits: ["Current viewport/state only", "No closed shadow roots or frame traversal",
      "Active Web Animations only; JS loops, video and canvas may be missed",
      "fontFamily is declared, not a rendered-font confirmation"],
    nodes, animations
  };
}
