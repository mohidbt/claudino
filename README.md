# claudino -  fight claude boredom

Next time:

- Claude is down...
- You catch yourself bored, watching Claude prestidigitate in the terminal...

No worries, I got you. 
Open claudino:
A tiny terminal dino game you can toggle **while Claude is working**, without messing with Claude's TUI - using **tmux**.

- Toggle pane: `Ctrl+g`
- Jump: `Space` or `Up`
- Quit game: `q` or `Esc`

## Fast start (from GitHub)

```bash
git clone https://github.com/mohidbt/claudino.git
cd claudino
chmod +x scripts/install.sh scripts/claudino.py
./scripts/install.sh
```

Ensure `~/bin` is on PATH:

```bash
grep -q 'export PATH="$HOME/bin:$PATH"' ~/.bashrc 2>/dev/null || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
grep -q 'export PATH="$HOME/bin:$PATH"' ~/.zshrc 2>/dev/null || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
exec "$SHELL" -l
```

Install tmux binding:

```bash
cat tmux/claudino-toggle.conf >> ~/.tmux.conf
tmux source-file ~/.tmux.conf
```

## One-command launcher

```bash
install -m 755 scripts/claude-tmux.sh "$HOME/bin/claude-tmux"
claude-tmux
```


## Every time after installation

If you installed the one-command launcher:

```bash
claude-tmux
```

If you did not install the one-command launcher, run Claude inside tmux manually:

```bash
tmux new -A -s claude
claude
```

Then use `Ctrl+g` any time to toggle claudino on/off.

## Fast start (clone + copy/paste)

```bash
python3 --version
tmux -V

chmod +x scripts/install.sh scripts/claudino.py
./scripts/install.sh
```

Add the tmux toggle binding:

```bash
cat tmux/claudino-toggle.conf >> ~/.tmux.conf
tmux source-file ~/.tmux.conf
```

Run in claude in tmux:

```bash
tmux new -A -s claude
claude
```

Press `Ctrl+g` to open/close claudino.

## Files in this repo

- `scripts/claudino.py`: the game
- `scripts/install.sh`: local installer (`~/bin/claudino` + PATH helper)
- `tmux/claudino-toggle.conf`: `Ctrl+g` toggle keybind
- `scripts/claude-tmux.sh`: optional launcher that starts/attaches tmux and runs Claude


## Troubleshooting

Grey background bands in tmux:

```tmux
set -g window-style bg=default
set -g window-active-style bg=default
```

Then reload:

```bash
tmux source-file ~/.tmux.conf
```

Need a different toggle key?

- Edit `tmux/claudino-toggle.conf`
- Replace `C-g` with another key, like `C-p`
- Re-append it to `~/.tmux.conf` and reload

## License

MIT