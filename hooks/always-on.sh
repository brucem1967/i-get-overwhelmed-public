#!/usr/bin/env sh
# SessionStart hook: injects the i-get-overwhelmed rules (and the reader profile, if one exists) when the user has opted in
# by creating $CLAUDE_CONFIG_DIR/.i-get-overwhelmed-always (default ~/.claude). Never blocks session start: any failure exits 0.
# Forked from ayghri/i-have-adhd (MIT). Runs in sh on Linux/macOS and in Git Bash on Windows (no Node needed).

claude_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
flag_path="$claude_dir/.i-get-overwhelmed-always"
[ -f "$flag_path" ] || exit 0

script_dir=$(dirname -- "$0")
skill_dir="$script_dir/../skills/i-get-overwhelmed"
[ -f "$skill_dir/SKILL.md" ] || exit 0

# drop the YAML frontmatter (first line '---' up to the next '---')
body=$(awk 'NR==1 && /^---[[:space:]]*$/ {fm=1; next} fm && /^---[[:space:]]*$/ {fm=0; next} !fm {print}' "$skill_dir/SKILL.md") || exit 0

printf 'OVERWHELM MODE ACTIVE (always-on). The rules below apply to every response. "stop overwhelm mode" turns it off for this session; delete %s to turn always-on off for good.\n\n%s\n' "$flag_path" "$body"
if [ -f "$skill_dir/READER.md" ]; then
  printf '\n\n# Reader profile (follow this too; it wins where it differs)\n\n'
  cat "$skill_dir/READER.md"
fi
exit 0
