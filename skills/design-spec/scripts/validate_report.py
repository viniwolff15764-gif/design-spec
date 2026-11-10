#!/usr/bin/env python3
"""Check a Design Spec inventory's structure and evidence links, not visual truth."""
import argparse
import hashlib
from datetime import datetime
import json
import math
from pathlib import Path
import re

CATEGORIES = {"foundations","layout","navigation","component","typography","imagery",
              "surface","data-visualization","motion","responsive","other"}
STATUSES = {"measured","observed","inferred","unknown"}

def validate(data, base):
    errors = []
    def fail(message): errors.append(message)
    def text(value): return isinstance(value, str) and bool(value.strip())
    def local_file(value, label):
        if not text(value):
            fail(f"{label}: missing relative path"); return None
        p = Path(value)
        if p.is_absolute() or ".." in p.parts:
            fail(f"{label}: path must stay inside the report folder"); return None
        resolved = (base / p).resolve()
        if not resolved.is_relative_to(base.resolve()) or not resolved.is_file():
            fail(f"{label}: missing or external file {value}"); return None
        return resolved
    if not isinstance(data, dict): return ["Inventory must be an object"]
    if data.get("version") != "1.0": fail("version must be 1.0")
    for key in ("url","inspected_at","scope"):
        if not text(data.get(key)): fail(f"{key}: required nonempty string")
    try:
        when = datetime.fromisoformat(data.get("inspected_at","").replace("Z","+00:00"))
        if when.tzinfo is None: fail("inspected_at must include a timezone")
    except (ValueError, TypeError, AttributeError): fail("Invalid inspected_at")
    complete = data.get("annotation_status") == "complete"
    if data.get("annotation_status") not in {"complete","partial","unavailable"}:
        fail("Invalid annotation_status")
    for key in ("evidence","items","coverage","limitations","sources"):
        if not isinstance(data.get(key), list): fail(f"{key} must be a list")
    if errors: return errors
    if not complete and not data["limitations"]:
        fail("Incomplete annotations require a limitation")
    if not data["coverage"]: fail("Coverage ledger is empty")
    if not data["items"] and complete: fail("A complete inventory cannot be empty")
    evidence = {}
    marks_by_evidence = {}
    image_sizes = {}
    image_hashes = {}
    for ev in data["evidence"]:
        if not isinstance(ev, dict):
            fail("Evidence entry must be an object"); continue
        eid = ev.get("id")
        if not text(eid) or eid in evidence:
            fail(f"Missing/repeated evidence ID: {eid}"); continue
        evidence[eid] = ev
        if ev.get("kind") not in {"screenshot","recording","dom","css"}:
            fail(f"{eid}: invalid evidence kind")
        original_path = local_file(ev.get("path"), eid)
        if not text(ev.get("state")): fail(f"{eid}: state is required")
        if ev.get("kind") == "screenshot":
            if not text(ev.get("viewport")): fail(f"{eid}: viewport is required")
            if original_path:
                try:
                    from PIL import Image
                    with Image.open(original_path) as image:
                        image.load()
                        image_sizes[eid] = list(image.size)
                    image_hashes[eid] = hashlib.sha256(original_path.read_bytes()).hexdigest()
                except ImportError:
                    fail("Pillow>=10.4 is required to validate screenshot files")
                except (OSError, ValueError):
                    fail(f"{eid}: original is not a valid image")
            item_ids = ev.get("item_ids", [])
            if not isinstance(item_ids,list) or any(not text(i) for i in item_ids):
                fail(f"{eid}: invalid item_ids"); item_ids = []
            if ev.get("annotated_path"):
                annotated_path = local_file(ev["annotated_path"], eid+" annotated")
                if annotated_path and original_path:
                    if annotated_path == original_path:
                        fail(f"{eid}: original and annotated paths must differ")
                    try:
                        from PIL import Image
                        with Image.open(annotated_path) as image:
                            image.load()
                            if list(image.size) != image_sizes.get(eid):
                                fail(f"{eid}: annotated dimensions differ from original")
                    except ImportError:
                        fail("Pillow>=10.4 is required to validate screenshot files")
                    except (OSError, ValueError):
                        fail(f"{eid}: annotated file is not a valid image")
                mp = local_file(ev.get("marks_path"), eid+" marks")
                if mp:
                    try:
                        marks_data = json.loads(mp.read_text())
                        marks = marks_data["marks"]
                        marked = [m["id"] for m in marks]
                        if set(marked) != set(item_ids):
                            fail(f"{eid}: item_ids differ from annotation marks")
                        if len(marked) != len(set(marked)):
                            fail(f"{eid}: repeated annotation IDs")
                        size = marks_data["image_size"]
                        if size != image_sizes.get(eid):
                            fail(f"{eid}: marks dimensions differ from original")
                        if (not isinstance(size,list) or len(size)!=2 or
                            any(type(n) is not int or n <= 0 for n in size)):
                            raise ValueError("invalid image_size")
                        for m in marks:
                            if m.get("shape") not in {"rect","ellipse"}:
                                raise ValueError("invalid mark shape")
                            x,y,w,h = m["bbox"]
                            if any(type(n) not in (int,float) or not math.isfinite(n)
                                   for n in [x,y,w,h]):
                                raise ValueError("non-numeric bbox")
                            if not (0<=x<size[0] and 0<=y<size[1] and
                                    2<=w<=size[0]-x and 2<=h<=size[1]-y):
                                raise ValueError("bbox outside image")
                        marks_by_evidence[eid] = set(marked)
                    except (ValueError, KeyError, TypeError) as exc:
                        fail(f"{eid}: malformed marks ({exc})")
    item_ids = set()
    for item in data["items"]:
        if not isinstance(item,dict):
            fail("Item must be an object"); continue
        ident = item.get("id","")
        if not isinstance(ident,str) or not re.fullmatch(r"[EM][0-9]{2,}",ident):
            fail("Invalid item ID"); continue
        if ident in item_ids: fail(f"Duplicate item ID: {ident}")
        item_ids.add(ident)
        for key in ("name","location","description"):
            if not text(item.get(key)): fail(f"{ident}: {key} is required")
        if item.get("category") not in CATEGORIES: fail(f"{ident}: invalid category")
        if item.get("term_kind") not in {"established","descriptive","uncertain"}:
            fail(f"{ident}: invalid term_kind")
        if item.get("status") not in STATUSES: fail(f"{ident}: invalid status")
        refs = item.get("evidence",[])
        if not isinstance(refs,list) or not refs or any(not text(r) for r in refs):
            fail(f"{ident}: evidence IDs required"); refs = []
        for ref in refs:
            if ref not in evidence: fail(f"{ident}: missing evidence {ref}")
        visual = [evidence[r] for r in refs if r in evidence and
                  evidence[r].get("kind") in {"screenshot","recording"}]
        if not visual: fail(f"{ident}: no visual evidence")
        marked_refs = [r for r in refs if ident in marks_by_evidence.get(r,set())]
        if complete and not marked_refs:
            fail(f"{ident}: no screenshot marks this item")
        specs = item.get("specs",{})
        if not isinstance(specs,dict):
            fail(f"{ident}: specs must be an object"); specs = {}
        for key,spec in specs.items():
            if not isinstance(spec,dict):
                fail(f"{ident}/{key}: spec must be an object"); continue
            if spec.get("status") not in STATUSES: fail(f"{ident}/{key}: invalid status")
            if spec.get("value") is not None and not text(spec.get("source")):
                fail(f"{ident}/{key}: non-null value requires source")
            if spec.get("status")=="unknown" and spec.get("value") is not None:
                fail(f"{ident}/{key}: unknown value must be null")
        if ident.startswith("M"):
            motion = item.get("motion")
            if item.get("category") != "motion": fail(f"{ident}: M IDs require motion category")
            if not isinstance(motion,dict):
                fail(f"{ident}: motion details required"); continue
            for key in ("trigger","behavior","repeat","reduced_motion"):
                if not text(motion.get(key)): fail(f"{ident}: motion.{key} required")
            if not isinstance(motion.get("properties"),list) or not motion["properties"]:
                fail(f"{ident}: changed properties required")
            duration = motion.get("duration_ms")
            if duration is not None and (type(duration) not in (int,float) or
                                         not math.isfinite(duration) or duration<0):
                fail(f"{ident}: invalid duration_ms")
            if duration is not None and not text(motion.get("duration_source")):
                fail(f"{ident}: measured duration needs duration_source")
            stills = {str((base/e["path"]).resolve()) for e in visual
                      if e.get("kind")=="screenshot"}
            recordings = [e for e in visual if e.get("kind")=="recording"]
            frames = [e for e in visual if e.get("kind")=="screenshot"]
            if len(frames) >= 2:
                if len({e.get("viewport") for e in frames}) != 1:
                    fail(f"{ident}: motion frames must share the same viewport")
                sizes = {tuple(image_sizes.get(e["id"],[])) for e in frames}
                if len(sizes) != 1:
                    fail(f"{ident}: motion frames must share image dimensions")
                hashes = {image_hashes.get(e["id"]) for e in frames} - {None}
                if len(hashes) < 2 and not recordings:
                    fail(f"{ident}: identical frame files do not demonstrate motion")
            if len(stills)<2 and not recordings:
                fail(f"{ident}: motion needs two distinct frames or a recording")
            if complete and not recordings and len(set(marked_refs))<2:
                fail(f"{ident}: mark the target in both motion frames")
        elif item.get("category")=="motion":
            fail(f"{ident}: motion category requires an M ID")
    for eid, ev in evidence.items():
        for ident in ev.get("item_ids",[]) if isinstance(ev.get("item_ids",[]),list) else []:
            if ident not in item_ids: fail(f"{eid}: unknown annotated item {ident}")
    for row in data["coverage"]:
        if not isinstance(row,dict):
            fail("Coverage row must be an object"); continue
        for key in ("route","section","viewport","state"):
            if not text(row.get(key)): fail(f"Coverage: {key} required")
        if row.get("status") not in {"inspected","blocked","not-inspected","not-applicable"}:
            fail("Coverage: invalid status")
        refs = row.get("evidence",[])
        if not isinstance(refs,list) or any(not text(r) for r in refs):
            fail("Coverage: invalid evidence"); refs = []
        if row.get("status")=="inspected" and not refs:
            fail("Inspected coverage needs evidence")
        for ref in refs:
            if ref not in evidence: fail(f"Coverage: missing evidence {ref}")
        if row.get("status")!="inspected" and not text(row.get("notes")):
            fail("Uninspected coverage needs an explanation")
    for source in data["sources"]:
        if not isinstance(source,dict) or not text(source.get("url")) or not text(source.get("supports")):
            fail("Sources need url and supports")
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.inventory.read_text()), args.inventory.parent)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Cannot read inventory: {exc}\n")
    if errors:
        parser.exit(1, "\n".join(f"- {error}" for error in errors)+"\n")
    print("PASS: inventory structure, evidence links and annotation references are consistent.")
    print("Visual truth, naming accuracy and coverage still require human/agent review.")

if __name__=="__main__":
    main()
