#!/usr/bin/env python3
"""Install Design Spec without a package manager or changing agent settings."""
import argparse
import filecmp
from pathlib import Path
import shutil
import tempfile

SOURCE = Path(__file__).resolve().parent / "skills" / "design-spec"

def same_tree(a, b):
    if b.is_symlink() or not b.is_dir(): return False
    def included(p): return p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    left = {p.relative_to(a) for p in a.rglob("*") if included(p)}
    right = {p.relative_to(b) for p in b.rglob("*") if included(p)}
    return left == right and all(filecmp.cmp(a/p,b/p,shallow=False) for p in left)

def destinations(agent, project=None, target=None):
    if target:
        if agent != "generic": raise ValueError("--target requires --agent generic")
        if project: raise ValueError("--target and --project cannot be combined")
        return [Path(target).expanduser().absolute()]
    if agent == "generic": raise ValueError("Generic installation needs --target PATH/design-spec")
    base = Path(project).expanduser().absolute() if project else Path.home()
    paths = []
    if agent in ("all","claude-code"): paths.append(base/".claude/skills/design-spec")
    if agent in ("all","codex"): paths.append(base/".agents/skills/design-spec")
    return paths

def install(paths, dry_run=False):
    if not (SOURCE/"SKILL.md").is_file(): raise ValueError("Skill package is missing")
    if any(p.is_symlink() for p in SOURCE.rglob("*")):
        raise ValueError("Refusing a skill package containing symlinks")
    plan = []
    for dest in paths:
        if dest.is_symlink(): raise ValueError(f"Refusing existing symlink: {dest}")
        if dest.exists():
            if same_tree(SOURCE,dest): plan.append((dest,"already installed")); continue
            raise ValueError(f"Existing content differs; left untouched: {dest}")
        for parent in dest.parents:
            if parent.is_symlink():
                raise ValueError(f"Refusing symlinked destination parent: {parent}")
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Destination parent is not a directory: {parent}")
        plan.append((dest,"install"))
    for dest,action in plan:
        if action != "install" or dry_run:
            print(f"{'DRY RUN ' if dry_run else ''}{action}: {dest}"); continue
        dest.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".design-spec-",dir=dest.parent) as temp:
            staged = Path(temp)/"design-spec"
            shutil.copytree(SOURCE,staged,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
            if dest.exists() or dest.is_symlink():
                raise ValueError(f"Destination appeared during install: {dest}")
            staged.rename(dest)
        print(f"Installed: {dest}")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent",choices=["all","claude-code","codex","generic"],default="all")
    parser.add_argument("--project",help="Install into this project instead of the home folder")
    parser.add_argument("--target",help="Exact skill directory for another compatible agent")
    parser.add_argument("--dry-run",action="store_true")
    args=parser.parse_args()
    try: install(destinations(args.agent,args.project,args.target),args.dry_run)
    except (ValueError,OSError) as exc: parser.exit(2,f"Install stopped: {exc}\n")
    print("Claude Code: /design-spec URL | Codex: $design-spec URL")
    print("Other agents: load SKILL.md using their native skill/prompt mechanism.")

if __name__=="__main__": main()
