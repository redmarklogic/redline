"""Probe cce.exe serve as an MCP stdio server: time the handshake, list tools.

Reproduces what Claude Code does at session start. Distinguishes 'binary
unreachable' from 'too slow' from 'protocol error'.
"""
import json
import shutil
import subprocess
import sys
import time
import threading
from pathlib import Path

PROJ = Path(__file__).resolve().parents[2]   # repo root (tasks/tests/probe → root)
CCE = shutil.which("cce") or r"C:\Users\harel\.local\bin\cce.exe"
TIMEOUT = 120


def rpc(id_, method, params):
    return (json.dumps({"jsonrpc": "2.0", "id": id_, "method": method,
                        "params": params}) + "\n").encode()


def main():
    t0 = time.time()
    p = subprocess.Popen([CCE, "serve", "--project-dir", str(PROJ)],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, cwd=PROJ)
    stderr_buf = []
    threading.Thread(target=lambda: stderr_buf.extend(p.stderr),
                     daemon=True).start()

    p.stdin.write(rpc(1, "initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "probe", "version": "0"}}))
    p.stdin.flush()

    line = None
    deadline = time.time() + TIMEOUT
    while time.time() < deadline:
        line = p.stdout.readline()
        if line:
            break
        if p.poll() is not None:
            print(f"SERVER EXITED rc={p.returncode} after {time.time()-t0:.1f}s")
            print(b"".join(stderr_buf[-30:]).decode(errors="replace"))
            return 1
    if not line:
        print(f"NO RESPONSE within {TIMEOUT}s")
        p.kill()
        return 1

    t_init = time.time() - t0
    resp = json.loads(line)
    info = resp.get("result", {}).get("serverInfo", {})
    print(f"initialize OK in {t_init:.1f}s  server={info.get('name')} {info.get('version')}")

    p.stdin.write((json.dumps({"jsonrpc": "2.0", "method":
                               "notifications/initialized"}) + "\n").encode())
    p.stdin.write(rpc(2, "tools/list", {}))
    p.stdin.flush()
    line = p.stdout.readline()
    t_tools = time.time() - t0
    tools = json.loads(line).get("result", {}).get("tools", [])
    print(f"tools/list OK in {t_tools:.1f}s — {len(tools)} tools:")
    for t in tools:
        desc = (t.get("description") or "").split("\n")[0][:80]
        print(f"  {t['name']:24s} {desc}")

    # one real search to time a query end-to-end
    p.stdin.write(rpc(3, "tools/call", {
        "name": "context_search",
        "arguments": {"query": "cloud run deployment terraform configuration"}}))
    p.stdin.flush()
    line = p.stdout.readline()
    t_q = time.time() - t0
    r = json.loads(line)
    content = r.get("result", {}).get("content", [])
    text = (content[0].get("text", "") if content else "")[:400]
    print(f"\ncontext_search OK in {t_q - t_tools:.1f}s, result preview:")
    print(text)
    p.kill()
    return 0


if __name__ == "__main__":
    sys.exit(main())
