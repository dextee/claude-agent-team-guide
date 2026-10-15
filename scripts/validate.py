#!/usr/bin/env python3
"""Static checks for the Claude Code Agent Team Guide.

Checks internal links and heading anchors, image references and files,
agent frontmatter, README/agent agreement, published rates and cost
arithmetic, counted artifacts, leftover markers, hype words, credential
patterns and email addresses. Read-only; never calls a model or the network.

Usage:
    python3 scripts/validate.py                  # strict (use before publishing)
    python3 scripts/validate.py --allow-missing-images
"""
from __future__ import annotations

import json
import re
import struct
import sys
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

AGENT_NAMES = ['architect', 'implementer', 'worker', 'explorer',
               'reviewer', 'auditor', 'researcher', 'editor']
MODELS = {
    'claude-fable-5-1': 'Fable 5.1',
    'claude-opus-5-5': 'Opus 5.5',
    'claude-sonnet-5-5': 'Sonnet 5.5',
    'claude-haiku-5-5': 'Haiku 5.5',
}
EFFORTS = {'low', 'medium', 'high', 'xhigh', 'max'}
KNOWN_TOOLS = {'Read', 'Edit', 'Write', 'Glob', 'Grep', 'Bash', 'WebFetch', 'WebSearch',
               'Agent', 'NotebookEdit', 'TodoWrite'}
REQUIRED_IMAGES = [
    'assets/images/hero.png', 'assets/images/model-team.png', 'assets/images/orchestration.png',
    'assets/images/workflow-coding.png', 'assets/images/workflow-research.png',
    'assets/images/workflow-review.png', 'assets/images/workflow-docs.png',
    'assets/images/workflow-ops.png',
]
SOCIAL_PREVIEW = 'assets/social-preview.png'
EXPECTED_TASKS = 24
EXPECTED_RECIPES = 12
ALLOWED_EMAILS = {'dextee@users.noreply.github.com', 'noreply@anthropic.com'}
# Built from parts so this file does not trip its own marker check.
MARKERS = ['TO' + 'DO', 'FIX' + 'ME', 'TB' + 'D', 'XX' + 'X', 'lorem ' + 'ipsum']
HYPE = ['revolutionary', 'game-changing', 'game changer', 'supercharge', 'unleash',
        'cutting-edge', 'blazing', 'seamless', 'next-level', 'mind-blowing', '10x']
TEXT_SUFFIXES = {'.md', '.py', '.json', '.yml', '.yaml', '.sh', '.cff', '.csv', '.txt'}


# ---------- helpers ----------

def strip_fences(text: str) -> str:
    return re.sub(r'^(```|~~~).*?^\1[^\n]*$', '', text, flags=re.S | re.M)


def slugify(title: str) -> str:
    title = re.sub(r'[`*_]|<[^>]+>', '', title).strip().lower()
    title = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', title)
    return re.sub(r'[^\w\- ]', '', title).replace(' ', '-')


def headings(text: str) -> set[str]:
    result, counts = set(), {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', strip_fences(text), re.M):
        slug = slugify(title)
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        result.add(slug if n == 0 else f'{slug}-{n}')
    return result


def link_targets(text: str) -> list[tuple[str, str | None]]:
    """Return (target, alt-or-None) pairs. alt is set for images."""
    visible = strip_fences(text)
    out = []
    for m in re.finditer(r'(!?)\[([^\]]*)\]\(([^\s)]+)(?:\s+"[^"]*")?\)', visible):
        out.append((m.group(3), m.group(2) if m.group(1) else None))
    for m in re.finditer(r'<img\b[^>]*>', visible):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        if src:
            out.append((src.group(1), alt.group(1) if alt else ''))
    for m in re.finditer(r'<a\b[^>]*href="([^"]+)"', visible):
        out.append((m.group(1), None))
    return out


def png_size(path: Path) -> tuple[int, int] | None:
    raw = path.read_bytes()[:24]
    if raw[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return struct.unpack('>II', raw[16:24])


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---\n', 4)
    if end == -1:
        return None, text
    data = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        m = re.match(r'^([A-Za-z][\w-]*):\s*(.*)$', line)
        if not m:
            return None, text
        data[m.group(1)] = m.group(2).strip()
    return data, text[end + 5:]


def money(value: str) -> Decimal:
    return Decimal(value.replace('$', '').replace(',', ''))


# ---------- individual checks (pure functions, used by tests) ----------

def check_agent(text: str, stem: str) -> list[str]:
    errors = []
    fm, body = parse_frontmatter(text)
    if fm is None:
        return [f'{stem}: frontmatter missing or not simple key: value lines']
    for key in ('name', 'description', 'model', 'tools', 'effort'):
        if not fm.get(key):
            errors.append(f'{stem}: missing frontmatter field "{key}"')
    if fm.get('name') and fm['name'] != stem:
        errors.append(f'{stem}: name "{fm["name"]}" does not match file name')
    if fm.get('name') and ':' in fm['name']:
        errors.append(f'{stem}: name cannot contain ":"')
    if fm.get('model') and fm['model'] not in MODELS:
        errors.append(f'{stem}: model "{fm["model"]}" is not a current model ID')
    if fm.get('effort') and fm['effort'] not in EFFORTS:
        errors.append(f'{stem}: effort "{fm["effort"]}" is not a valid level')
    if fm.get('tools'):
        tools = [t.strip() for t in fm['tools'].split(',')]
        unknown = [t for t in tools if t not in KNOWN_TOOLS]
        if unknown:
            errors.append(f'{stem}: unknown tools {unknown}')
        if 'Agent' in tools:
            errors.append(f'{stem}: guide agents must not spawn subagents (remove Agent)')
    if 'final message' not in body.lower():
        errors.append(f'{stem}: body must say its final message is the handoff')
    return errors


def parse_rates(models_text: str) -> dict[str, tuple[Decimal, Decimal, Decimal]]:
    rates = {}
    for m in re.finditer(r'^\| `(claude-[\w-]+)` \| (\$[\d.]+) \| (\$[\d.]+) \| (\$[\d.]+) \|$',
                         models_text, re.M):
        if m.group(1) in rates:
            raise ValueError(f'duplicate rate row for {m.group(1)}')
        rates[m.group(1)] = (money(m.group(2)), money(m.group(3)), money(m.group(4)))
    return rates


def check_rates_and_costs(models_text: str, cost_text: str, readme_text: str) -> list[str]:
    errors = []
    try:
        rates = parse_rates(models_text)
    except ValueError as e:
        return [f'models-and-effort: {e}']
    if set(rates) != set(MODELS):
        errors.append(f'models-and-effort: expected one rate row per model, found {sorted(rates)}')
    by_name = {MODELS[k]: v for k, v in rates.items() if k in MODELS}

    prose = re.search(r'\*\*([\d,]+) uncached input tokens and ([\d,]+) billable output tokens\*\*',
                      cost_text)
    if not prose:
        errors.append('cost-and-evaluation: example token counts not found in prose')
        return errors
    tin, tout = int(prose.group(1).replace(',', '')), int(prose.group(2).replace(',', ''))
    rows = re.findall(r'^\| (Fable 5\.1|Opus 5\.5|Sonnet 5\.5|Haiku 5\.5) \| ([\d,]+) / 1M × (\$[\d.]+) \| '
                      r'([\d,]+) / 1M × (\$[\d.]+) \| (\$[\d.]+) \|$', cost_text, re.M)
    if len(rows) != 4:
        errors.append(f'cost-and-evaluation: expected 4 arithmetic rows, found {len(rows)}')
    for name, rin, pin, rout, pout, total in rows:
        if int(rin.replace(',', '')) != tin or int(rout.replace(',', '')) != tout:
            errors.append(f'cost-and-evaluation: {name} token counts differ from the prose')
        if name in by_name:
            exp_in, _, exp_out = by_name[name]
            if money(pin) != exp_in or money(pout) != exp_out:
                errors.append(f'cost-and-evaluation: {name} rates differ from models-and-effort')
        computed = (Decimal(tin) * money(pin) + Decimal(tout) * money(pout)) / Decimal(1_000_000)
        if computed.quantize(Decimal('0.001')) != money(total):
            errors.append(f'cost-and-evaluation: {name} displayed total {total} != computed {computed}')

    readme_rows = re.findall(r'^\| \*\*(Fable 5\.1|Opus 5\.5|Sonnet 5\.5|Haiku 5\.5)\*\* \|.*?\| '
                             r'(\$[\d.]+) / (\$[\d.]+)[^|]*\|$', readme_text, re.M)
    if len(readme_rows) != 4:
        errors.append(f'README: expected 4 rows with prices in the 30-second table, found {len(readme_rows)}')
    for name, pin, pout in readme_rows:
        if name in by_name and (money(pin) != by_name[name][0] or money(pout) != by_name[name][2]):
            errors.append(f'README: {name} price differs from models-and-effort')
    return errors


def check_readme_agents(readme_text: str, agents: dict[str, dict[str, str]]) -> list[str]:
    errors = []
    rows = re.findall(r'^\| \[(\w+)\]\(agents/\1\.md\) \| `(claude-[\w-]+)` \| (\w+) \|', readme_text, re.M)
    if sorted(r[0] for r in rows) != sorted(AGENT_NAMES):
        errors.append(f'README: agent table rows {sorted(r[0] for r in rows)} != agent files')
    for name, model, effort in rows:
        fm = agents.get(name, {})
        if fm.get('model') != model or fm.get('effort') != effort:
            errors.append(f'README: {name} shows {model}/{effort}, file has {fm.get("model")}/{fm.get("effort")}')
    return errors


def check_agents_doc(doc_text: str, agents: dict[str, dict[str, str]]) -> list[str]:
    """docs/agents.md roster: model / effort and tools must match each file."""
    errors = []
    rows = re.findall(r'^\| \[(\w+)\]\(\.\./agents/\1\.md\) \| (Fable 5\.1|Opus 5\.5|Sonnet 5\.5|Haiku 5\.5) / (\w+) \| ([^|]+) \|',
                      doc_text, re.M)
    if sorted(r[0] for r in rows) != sorted(AGENT_NAMES):
        errors.append(f'docs/agents.md: roster rows {sorted(r[0] for r in rows)} != agent files')
    for name, model, effort, tools in rows:
        fm = agents.get(name, {})
        if MODELS.get(fm.get('model', '')) != model or fm.get('effort') != effort:
            errors.append(f'docs/agents.md: {name} shows {model} / {effort}, file differs')
        if [x.strip() for x in tools.split(',')] != [x.strip() for x in fm.get('tools', '').split(',')]:
            errors.append(f'docs/agents.md: {name} tools differ from the agent file')
    return errors


def check_min_version(texts: dict[str, str], version: str) -> list[str]:
    """Every stated Claude Code minimum for the team must equal the installer's."""
    errors = []
    for label, text in texts.items():
        for found in re.findall(r'(?:Claude_Code-|[Vv]ersion v|Claude Code(?:\]\([^)]*\))?\*{0,2} \*{0,2}v?)(2\.1\.\d+)(?:%2B|\+|\*{0,2} or later)', text):
            if found != version:
                errors.append(f'{label}: states minimum {found}, installer requires {version}')
    return errors


def check_text_hygiene(text: str, label: str) -> list[str]:
    errors = []
    for marker in MARKERS:
        if re.search(rf'\b{re.escape(marker)}\b', text, re.I if ' ' in marker else 0):
            errors.append(f'{label}: leftover marker "{marker}"')
    if re.search(r'(?:ghp_|gho_|github_pat_|sk-ant-|sk-proj-|xox[bp]-|AKIA)[A-Za-z0-9_-]{12,}', text):
        errors.append(f'{label}: credential-like string')
    if re.search(r'(?:/home/|/Users/|C:\\Users\\)[A-Za-z]', text):
        errors.append(f'{label}: local home-directory path')
    if re.search(r'-----BEGIN [A-Z ]*PRIVATE KEY-----', text):
        errors.append(f'{label}: private key block')
    for email in re.findall(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+', text):
        if email.lower() not in ALLOWED_EMAILS and not email.lower().endswith('@example.com'):
            errors.append(f'{label}: unexpected email address {email}')
    return errors


def check_hype(text: str, label: str) -> list[str]:
    prose = strip_fences(text).lower()
    return [f'{label}: hype word "{w}"' for w in HYPE if re.search(rf'(?<![\w-]){re.escape(w)}(?![\w-])', prose)]


# ---------- repository walk ----------

def main(argv: list[str]) -> int:
    allow_missing_images = '--allow-missing-images' in argv
    errors: list[str] = []
    notes: list[str] = []
    stats = {'markdown': 0, 'links': 0, 'images': 0}

    files = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts
             and '__pycache__' not in p.parts]
    markdown = sorted(p for p in files if p.suffix == '.md')
    heading_cache: dict[Path, set[str]] = {}
    referenced_images: set[str] = set()

    for path in markdown:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding='utf-8')
        stats['markdown'] += 1
        if len(re.findall(r'^```', text, re.M)) % 2:
            errors.append(f'{rel}: unclosed code fence')
        for target, alt in link_targets(text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or target.startswith('mailto:'):
                continue
            stats['links'] += 1
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not dest.is_relative_to(ROOT):
                errors.append(f'{rel}: link escapes repository: {target}')
                continue
            dest_rel = dest.relative_to(ROOT).as_posix()
            is_image = alt is not None or dest.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
            if is_image:
                stats['images'] += 1
                referenced_images.add(dest_rel)
                if alt is not None and len(alt.strip()) < 15:
                    errors.append(f'{rel}: image {target} needs descriptive alt text')
            if not dest.exists():
                if allow_missing_images and dest_rel.startswith('assets/'):
                    notes.append(f'pending asset: {dest_rel}')
                else:
                    errors.append(f'{rel}: missing link target {target}')
                continue
            if parsed.fragment and dest.suffix == '.md':
                if dest not in heading_cache:
                    heading_cache[dest] = headings(dest.read_text(encoding='utf-8'))
                if unquote(parsed.fragment) not in heading_cache[dest]:
                    errors.append(f'{rel}: missing heading #{parsed.fragment} in {dest_rel}')

    # Required images: referenced, present, real PNGs.
    for img in REQUIRED_IMAGES:
        if img not in referenced_images:
            errors.append(f'required image never referenced: {img}')
    publish = (ROOT / 'PUBLISH.md')
    if publish.exists() and SOCIAL_PREVIEW not in publish.read_text(encoding='utf-8'):
        errors.append(f'PUBLISH.md must reference {SOCIAL_PREVIEW}')
    for img in sorted(set(REQUIRED_IMAGES) | {SOCIAL_PREVIEW}):
        path = ROOT / img
        if not path.exists():
            if allow_missing_images:
                notes.append(f'pending image: {img}')
            else:
                errors.append(f'missing image file: {img}')
            continue
        size = png_size(path)
        if size is None:
            errors.append(f'{img}: not a valid PNG')
        elif img == SOCIAL_PREVIEW and size != (1280, 640):
            errors.append(f'{img}: expected 1280x640, found {size[0]}x{size[1]}')
        elif size[0] < 600:
            errors.append(f'{img}: width {size[0]} is too small for a README image')
    if not (ROOT / 'assets/README.md').exists():
        (notes if allow_missing_images else errors).append('assets/README.md gallery not present')

    # Agents.
    agent_dir = ROOT / 'agents'
    md_in_agents = sorted(p.stem for p in agent_dir.glob('**/*.md'))
    if md_in_agents != sorted(AGENT_NAMES):
        errors.append(f'agents/: expected exactly {sorted(AGENT_NAMES)}, found {md_in_agents}')
    agents = {}
    for name in AGENT_NAMES:
        path = agent_dir / f'{name}.md'
        if path.exists():
            text = path.read_text(encoding='utf-8')
            errors.extend(check_agent(text, name))
            agents[name] = parse_frontmatter(text)[0] or {}
    installer = (ROOT / 'install.sh').read_text(encoding='utf-8')
    m = re.search(r'^\s*(?:local )?AGENTS=\(([^)]*)\)', installer, re.M)
    if not m or sorted(m.group(1).split()) != sorted(AGENT_NAMES):
        errors.append('install.sh: AGENTS list does not match agent files')

    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    errors.extend(check_readme_agents(readme, agents))
    errors.extend(check_agents_doc((ROOT / 'docs/agents.md').read_text(encoding='utf-8'), agents))
    mv = re.search(r'MIN_VERSION="([\d.]+)"', installer)
    if not mv:
        errors.append('install.sh: MIN_VERSION not found')
    else:
        team_docs = {n: (ROOT / n).read_text(encoding='utf-8') for n in
                     ('README.md', 'SETUP.md', 'CHANGELOG.md', 'docs/product-surfaces.md')}
        errors.extend(check_min_version(team_docs, mv.group(1)))
    errors.extend(check_rates_and_costs(
        (ROOT / 'docs/models-and-effort.md').read_text(encoding='utf-8'),
        (ROOT / 'docs/cost-and-evaluation.md').read_text(encoding='utf-8'),
        readme))

    # Counted artifacts.
    selector = (ROOT / 'docs/task-selector.md').read_text(encoding='utf-8')
    numbers = [int(n) for n in re.findall(r'^\| (\d+) \|', selector, re.M)]
    if numbers != list(range(1, EXPECTED_TASKS + 1)):
        errors.append(f'task-selector: expected rows 1..{EXPECTED_TASKS}, found {len(numbers)}')
    recipes = (ROOT / 'docs/workflows.md').read_text(encoding='utf-8')
    found = [int(n) for n in re.findall(r'^## (\d+)\. ', recipes, re.M)]
    if found != list(range(1, EXPECTED_RECIPES + 1)):
        errors.append(f'workflows: expected recipes 1..{EXPECTED_RECIPES}, found {found}')

    # Docs breadcrumbs.
    for path in sorted((ROOT / 'docs').glob('*.md')):
        first = next((l for l in path.read_text(encoding='utf-8').splitlines() if l.strip()), '')
        if '[Home](../README.md)' not in first:
            errors.append(f'docs/{path.name}: first line must be a breadcrumb with [Home](../README.md)')

    # Manifests and metadata.
    try:
        plugin = json.loads((ROOT / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        entry_names = [p['name'] for p in market['plugins']]
        if plugin['name'] not in entry_names:
            errors.append('marketplace.json: no entry matches plugin.json name')
        cff = (ROOT / 'CITATION.cff').read_text(encoding='utf-8')
        if f'version: {plugin["version"]}' not in cff:
            errors.append('CITATION.cff version differs from plugin.json')
    except (OSError, KeyError, json.JSONDecodeError) as e:
        errors.append(f'plugin manifests: {e}')
    for path in files:
        if path.suffix == '.json':
            try:
                json.loads(path.read_text(encoding='utf-8'))
            except json.JSONDecodeError as e:
                errors.append(f'{path.relative_to(ROOT)}: invalid JSON ({e})')

    # VYR links carry campaign tags on the pages that promote VYR.
    for name in ('README.md', 'WORK_WITH_VYR.md'):
        for url in re.findall(r'https://vyrwork\.com[^\s)"]*', (ROOT / name).read_text(encoding='utf-8')):
            if 'utm_campaign=claude_agent_guide' not in url:
                errors.append(f'{name}: VYR link without utm_campaign=claude_agent_guide: {url}')

    # Text hygiene across the repository.
    for path in files:
        if path.suffix not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding='utf-8')
        errors.extend(check_text_hygiene(text, rel))
        if path.suffix == '.md' and not rel.startswith('docs/atlas/'):
            errors.extend(check_hype(text, rel))
        if rel == 'PUBLISH.md':  # launch copy lives inside code fences
            errors.extend(check_hype(text.replace('```', ''), rel + ' (posts)'))

    for note in sorted(set(notes)):
        print(f'note: {note}')
    if errors:
        print(f'FAIL: {len(errors)} problem(s)')
        for e in errors:
            print(f'  - {e}')
        return 1
    print(f'PASS: {stats["markdown"]} Markdown files; {stats["links"]} local links and anchors; '
          f'{stats["images"]} image references; {len(AGENT_NAMES)} agents; {EXPECTED_TASKS} tasks; '
          f'{EXPECTED_RECIPES} recipes; rates and cost arithmetic; hygiene checks.'
          + (' (images pending)' if any(n.startswith('pending') for n in notes) else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
