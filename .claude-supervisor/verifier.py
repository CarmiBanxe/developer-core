#!/usr/bin/env python3
import json, fnmatch, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / 'state'
LOGS = ROOT / 'logs'
CONTRACT_PATH = STATE / 'active_contract.json'
SUMMARY_PATH = LOGS / 'verifier_summary.json'

if not CONTRACT_PATH.exists():
    print('No active contract found', file=sys.stderr)
    sys.exit(2)

contract = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
proc = subprocess.run(['git', 'diff', '--numstat'], capture_output=True, text=True)

if proc.returncode != 0:
    print('git diff --numstat failed; is this a git repo?', file=sys.stderr)
    sys.exit(3)

changed = []
added = deleted = 0

for line in proc.stdout.splitlines():
    parts = line.split('\t')
    if len(parts) != 3:
        continue
    a, d, path = parts
    changed.append(path)
    if a.isdigit():
        added += int(a)
    if d.isdigit():
        deleted += int(d)

scope = contract.get('files_in_scope', [])
outside = [p for p in changed if not any(fnmatch.fnmatch(p, s) for s in scope)]

forbidden = []
for p in changed:
    low = p.lower()
    if '/.env' in low or low.endswith('.env') or low.endswith('.pem') or low.endswith('.key') or 'secret' in low or 'credential' in low or 'token' in low:
        forbidden.append(p)

limits = contract.get('patch_limits', {})
errors = []

if outside:
    errors.append(f'Changed files outside scope: {outside}')
if forbidden:
    errors.append(f'Forbidden-looking files changed: {forbidden}')
if len(changed) > limits.get('max_files_changed', 10):
    errors.append(f'Too many files changed: {len(changed)} > {limits.get("max_files_changed", 10)}')
if added > limits.get('max_lines_added', 400):
    errors.append(f'Too many lines added: {added} > {limits.get("max_lines_added", 400)}')
if deleted > limits.get('max_lines_deleted', 200):
    errors.append(f'Too many lines deleted: {deleted} > {limits.get("max_lines_deleted", 200)}')

summary = {
    "changed_files": changed,
    "added": added,
    "deleted": deleted,
    "outside_scope": outside,
    "forbidden_hits": forbidden,
    "errors": errors,
    "result": "pass" if not errors else "fail"
}

LOGS.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False))
sys.exit(0 if not errors else 1)
