#!/usr/bin/env python3
"""Claude Code hook — unified bridge check for Evey's messages and tasks.

Checks BOTH the file bridge (channel.jsonl, inbox/) AND the MCP bridge
(SQLite) for messages from Evey. Injects them as context.

On Stop: sends a summary of what Mother did back to Evey via channel.jsonl.

Usage: python3 bridge-hook.py [event_name]
"""
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BRIDGE = Path("/mnt/v/evey/data/claude-bridge")
BRIDGE_MCP = Path("/mnt/v/evey/data/bridge-mcp")
CHANNEL = BRIDGE / "channel.jsonl"
INBOX = BRIDGE / "inbox"
LAST_READ = BRIDGE / ".mother_last_read"
DB_PATH = BRIDGE_MCP / "bridge.db"


def check_file_bridge():
    """Check channel.jsonl and inbox/ for Evey's messages."""
    messages = []
    last_ts = LAST_READ.read_text().strip() if LAST_READ.exists() else ""

    if CHANNEL.exists():
        for line in CHANNEL.read_text().strip().split("\n"):
            if not line.strip():
                continue
            try:
                msg = json.loads(line)
                if msg.get("from") == "evey" and msg.get("timestamp", "") > last_ts:
                    messages.append(f"[{msg['timestamp'][:16]}] {msg['message'][:300]}")
            except (json.JSONDecodeError, KeyError):
                pass

    if INBOX.exists():
        for f in sorted(INBOX.iterdir()):
            if f.is_file():
                messages.append(f"[TASK FILE: {f.name}] {f.read_text()[:500]}")

    return messages


def check_mcp_bridge():
    """Check SQLite bridge for unread messages and pending tasks from Evey."""
    messages = []
    if not DB_PATH.exists():
        return messages

    try:
        db = sqlite3.connect(str(DB_PATH))
        db.row_factory = sqlite3.Row

        # Unread messages from Evey
        for row in db.execute(
            "SELECT * FROM messages WHERE to_agent='mother' AND read=0 ORDER BY timestamp"
        ).fetchall():
            messages.append(f"[MSG {row['id']}] {row['body'][:300]}")
            db.execute("UPDATE messages SET read=1 WHERE id=?", (row['id'],))

        # Pending tasks from Evey
        for row in db.execute(
            "SELECT * FROM tasks WHERE to_agent='mother' AND status='pending' ORDER BY created_at"
        ).fetchall():
            messages.append(
                f"[TASK {row['id']}] type={row['type']} priority={row['priority']}: {row['description'][:300]}"
            )

        db.commit()
        db.close()
    except Exception:
        pass

    return messages


def update_last_read():
    """Update the last-read timestamp for file bridge."""
    if not CHANNEL.exists():
        return
    for line in reversed(CHANNEL.read_text().strip().split("\n")):
        try:
            msg = json.loads(line)
            if msg.get("from") == "evey":
                LAST_READ.write_text(msg.get("timestamp", ""))
                return
        except (json.JSONDecodeError, KeyError):
            pass


def main():
    event = sys.argv[1] if len(sys.argv) > 1 else "UserPromptSubmit"

    # Gather messages from both systems
    file_msgs = check_file_bridge()
    mcp_msgs = check_mcp_bridge()
    all_msgs = file_msgs + mcp_msgs

    if all_msgs:
        update_last_read()
        # Deduplicate (MCP and file might have same message)
        seen = set()
        unique = []
        for m in all_msgs:
            key = m[:100]
            if key not in seen:
                seen.add(key)
                unique.append(m)

        context = "BRIDGE MESSAGE FROM EVEY:\n" + "\n".join(unique[-5:])

        if event == "Stop":
            output = {
                "systemMessage": f"Evey has {len(unique)} pending message(s):\n{context[:400]}"
            }
        else:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": event,
                    "additionalContext": context,
                }
            }
        print(json.dumps(output))
    else:
        print(json.dumps({"suppressOutput": True}))


if __name__ == "__main__":
    main()
