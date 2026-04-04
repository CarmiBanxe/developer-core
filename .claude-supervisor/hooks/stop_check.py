#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUP = ROOT / '.claude-supervisor'
LOGS = SUP / 'logs'
STATUS_PATH = LOGS / 'final_status.json'

res = subprocess.run([sys.executable, str(SUP / 'verifier.py')], capture_output=True, text=True)
summary = {
    "verifier_exit_code": res.returncode,
    "stdout": res.stdout.strip(),
    "stderr": res.stderr.strip()
}
LOGS.mkdir(parents=True, exist_ok=True)
STATUS_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

if res.returncode != 0:
    print(json.dumps({"decision": "deny", "reason": "Verifier failed. Check .claude-supervisor/logs/final_status.json"}, ensure_ascii=False))
else:
    print(json.dumps({"decision": "allow", "reason": "Verifier passed"}, ensure_ascii=False))
