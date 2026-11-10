#!/usr/bin/env python3
"""Validate package metadata and local documentation links."""
from pathlib import Path
import re
import sys
import yaml

root=Path(__file__).resolve().parents[1]
skill=root/"skills/design-spec"
errors=[]
raw=(skill/"SKILL.md").read_text()
parts=raw.split("---",2)
if len(parts)!=3:
    errors.append("Missing skill frontmatter")
    meta={}
else:
    meta=yaml.safe_load(parts[1])
if meta.get("name")!=skill.name: errors.append("Skill name and folder differ")
if not isinstance(meta.get("description"),str) or not 1<=len(meta["description"])<=1024:
    errors.append("Invalid skill description")
if meta.get("compatibility") and len(meta["compatibility"])>500:
    errors.append("Compatibility too long")
allowed={"name","description","license","compatibility","metadata","allowed-tools"}
if set(meta)-allowed: errors.append("Non-standard frontmatter")
ui=yaml.safe_load((skill/"agents/openai.yaml").read_text())["interface"]
if "$design-spec" not in ui["default_prompt"]: errors.append("Missing Codex invocation")
if not 25<=len(ui["short_description"])<=64: errors.append("Invalid short description")
for p in root.rglob("*.md"):
    if ".git" in p.parts or "__pycache__" in p.parts: continue
    content=p.read_text()
    links=re.findall(r"\]\(([^)\s]+)(?:\s+[^)]*)?\)",content)
    if p.name.startswith("README"):
        links+=re.findall(r'(?:src|href)="([^"]+)"',content)
    for link in links:
        if link.startswith(("http:","https:","mailto:","#")): continue
        relative=link.split("#",1)[0]
        if relative and not (p.parent/relative).exists():
            errors.append(f"{p.relative_to(root)}: missing {relative}")
for p in skill.rglob("*"):
    if p.is_symlink(): errors.append(f"Unexpected symlink: {p}")
    if p.suffix==".py": compile(p.read_text(),str(p),"exec")
if errors:
    print("\n".join(errors));sys.exit(1)
print("PASS: metadata, local references and Python syntax.")
