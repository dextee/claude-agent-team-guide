#!/usr/bin/env bash
# Claude Code Agent Team installer
# https://github.com/dextee/claude-agent-team-guide
#
# Installs eight model-matched Claude Code subagents. Safe to re-run:
# identical files are skipped, changed files are backed up, and your
# settings are untouched unless you pass --with-settings.
#
#   curl -fsSL https://raw.githubusercontent.com/dextee/claude-agent-team-guide/main/install.sh | bash
#   curl -fsSL .../install.sh | bash -s -- --dry-run
#
# Options:
#   --dry-run         Show what would change; change nothing
#   --project DIR     Install into DIR/.claude/agents (share with a team via git)
#                     instead of your user agents folder
#   --with-settings   Also merge the recommended settings preset into settings.json
#                     (keeps any value you already set)
#   --force           With --with-settings, replace conflicting preset values
#   --uninstall       Remove agent files this installer wrote and you have not
#                     edited since; edited files are kept and reported
#   -h, --help        Show this help
#
# Set AGENT_TEAM_REF=<tag or commit> to download agents from a fixed release.

set -euo pipefail

AGENT_TEAM_TMP=""

# Everything runs inside main(), called on the last line, so a truncated
# download through curl | bash cannot execute a partial script.
main() {
  local REPO="dextee/claude-agent-team-guide"
  local REF="${AGENT_TEAM_REF:-main}"
  local RAW="https://raw.githubusercontent.com/${REPO}/${REF}"
  local AGENTS=(architect implementer worker explorer reviewer auditor researcher editor)
  local MIN_VERSION="2.1.293"
  local MANIFEST_NAME=".agent-team-manifest"

  local dry_run=0 with_settings=0 force=0 uninstall=0 project=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --dry-run) dry_run=1 ;;
      --with-settings) with_settings=1 ;;
      --force) force=1 ;;
      --uninstall) uninstall=1 ;;
      --project) project="${2:?--project needs a directory}"; shift ;;
      -h|--help)
        if [ -f "${BASH_SOURCE[0]:-}" ]; then sed -n '2,23p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
        else echo "See https://github.com/${REPO}/blob/main/SETUP.md"; fi
        return 0 ;;
      *) echo "Unknown option: $1 (try --help)" >&2; return 2 ;;
    esac
    shift
  done

  if [ "$force" = 1 ] && [ "$with_settings" = 0 ]; then
    echo "--force only applies together with --with-settings" >&2; return 2
  fi

  local c1="" c2="" c0=""
  if [ -t 1 ]; then c1=$'\033[1;36m' c2=$'\033[1;33m' c0=$'\033[0m'; fi
  say()  { printf '%s==>%s %s\n' "$c1" "$c0" "$*"; }
  warn() { printf '%s!!%s %s\n' "$c2" "$c0" "$*" >&2; }
  run()  { if [ "$dry_run" = 1 ]; then echo "   [dry-run] $*"; else "$@"; fi; }
  hash_of() {
    if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1
    else shasum -a 256 "$1" | cut -d' ' -f1; fi
  }

  [ "$dry_run" = 1 ] && say "Dry run: nothing will be written."

  local claude_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}" agents_dir
  if [ -n "$project" ]; then
    [ -d "$project" ] || { echo "Project directory not found: $project" >&2; return 1; }
    agents_dir="$(cd "$project" && pwd)/.claude/agents"
  else
    agents_dir="$claude_dir/agents"
  fi
  local settings_file="$claude_dir/settings.json"
  local manifest="$agents_dir/$MANIFEST_NAME"
  local stamp; stamp="$(date +%Y%m%d-%H%M%S)"

  # Refuse to write through a symlinked agents folder. Parent folders such as
  # ~/.claude are used as they are; only the agents folder and files are checked.
  if [ -L "$agents_dir" ]; then
    echo "Refusing to write: $agents_dir is a symlink. Install with --project or fix the link." >&2; return 1
  fi
  if [ -L "$manifest" ] || { [ -e "$manifest" ] && [ ! -f "$manifest" ]; }; then
    warn "Refusing a non-regular or symlinked manifest: $manifest"; return 1
  fi
  # Validate every record before touching any destination, including roles
  # retired since installation. Names must be plain agent filenames.
  if [ -f "$manifest" ] && ! awk '
    NF != 2 || length($1) != 64 || $1 !~ /^[a-f0-9]+$/ ||
    $2 !~ /^[a-z][a-z0-9-]*[.]md$/ || seen[$2]++ {exit 1}
  ' "$manifest"; then
    warn "Invalid agent-team manifest; no files changed."; return 1
  fi

  local dest digest filename
  if [ "$uninstall" = 1 ]; then
    if [ ! -f "$manifest" ]; then say "No ownership manifest. No agents removed."; return 0; fi
    while read -r digest filename || [ -n "$filename" ]; do
      dest="$agents_dir/$filename"
      if [ ! -e "$dest" ] && [ ! -L "$dest" ]; then continue; fi
      if [ ! -L "$dest" ] && [ -f "$dest" ] && [ "$(hash_of "$dest")" = "$digest" ]; then
        run rm -- "$dest"; echo "   - $filename"
      else
        echo "   ! $filename kept (changed or not a regular file)"
      fi
    done < "$manifest"
    run rm -- "$manifest"
    say "Settings and backups were left in place."
    return 0
  fi

  # Version check is advisory: files are copied either way. stdin is closed so
  # the child cannot read the rest of a piped script.
  if command -v claude >/dev/null 2>&1; then
    local have
    have="$(claude --version </dev/null 2>/dev/null | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' | head -n1 || true)"
    if [ -n "$have" ] && [ "$(printf '%s\n%s\n' "$MIN_VERSION" "$have" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
      warn "Claude Code $have found. These agents need $MIN_VERSION or later (Haiku 5.5). Run: claude update"
    fi
  else
    warn "claude was not found on PATH. Files will still be installed; install Claude Code to use them."
  fi

  # Use local files when run from a clone, otherwise download from GitHub.
  local script_dir="" src_dir
  if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  fi
  if [ -n "$script_dir" ] && [ -f "$script_dir/agents/architect.md" ]; then
    src_dir="$script_dir"
    say "Using local files from $src_dir"
  else
    command -v curl >/dev/null || { echo "curl is required" >&2; return 1; }
    src_dir="$(mktemp -d)"
    AGENT_TEAM_TMP="$src_dir"   # global: the EXIT trap runs after main's locals are gone
    trap 'rm -rf "${AGENT_TEAM_TMP:-}"' EXIT
    mkdir -p "$src_dir/agents" "$src_dir/templates"
    say "Downloading the agent team from github.com/$REPO ($REF)"
    local a
    for a in "${AGENTS[@]}"; do
      curl -fsSL "$RAW/agents/$a.md" -o "$src_dir/agents/$a.md" </dev/null
    done
    curl -fsSL "$RAW/templates/recommended-settings.json" -o "$src_dir/templates/recommended-settings.json" </dev/null
  fi

  local a
  for a in "${AGENTS[@]}"; do
    head -n1 "$src_dir/agents/$a.md" | grep -qx -- '---' || { echo "Unexpected content in $a.md; aborting." >&2; return 1; }
  done

  # Validate requested settings before touching agents or taking backups.
  if [ "$with_settings" = 0 ]; then
    say "Settings untouched (pass --with-settings to merge the recommended preset)"
  elif ! command -v python3 >/dev/null; then
    warn "--with-settings requires python3. No files changed."; return 1
  else
    if [ -L "$settings_file" ] || { [ -e "$settings_file" ] && [ ! -f "$settings_file" ]; }; then
      warn "Refusing a non-regular or symlinked settings file."; return 1
    fi
    say "Merging the recommended preset into $settings_file"
    FORCE="$force" DRY="$dry_run" python3 - "$settings_file" "$src_dir/templates/recommended-settings.json" <<'PY'
import copy, json, os, shutil, sys, tempfile
path, rec_path = sys.argv[1], sys.argv[2]
force, dry = os.environ["FORCE"] == "1", os.environ["DRY"] == "1"
try:
    with open(path, encoding="utf-8") as f:
        current = json.load(f)
except FileNotFoundError:
    current = {}
except json.JSONDecodeError as e:
    sys.exit(f"   {path} is not valid JSON ({e}). Fix it, then re-run.")
with open(rec_path, encoding="utf-8") as f:
    rec = json.load(f)
if not isinstance(current, dict) or not isinstance(rec, dict):
    sys.exit("   Settings and preset must both be JSON objects.")
before = copy.deepcopy(current)
rec.pop("$comment", None)

def merge(cur, new, prefix=""):
    for key, value in new.items():
        name = prefix + key
        if isinstance(value, dict) and isinstance(cur.get(key), dict):
            merge(cur[key], value, name + ".")
        elif key not in cur:
            cur[key] = value
            print(f"   + {name} = {json.dumps(value)}")
        elif cur[key] == value:
            print(f"   = {name} (already set)")
        elif force:
            print(f"   ~ {name} updated")
            cur[key] = value
        else:
            print(f"   ! {name} kept (use --force to replace)")

merge(current, rec)
if not dry and current != before:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if os.path.exists(path):
        fd, backup = tempfile.mkstemp(dir=os.path.dirname(path), prefix="settings.json.bak-")
        os.close(fd)
        shutil.copy2(path, backup)
        print(f"   backup: {backup}")
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", prefix=".settings-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)
PY
  fi

  say "Installing agents into $agents_dir"
  run mkdir -p "$agents_dir"
  local src backup next_manifest
  for a in "${AGENTS[@]}"; do
    src="$src_dir/agents/$a.md" dest="$agents_dir/$a.md"
    if [ -L "$dest" ]; then warn "$a skipped: $dest is a symlink"; continue; fi
    if [ -e "$dest" ] && [ ! -f "$dest" ]; then warn "$a skipped: $dest is not a regular file"; continue; fi
    if [ -f "$dest" ] && cmp -s "$src" "$dest"; then
      echo "   = $a (already up to date)"; continue
    fi
    if [ -f "$dest" ]; then
      if [ "$dry_run" = 1 ]; then echo "   ~ $a (would back up and update)"; continue; fi
      backup="$(mktemp "$dest.bak-$stamp-XXXXXX")"
      cp -p "$dest" "$backup"; echo "   ~ $a (backup: $backup)"
    else
      echo "   + $a"
    fi
    if [ "$dry_run" = 1 ]; then continue; fi
    cp "$src" "$dest"
    # Only claim files actually written. Keep previous records (including
    # retired roles) and replace the manifest atomically after each write.
    next_manifest="$(mktemp "$agents_dir/.agent-team-record-XXXXXX")"
    if [ -f "$manifest" ]; then awk -v f="$a.md" '$2 != f' "$manifest" > "$next_manifest"; fi
    printf '%s  %s\n' "$(hash_of "$dest")" "$a.md" >> "$next_manifest"
    mv -f -- "$next_manifest" "$manifest"
  done

  if [ "$dry_run" = 1 ]; then say "Dry run complete. Re-run without --dry-run to apply."; return 0; fi

  cat <<EOF

$(say "Done.")
Next steps:
  1. Start a new Claude Code session (v$MIN_VERSION or later) in your project.
  2. Ask: "Use the explorer agent to list this project's entry points and test commands."
  3. Run /tasks while it works to see which model each agent is running on.
  4. Fable agents (architect, auditor) may bill usage credits on some plans. In an
     interactive session you are asked first; with claude -p you are not.

Guide: https://github.com/$REPO
EOF
}

main "$@"
