#!/usr/bin/env python3
"""Build annotations and a Markdown report from one evidence inventory."""
import argparse
import json
from pathlib import Path
from urllib.parse import quote
from annotate import annotate
from validate_report import validate


def local(base, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('Expected a relative file path')
    path = (base / value).resolve()
    if not path.is_relative_to(base):
        raise ValueError('Paths must stay inside the report folder')
    return path


def cell(value):
    if value is None:
        return '—'
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\r', '').replace('\n', '<br>')


def link(value):
    return quote(value, safe='/.-_')


def render(data):
    labels = data.get('report_labels', {})
    def label(key, default):
        return cell(labels.get(key, default))
    lines = [f"# {label('title', 'Design Spec')}", '', cell(data['url']), '',
             cell(data['scope']), '', cell(data['inspected_at']), '',
             f"## {label('atlas', 'Visual atlas')}", '']
    items = {item['id']: item for item in data['items']}
    for e in data['evidence']:
        if e['kind'] != 'screenshot':
            continue
        path = e.get('annotated_path') or e['path']
        lines += [f"### {cell(e['id'])} · {cell(e.get('state', ''))}", '',
                  f"![{cell(e['id'])}]({link(path)})", '',
                  cell(e.get('viewport', '')), '']
        for ident in e.get('item_ids', []):
            item = items.get(ident)
            if item:
                lines.append(f"- **{cell(ident)} — {cell(item['name'])}**: {cell(item.get('name_local') or item['description'])}")
        lines.append('')
    lines += [f"## {label('inventory', 'Inventory and specifications')}", '']
    for item in data['items']:
        lines += [f"### {cell(item['id'])} · {cell(item['name'])}", '',
                  cell(item.get('name_local', '')), '', cell(item['description']), '',
                  f"{cell(item['location'])} · {cell(item['category'])} · {cell(item['term_kind'])} · {cell(item['status'])}", '',
                  ]
        for eid in item['evidence']:
            e = next(e for e in data['evidence'] if e['id'] == eid)
            lines.append(f"[{cell(eid)}]({link(e.get('annotated_path') or e['path'])})")
        if item.get('specs'):
            lines += ['', '| Spec | Value | Unit | Status | Source |', '|---|---|---|---|---|']
            for name, spec in item['specs'].items():
                lines.append('| ' + ' | '.join(cell(v) for v in [name, spec.get('value'), spec.get('unit'), spec.get('status'), spec.get('source')]) + ' |')
        if item.get('motion'):
            lines += ['', f"**{label('motion', 'Motion')}**", '']
            lines.extend(f"- {cell(k)}: {cell(v)}" for k, v in item['motion'].items())
        lines.append('')
    lines += [f"## {label('coverage', 'Coverage')}", '', '| Route | Section | Viewport | State | Status | Evidence | Notes |', '|---|---|---|---|---|---|---|']
    for row in data['coverage']:
        lines.append('| ' + ' | '.join(cell(row.get(k)) for k in ['route','section','viewport','state','status','evidence','notes']) + ' |')
    lines += ['', f"## {label('limits', 'Limits')}", '']
    lines.extend('- ' + cell(s) for s in data['limitations'])
    lines += ['', f"## {label('sources', 'Terminology sources')}", '']
    for source in data['sources']:
        url = source['url']
        if not url.startswith(('https://', 'http://')):
            raise ValueError('Source links must use HTTP or HTTPS')
        lines.append(f"- [{cell(source['supports'])}]({quote(url, safe=':/?=&%#.-_~')})")
    return '\n'.join(lines).strip() + '\n'


def finish(inventory, report='report.md'):
    inventory = Path(inventory).resolve()
    base = inventory.parent
    target = local(base, report)
    if target.exists() or target == inventory:
        raise ValueError('Report output already exists; choose a new --report name')
    data = json.loads(inventory.read_text(encoding='utf-8'))
    # Preflight every path before creating files. Do not overwrite supplied evidence.
    jobs = []
    destinations = set()
    for e in data['evidence']:
        for key in ['path', 'annotated_path', 'marks_path']:
            if e.get(key):
                local(base, e[key])
        if e['kind'] == 'screenshot' and e.get('annotated_path') and e.get('marks_path'):
            original, marks, output = [local(base, e[k]) for k in ['path','marks_path','annotated_path']]
            if output == original or output == marks or output == inventory or output == target or output in destinations:
                raise ValueError('Annotation output conflicts with another file')
            destinations.add(output)
            if not output.exists():
                jobs.append((original, marks, output))
    for job in jobs:
        annotate(*job)
    errors = validate(data, base)
    if errors:
        raise ValueError('\n'.join(errors))
    content = render(data)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as f:
        f.write(content)
    return {'report': str(target), 'items': len(data['items']), 'annotations_created': len(jobs), 'validation': 'passed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inventory')
    parser.add_argument('--report', default='report.md')
    args = parser.parse_args()
    try:
        result = finish(args.inventory, args.report)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.exit(2, f'Build failed: {exc}\n')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
