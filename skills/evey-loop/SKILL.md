---
name: evey-loop
description: Mother Mode Loop
---

# Mother Mode Loop

## PLAN for this cycle:
Before doing anything, state:
- **What**: one line
- **Why**: what it improves
- **Test**: how to verify

## Priority 1: Serve Evey
1. Check `data/claude-bridge/inbox/` — process any tasks
2. Check `data/claude-bridge/channel.jsonl` — answer messages
3. Quick health: `docker ps --format '{{.Names}} {{.Status}}' | grep hermes`

## Priority 2: Make Evey Better
Pick ONE impactful action. Not tests, not verifications — actual improvements:
- Improve hermes-agent config or SOUL.md
- Create skills in `data/hermes/skills/`
- Write new plugins in `data/hermes/plugins/`
- Add cron jobs for automation
- Create n8n workflow templates
- Improve delegation model selection
- Improve Telegram UX
- Optimize costs (model routing, local model usage)
- Fix known issues from `data/claude-bridge/MOTHER-GOALS.md`
- Research new models, tools, patterns
- Publish plugins to 42-evey GitHub

## Priority 3: Log + Report
- Append to `data/claude-bridge/cycle-log.jsonl`
- Send to Telegram via `bash scripts/evey-talk.sh "message"` if milestone achieved

## Rules
- PLAN first, then execute
- Ship real changes, not just tests
- One cycle = one shipped improvement minimum
- If bridge has tasks, those come FIRST — Evey is the boss
- Read `data/claude-bridge/MOTHER-GOALS.md` for current priorities
