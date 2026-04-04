#!/usr/bin/env python3
import json, sys, re, fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUP = ROOT / '.claude-supervisor'
STATE = SUP / 'state'
LOGS = SUP / 'logs'
CONTRACT_PATH = STATE / 'active_contract.json'
TRACE_PATH = LOGS / 'trace.jsonl'

FORBIDDEN_PATH_PATTERNS = [
    '.env', '.env.*', '**/.env', '**/.env.*',
    '**/id_rsa', '**/id_ed25519', '**/*.pem', '**/*.key',
    '**/secrets.*', '**/credentials*', '**/token*',
    '.git/**'
]

def load_contract():
    if not CONTRACT_PATH.exists():
        return None
    return json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))

def match_any_pattern(path_str, patterns):
    normalized = path_str.replace('\\', '/')
    return any(fnmatch.fnmatch(normalized, p) for p in patterns)

def in_scope(path_str, scope_patterns):
    normalized = path_str.replace('\\', '/')
    return any(fnmatch.fnmatch(normalized, p) for p in scope_patterns)

def log_event(event, decision, reason):
    LOGS.mkdir(parents=True, exist_ok=True)
    with TRACE_PATH.open('a', encoding='utf-8') as f:
        f.write(json.dumps({"event": event, "decision": decision, "reason": reason}, ensure_ascii=False) + '\n')

def respond(decision, reason):
    print(json.dumps({"decision": decision, "reason": reason}, ensure_ascii=False))
    sys.exit(0)

def extract_paths(tool_input):
    paths = []
    if isinstance(tool_input, dict):
        for key in ['file_path', 'path', 'target_file', 'filepath']:
            if isinstance(tool_input.get(key), str):
                paths.append(tool_input[key])
        if isinstance(tool_input.get('files'), list):
            for item in tool_input['files']:
                if isinstance(item, str):
                    paths.append(item)
                elif isinstance(item, dict):
                    for k in ['file_path', 'path']:
                        if isinstance(item.get(k), str):
                            paths.append(item[k])
    return paths

def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        respond('deny', 'Invalid hook input JSON')

    contract = load_contract()
    if contract is None:
        respond('deny', 'No active contract. Run the guarded task launcher first.')

    tool = event.get('tool_name', '')
    tool_input = event.get('tool_input', {})

    if tool not in contract.get('tools_allowed', []):
        log_event(event, 'deny', f'Tool not allowed: {tool}')
        respond('deny', f'Tool not allowed by contract: {tool}')

    for p in extract_paths(tool_input):
        if match_any_pattern(p, FORBIDDEN_PATH_PATTERNS):
            log_event(event, 'deny', f'Forbidden path: {p}')
            respond('deny', f'Forbidden path targeted: {p}')
        if tool in ['Edit', 'MultiEdit', 'Write'] and not in_scope(p, contract.get('files_in_scope', [])):
            log_event(event, 'deny', f'Write outside scope: {p}')
            respond('deny', f'Write outside approved scope: {p}')

    if tool == 'Bash':
        cmd = tool_input.get('command', '') if isinstance(tool_input, dict) else ''
        deny_regex = [re.compile(x) for x in contract.get('bash_deny_regex', [])]
        allow_regex = [re.compile(x) for x in contract.get('bash_allow_regex', [])]
        if any(r.search(cmd) for r in deny_regex):
            log_event(event, 'deny', f'Forbidden bash command: {cmd}')
            respond('deny', 'Forbidden shell command blocked by supervisor policy')
        if not any(r.search(cmd) for r in allow_regex):
            log_event(event, 'deny', f'Non-allowlisted bash command: {cmd}')
            respond('deny', 'Shell command is not on the allowlist')

    log_event(event, 'allow', 'Within policy')
    respond('allow', 'Within policy')

if __name__ == '__main__':
    main()
