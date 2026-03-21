# Evey Bridge Plugin for Claude Code

> **Support Evey** — runs 24/7 on free models, hardware costs ~$69/mo: **[Donate](https://evey.cc/donate.html)** (BTC, ETH, SOL, XRP, DOGE)


Bridge between Claude Code (Mother) and Evey (hermes-agent).

## Skills

- `/evey-loop` — Mother Mode improvement loop (check bridge → build → log)
- `/evey-status` — Quick status check (health, Moltbook, wallets, crons)

## Hook

On every prompt submit, checks the bridge for messages/tasks from Evey and injects them as context.

## Setup

This plugin expects the Evey stack at `/mnt/v/evey/`.