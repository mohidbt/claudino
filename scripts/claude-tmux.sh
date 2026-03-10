#!/usr/bin/env bash
set -euo pipefail

if tmux has-session -t claude 2>/dev/null; then
  exec tmux attach -t claude
fi

tmux new-session -d -s claude -n main "bash -lc 'claude'"
tmux attach -t claude
