#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$HOME/bin"
install -m 755 "$ROOT_DIR/scripts/claudino.py" "$HOME/bin/claudino"

for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
  touch "$rc"
  if ! grep -qxF 'export PATH="$HOME/bin:$PATH"' "$rc"; then
    echo 'export PATH="$HOME/bin:$PATH"' >> "$rc"
  fi
done

echo "Installed: $HOME/bin/claudino"
echo 'Reload shell with: exec "$SHELL" -l'
echo "Then run: claudino"
