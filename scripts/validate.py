#!/usr/bin/env python3
"""Static checks for the Claude Code Agent Team Guide.

Checks internal links and heading anchors, image references and files,
agent frontmatter (field names, values, and a PyYAML cross-parse when PyYAML
is installed), README/agent agreement, model IDs, rates, minimum versions and
cost arithmetic against templates/models.json, model names, pinned download
URLs, docs footers and check dates, recipe and pattern structure, leftover
markers, hype words, credential patterns and email addresses. Read-only;
never calls a model or the network.

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

try:  # Optional: a second, independent parse of agent frontmatter.
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - depends on the environment
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MODELS_FILE = ROOT / 'templates' / 'models.json'


def load_models(path: Path = MODELS_FILE) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


MODEL_DATA = load_models()
CHECKED_ON = MODEL_DATA['checked_on']
CURRENT = {m['id']: m for m in MODEL_DATA['current']}
OLDER = {m['id']: m for m in MODEL_DATA['older']}
MODELS = {k: v['name'] for k, v in CURRENT.items()}           # ID -> display name
KNOWN_MODEL_NAMES = ({m['name'] for m in MODEL_DATA['current']} | {m['name'] for m in MODEL_DATA['older']}
                     | set(MODEL_DATA['other_known_names']))
EFFORTS = set(MODEL_DATA['effort_levels'])
NAME_ALT = '|'.join(re.escape(n) for n in MODELS.values())

AGENT_NAMES = ['architect', 'implementer', 'worker', 'explorer',
               'reviewer', 'auditor', 'researcher', 'editor']
KNOWN_TOOLS = {'Read', 'Edit', 'Write', 'Glob', 'Grep', 'Bash', 'WebFetch', 'WebSearch',
               'Agent', 'NotebookEdit', 'TodoWrite'}
# Every frontmatter field in the official subagent reference
# (https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields, checked 2026-11-15).
# Claude Code silently ignores a field it does not recognize, so a typo here is a real defect.
FRONTMATTER_FIELDS = {'name', 'description', 'tools', 'disallowedTools', 'model', 'permissionMode',
                      'maxTurns', 'autoCompactWindow', 'skills', 'mcpServers', 'hooks', 'memory',
                      'background', 'omitClaudeMd', 'effort', 'isolation', 'color', 'initialPrompt',
                      'experimental'}
COLORS = {'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan'}
PERMISSION_MODES = {'default', 'manual', 'acceptEdits', 'auto', 'dontAsk', 'bypassPermissions', 'plan'}
MEMORY_SCOPES = {'user', 'project', 'local'}
REQUIRED_IMAGES = [
    'assets/images/hero.png', 'assets/images/model-team.png', 'assets/images/orchestration.png',
    'assets/images/workflow-coding.png', 'assets/images/workflow-research.png',
    'assets/images/workflow-review.png', 'assets/images/workflow-docs.png',
    'assets/images/workflow-ops.png',
]
SOCIAL_PREVIEW = 'assets/social-preview.png'
EXPECTED_TASKS = 24
EXPECTED_RECIPES = 12
EXPECTED_PATTERNS = 6
REPO = 'dextee/claude-agent-team-guide'
PROOF_LINE = '**What proves it worked:**'
DISCLAIMER = 'Independent guide, not an Anthropic publication'
# Pages left untouched pending an owner decision. They are reported, not failed.
FOOTER_EXEMPT = {'docs/atlas/compliance-evidence.md'}
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


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---\n', 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5:]


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    """Strict flat parser: every line must be `key: value`. Nested YAML is rejected on purpose,
    so the guide's own agents stay readable without a YAML library."""
    raw, body = split_frontmatter(text)
    if raw is None:
        return None, text
    data = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        m = re.match(r'^([A-Za-z][\w-]*):\s*(.*)$', line)
        if not m:
            return None, text
        data[m.group(1)] = m.group(2).strip()
    return data, body


def version_tuple(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.split('.'))


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
    for key in fm:
        if key not in FRONTMATTER_FIELDS:
            errors.append(f'{stem}: "{key}" is not a documented frontmatter field (Claude Code would ignore it)')
    name = fm.get('name', '')
    if name and name != stem:
        errors.append(f'{stem}: name "{name}" does not match file name')
    if name and (':' in name or name.startswith('-') or len(name) > 256):
        errors.append(f'{stem}: name cannot contain ":", start with "-" or exceed 256 characters')
    if fm.get('model') and fm['model'] not in MODELS:
        errors.append(f'{stem}: model "{fm["model"]}" is not a current model ID in templates/models.json')
    if fm.get('effort') and fm['effort'] not in EFFORTS:
        errors.append(f'{stem}: effort "{fm["effort"]}" is not a valid level')
    if 'color' in fm and fm['color'] not in COLORS:
        errors.append(f'{stem}: color "{fm["color"]}" is not one of {sorted(COLORS)}')
    if 'isolation' in fm and fm['isolation'] != 'worktree':
        errors.append(f'{stem}: isolation must be "worktree"')
    if 'maxTurns' in fm and not re.fullmatch(r'[1-9]\d*', fm['maxTurns']):
        errors.append(f'{stem}: maxTurns must be a positive whole number')
    for key in ('omitClaudeMd', 'background'):
        if key in fm and fm[key] not in ('true', 'false'):
            errors.append(f'{stem}: {key} must be true or false')
    if 'permissionMode' in fm and fm['permissionMode'] not in PERMISSION_MODES:
        errors.append(f'{stem}: permissionMode "{fm["permissionMode"]}" is not a documented mode')
    if 'memory' in fm and fm['memory'] not in MEMORY_SCOPES:
        errors.append(f'{stem}: memory must be user, project or local')
    if fm.get('tools'):
        tools = [t.strip() for t in fm['tools'].split(',')]
        unknown = [t for t in tools if t not in KNOWN_TOOLS]
        if unknown:
            errors.append(f'{stem}: unknown tools {unknown}')
        if 'Agent' in tools:
            errors.append(f'{stem}: guide agents must not spawn subagents (remove Agent)')
    if 'final message' not in body.lower():
        errors.append(f'{stem}: body must say its final message is the handoff')
    errors.extend(check_agent_yaml(text, stem, fm))
    return errors


def check_agent_yaml(text: str, stem: str, flat: dict[str, str]) -> list[str]:
    """Cross-check with PyYAML, the parser family Claude Code's YAML frontmatter follows.
    Skipped (not failed) when PyYAML is not installed."""
    if yaml is None:
        return []
    raw, _ = split_frontmatter(text)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return [f'{stem}: frontmatter is not valid YAML ({e.__class__.__name__})']
    if not isinstance(data, dict):
        return [f'{stem}: frontmatter is not a YAML mapping']
    errors = []
    if set(data) != set(flat):
        errors.append(f'{stem}: YAML keys {sorted(data)} differ from line keys {sorted(flat)}')
    if 'maxTurns' in data and (not isinstance(data['maxTurns'], int) or isinstance(data['maxTurns'], bool)):
        errors.append(f'{stem}: maxTurns does not parse as an integer')
    for key in ('omitClaudeMd', 'background'):
        if key in data and not isinstance(data[key], bool):
            errors.append(f'{stem}: {key} does not parse as a boolean')
    for key in ('name', 'description', 'model', 'effort', 'tools', 'color', 'isolation'):
        if key in data and not isinstance(data[key], str):
            errors.append(f'{stem}: {key} does not parse as a string')
    return errors


def parse_rates(models_text: str) -> dict[str, tuple[Decimal, Decimal, Decimal]]:
    rates = {}
    for m in re.finditer(r'^\| `(claude-[\w-]+)` \| (\$[\d.]+) \| (\$[\d.]+) \| (\$[\d.]+) \|',
                         models_text, re.M):
        if m.group(1) in rates:
            raise ValueError(f'duplicate rate row for {m.group(1)}')
        rates[m.group(1)] = (money(m.group(2)), money(m.group(3)), money(m.group(4)))
    return rates


def json_rates(entry: dict) -> tuple[Decimal, Decimal, Decimal]:
    return (Decimal(entry['input_usd_per_mtok']), Decimal(entry['cache_read_usd_per_mtok']),
            Decimal(entry['output_usd_per_mtok']))


def check_rates_and_costs(models_text: str, cost_text: str, readme_text: str,
                          data: dict | None = None) -> list[str]:
    """Rates in the docs must equal templates/models.json, and the cost arithmetic must add up."""
    data = data or MODEL_DATA
    current = {m['id']: m for m in data['current']}
    names = {m['name']: m for m in data['current']}
    name_alt = '|'.join(re.escape(n) for n in names)
    errors = []
    try:
        rates = parse_rates(models_text)
    except ValueError as e:
        return [f'models-and-effort: {e}']
    for model_id, entry in current.items():
        if model_id not in rates:
            errors.append(f'models-and-effort: no rate row for {model_id}')
        elif rates[model_id] != json_rates(entry):
            errors.append(f'models-and-effort: {model_id} rates differ from templates/models.json')
    for model_id in rates:
        if model_id not in current:
            errors.append(f'models-and-effort: rate row for {model_id}, which is not a current model')

    prose = re.search(r'\*\*([\d,]+) uncached input tokens and ([\d,]+) billable output tokens\*\*',
                      cost_text)
    if not prose:
        errors.append('cost-and-evaluation: example token counts not found in prose')
        return errors
    tin, tout = int(prose.group(1).replace(',', '')), int(prose.group(2).replace(',', ''))
    rows = re.findall(rf'^\| ({name_alt}) \| ([\d,]+) / 1M × (\$[\d.]+) \| '
                      r'([\d,]+) / 1M × (\$[\d.]+) \| (\$[\d.]+) \|$', cost_text, re.M)
    if len(rows) != len(names):
        errors.append(f'cost-and-evaluation: expected {len(names)} arithmetic rows, found {len(rows)}')
    for name, rin, pin, rout, pout, total in rows:
        if int(rin.replace(',', '')) != tin or int(rout.replace(',', '')) != tout:
            errors.append(f'cost-and-evaluation: {name} token counts differ from the prose')
        exp_in, _, exp_out = json_rates(names[name])
        if money(pin) != exp_in or money(pout) != exp_out:
            errors.append(f'cost-and-evaluation: {name} rates differ from templates/models.json')
        computed = (Decimal(tin) * money(pin) + Decimal(tout) * money(pout)) / Decimal(1_000_000)
        if computed.quantize(Decimal('0.001')) != money(total):
            errors.append(f'cost-and-evaluation: {name} displayed total {total} != computed {computed}')

    readme_rows = re.findall(rf'^\| \*\*({name_alt})\*\* \|.*?\| '
                             r'(\$[\d.]+) / (\$[\d.]+)[^|]*\|$', readme_text, re.M)
    if len(readme_rows) != len(names):
        errors.append(f'README: expected {len(names)} rows with prices in the 30-second table, found {len(readme_rows)}')
    for name, pin, pout in readme_rows:
        exp_in, _, exp_out = json_rates(names[name])
        if money(pin) != exp_in or money(pout) != exp_out:
            errors.append(f'README: {name} price differs from templates/models.json')
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
    rows = re.findall(rf'^\| \[(\w+)\]\(\.\./agents/\1\.md\) \| ({NAME_ALT}) / (\w+) \| ([^|]+) \|',
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


def team_min_version(agents: dict[str, dict[str, str]], data: dict | None = None) -> str | None:
    """The team's Claude Code minimum is the highest minimum among the models the agents pin."""
    data = data or MODEL_DATA
    mins = {m['id']: m['min_claude_code'] for m in data['current']}
    found = [mins[fm['model']] for fm in agents.values() if fm.get('model') in mins]
    return max(found, key=version_tuple) if found else None


def check_min_version(texts: dict[str, str], version: str) -> list[str]:
    """Every stated Claude Code minimum for the team must equal the installer's."""
    errors = []
    for label, text in texts.items():
        for found in re.findall(r'(?:Claude_Code-|[Vv]ersion v|Claude Code(?:\]\([^)]*\))?\*{0,2} \*{0,2}v?)(2\.1\.\d+)(?:%2B|\+|\*{0,2} or later)', text):
            if found != version:
                errors.append(f'{label}: states minimum {found}, installer requires {version}')
    return errors


def check_raw_refs(text: str, label: str) -> list[str]:
    """A download URL for this repository must name main or a full commit SHA. The repository
    has no tags, so a tag ref would 404 (a v2.0.0 example did)."""
    errors = []
    for ref in re.findall(rf'raw\.githubusercontent\.com/{re.escape(REPO)}/([^/\s"\'`)]+)/', text):
        if ref == 'main' or re.fullmatch(r'[0-9a-f]{40}', ref) or ref in ('<commit-sha>', '${REF}', '$SHA', '${SHA}'):
            continue
        errors.append(f'{label}: raw.githubusercontent.com ref "{ref}" is not main or a 40-character commit SHA')
    return errors


def check_model_names(text: str, label: str, known: set[str] | None = None) -> list[str]:
    """Every Claude model name the guide mentions must be one listed in templates/models.json.
    Catches invented versions, the standing risk in a model guide."""
    known = known or KNOWN_MODEL_NAMES
    errors = []
    for family, version in re.findall(r'\b(Fable|Opus|Sonnet|Haiku)[ -](\d+(?:\.\d+)?)\b', text):
        if f'{family} {version}' not in known:
            errors.append(f'{label}: unknown model name "{family} {version}"')
    return errors


def check_docs_footer(text: str, label: str, checked_on: str, require_date: bool) -> list[str]:
    lines = [l for l in text.splitlines() if l.strip()]
    last = lines[-1] if lines else ''
    errors = []
    if DISCLAIMER not in last:
        errors.append(f'{label}: last line must carry the independent-guide footer')
    elif require_date and f'checked {checked_on}' not in last:
        errors.append(f'{label}: footer must state "checked {checked_on}" (templates/models.json checked_on)')
    return errors


def check_sections(text: str, label: str, heading_re: str, expected: int) -> list[str]:
    """Each numbered section needs a copy-paste ```text prompt and a proof line."""
    errors = []
    parts = re.split(rf'^(?={heading_re})', text, flags=re.M)[1:]
    numbers = []
    for part in parts:
        m = re.match(heading_re + r'(\d+)', part)
        numbers.append(int(m.group(1)) if m else -1)
        title = part.splitlines()[0]
        if '```text' not in part:
            errors.append(f'{label}: "{title}" has no ```text copy-paste prompt')
        if PROOF_LINE not in part:
            errors.append(f'{label}: "{title}" has no "{PROOF_LINE}" line')
    if numbers != list(range(1, expected + 1)):
        errors.append(f'{label}: expected sections 1..{expected}, found {numbers}')
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
    if yaml is None:
        notes.append('PyYAML not installed: agent frontmatter checked with the strict line parser only')
    installer = (ROOT / 'install.sh').read_text(encoding='utf-8')
    m = re.search(r'^\s*(?:local )?AGENTS=\(([^)]*)\)', installer, re.M)
    if not m or sorted(m.group(1).split()) != sorted(AGENT_NAMES):
        errors.append('install.sh: AGENTS list does not match agent files')

    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    errors.extend(check_readme_agents(readme, agents))
    errors.extend(check_agents_doc((ROOT / 'docs/agents.md').read_text(encoding='utf-8'), agents))
    required = team_min_version(agents)
    mv = re.search(r'MIN_VERSION="([\d.]+)"', installer)
    if not mv:
        errors.append('install.sh: MIN_VERSION not found')
    else:
        if required and mv.group(1) != required:
            errors.append(f'install.sh: MIN_VERSION {mv.group(1)} != {required}, the highest '
                          'min_claude_code in templates/models.json among the pinned models')
        team_docs = {n: (ROOT / n).read_text(encoding='utf-8') for n in
                     ('README.md', 'SETUP.md', 'CHANGELOG.md', 'docs/product-surfaces.md',
                      'docs/start-here.md')}
        # CHANGELOG keeps history: only its newest entry must agree.
        team_docs['CHANGELOG.md'] = team_docs['CHANGELOG.md'].split('\n## ')[1] if '\n## ' in team_docs['CHANGELOG.md'] else ''
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
    errors.extend(check_sections((ROOT / 'docs/workflows.md').read_text(encoding='utf-8'),
                                 'docs/workflows.md', r'## (?=\d)', EXPECTED_RECIPES))
    errors.extend(check_sections((ROOT / 'docs/orchestration-patterns.md').read_text(encoding='utf-8'),
                                 'docs/orchestration-patterns.md', r'## Pattern ', EXPECTED_PATTERNS))

    # Docs breadcrumbs and footers.
    for path in sorted((ROOT / 'docs').glob('*.md')):
        first = next((l for l in path.read_text(encoding='utf-8').splitlines() if l.strip()), '')
        if '[Home](../README.md)' not in first:
            errors.append(f'docs/{path.name}: first line must be a breadcrumb with [Home](../README.md)')
    for path in sorted((ROOT / 'docs').rglob('*.md')):
        rel = path.relative_to(ROOT).as_posix()
        if rel in FOOTER_EXEMPT:
            notes.append(f'footer not checked (pending owner decision): {rel}')
            continue
        errors.extend(check_docs_footer(path.read_text(encoding='utf-8'), rel, CHECKED_ON,
                                        require_date=not rel.startswith('docs/atlas/')))

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
        changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
        top = re.search(r'^## (\d+\.\d+\.\d+)', changelog, re.M)
        if not top or top.group(1) != plugin['version']:
            errors.append('CHANGELOG.md: newest entry differs from plugin.json version')
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

    # Text hygiene, model names and download refs across the repository.
    for path in files:
        if path.suffix not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding='utf-8')
        errors.extend(check_text_hygiene(text, rel))
        errors.extend(check_raw_refs(text, rel))
        if rel != 'scripts/test_validate.py':  # the tests feed it invented names on purpose
            errors.extend(check_model_names(text, rel))
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
          f'{stats["images"]} image references; {len(AGENT_NAMES)} agents (frontmatter '
          f'{"line + PyYAML" if yaml else "line"} parse); {EXPECTED_TASKS} tasks; {EXPECTED_RECIPES} recipes; '
          f'{EXPECTED_PATTERNS} patterns; rates, minimum version {required} and cost arithmetic from '
          f'templates/models.json (checked {CHECKED_ON}); model names; download refs; docs footers; hygiene checks.'
          + (' (images pending)' if any(n.startswith('pending') for n in notes) else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
