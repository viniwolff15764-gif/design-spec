#!/usr/bin/env python3
"""Draw evidence IDs on a copy of a screenshot; never change the original."""
import argparse
import json
import re
from pathlib import Path

def annotate(image_path, marks_path, output_path):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise ValueError("Pillow is required: python3 -m pip install Pillow")
    image_path, marks_path, output_path = map(Path, (image_path, marks_path, output_path))
    if output_path.suffix.lower() != ".png":
        raise ValueError("Annotated output must be a .png file")
    if output_path.resolve() == image_path.resolve() or output_path.exists():
        raise ValueError("Output must be a new path, separate from the original")
    data = json.loads(marks_path.read_text(encoding="utf-8"))
    with Image.open(image_path) as original:
        original.load()
        size = list(original.size)
        image = original.convert("RGB")
    if data.get("image_size") != size:
        raise ValueError(f"Coordinate/image size mismatch: expected {size}")
    marks = data.get("marks")
    if not isinstance(marks, list) or not marks:
        raise ValueError("marks must be a nonempty list")
    ids = set()
    parsed = []
    for mark in marks:
        ident = mark.get("id", "")
        if not re.fullmatch(r"[EM][0-9]{2,}", ident) or ident in ids:
            raise ValueError(f"Invalid or repeated ID: {ident}")
        ids.add(ident)
        if mark.get("shape") not in ("rect", "ellipse"):
            raise ValueError("shape must be rect or ellipse")
        box = mark.get("bbox")
        if not isinstance(box, list) or len(box) != 4 or any(
            type(v) not in (int, float) for v in box
        ):
            raise ValueError(f"{ident}: bbox must be [x, y, width, height]")
        x, y, w, h = box
        if not (0 <= x < size[0] and 0 <= y < size[1] and
                2 <= w <= size[0] - x and 2 <= h <= size[1] - y):
            raise ValueError(f"{ident}: box is outside the image or too small")
        parsed.append((mark, (x, y, x + w - 1, y + h - 1)))
    draw = ImageDraw.Draw(image)
    scale = max(1, min(size) / 800)
    stroke = max(2, round(3 * scale))
    font_size = max(16, round(19 * scale))
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except OSError:
        font = ImageFont.load_default(size=font_size)
    for mark, box in parsed:
        color = "#5eead4" if mark["id"].startswith("E") else "#fbbf24"
        method = draw.rectangle if mark["shape"] == "rect" else draw.ellipse
        method(box, outline="#111827", width=stroke + 3)
        method(box, outline=color, width=stroke)
        label = mark["id"]
        bounds = draw.textbbox((0, 0), label, font=font)
        pad = max(5, round(6 * scale))
        tw, th = bounds[2] - bounds[0] + 2*pad, bounds[3] - bounds[1] + 2*pad
        lx = max(0, min(round(box[0]), size[0] - tw))
        ly = max(0, round(box[1] - th - 3))
        if ly + th > size[1]: ly = max(0, size[1] - th)
        if "label_xy" in mark:
            pos = mark["label_xy"]
            if not isinstance(pos,list) or len(pos)!=2 or any(type(n) not in (int,float) for n in pos):
                raise ValueError(f"{label}: label_xy must be [x, y]")
            lx,ly = pos
            if not (0 <= lx <= size[0]-tw and 0 <= ly <= size[1]-th):
                raise ValueError(f"{label}: label is outside the image")
        draw.rounded_rectangle((lx, ly, lx + tw, ly + th), radius=5, fill=color,
                               outline="#111827", width=1)
        draw.text((lx + pad - bounds[0], ly + pad - bounds[1]),
                  label, font=font, fill="#101820")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, "PNG")
    return {"output": str(output_path), "size": size, "marks": len(parsed)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, help="Original screenshot")
    parser.add_argument("--marks", required=True, help="JSON with image_size and marks")
    parser.add_argument("--output", required=True, help="New annotated .png path")
    args = parser.parse_args()
    try:
        result = annotate(args.image, args.marks, args.output)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f"Annotation failed: {exc}\n")
    print(json.dumps(result))

if __name__ == "__main__":
    main()
