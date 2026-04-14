#!/usr/bin/env bash
set -euo pipefail

echo "[HOOK] triggered at $(date)" >> "$CLAUDE_PROJECT_DIR/.claude/hook.log"
