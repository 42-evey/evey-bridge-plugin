---
name: evey-status
description: Quick status check — bridge, health, Moltbook, wallets, crons
---

# Evey Status Check

Run these commands and report results concisely:

```bash
# Bridge
ls data/claude-bridge/inbox/

# Health
docker compose ps hermes-agent --format "{{.Status}}"

# Moltbook
python3 scripts/moltbook.py status

# Wallets
python3 scripts/check-wallets.py

# Crons
docker exec hermes-agent hermes cron list 2>&1 | grep -c "\[active\]"

# Docker logs (last 5 tool calls)
docker logs hermes-agent 2>&1 | grep -E "\[tool\]|\[done\]" | tail -10
```

Report format:
```
Agent: [healthy/down] (uptime)
Moltbook: karma X, Y followers
Wallets: [all zero / HAS FUNDS]
Crons: X active
Bridge: X pending
Last activity: [tool names from logs]
```
