# claudino - fight claude boredom

The next time:
- Claude is down...
- You catch yourself bored, following it Prestidigitating in the terminal...

No worries, I got you. 
Open claudino:
A tiny terminal dino game you can toggle **while Claude is working**, without messing with Claude’s TUI - using **tmux**.

- Toggle game pane: **Ctrl+g**
- Game controls: **Space / ↑** jump, **q** or **Esc** quit

---

## Requirements

- `python3`
- `tmux`

Check:
```bash
python3 --version
tmux -V
````

---

## Install claudino

### 1) Create the executable

```bash
mkdir -p ~/bin

cat > ~/bin/claudino <<'EOF'
#!/usr/bin/env python3
import curses, time, random

TICK = 0.05

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    # --- background fix (prevents tmux grey bands) ---
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, -1, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.clear()
    # -----------------------------------------------

    h, w = stdscr.getmaxyx()
    ground_y = h - 3
    player_x = 6
    y = ground_y
    vy = 0.0
    gravity = 0.9
    jump_v = -8.5

    obstacles = []
    score = 0
    speed = 1.0
    last_spawn = 0

    while True:
        h, w = stdscr.getmaxyx()
        ground_y = h - 3

        ch = stdscr.getch()
        if ch in (ord('q'), 27):  # q or ESC
            break
        if ch in (ord(' '), ord('w'), curses.KEY_UP):
            if y >= ground_y:
                vy = jump_v

        # physics
        vy += gravity
        y += vy * 0.25
        if y > ground_y:
            y = ground_y
            vy = 0.0

        # spawn obstacles
        now = time.time()
        if now - last_spawn > max(0.6, 1.2 - speed * 0.1):
            if random.random() < 0.8:
                obstacles.append([w - 2, ground_y, 1])      # cactus
            else:
                obstacles.append([w - 2, ground_y - 2, 2])  # bird
            last_spawn = now

        # move obstacles
        for o in obstacles:
            o[0] -= max(1, int(1 + speed))
        obstacles = [o for o in obstacles if o[0] + o[2] > 0]

        # collision
        py = int(round(y))
        for ox, oy, ow in obstacles:
            hit_x = (player_x in range(ox, ox + ow)) or ((player_x + 1) in range(ox, ox + ow))
            hit_y = abs(py - oy) <= 0
            if hit_x and hit_y:
                stdscr.nodelay(False)
                stdscr.addstr(1, 2, f"GAME OVER — score {score}. Press r to restart, q to quit.")
                while True:
                    c = stdscr.getch()
                    if c in (ord('q'), 27):
                        return
                    if c == ord('r'):
                        obstacles.clear()
                        score = 0
                        speed = 1.0
                        y = ground_y
                        vy = 0.0
                        stdscr.nodelay(True)
                        break

        # draw
        stdscr.erase()
        stdscr.addstr(0, 2, "claudino — Space/↑ jump, q quit, ESC quit")
        stdscr.addstr(0, max(0, w - 20), f"Score {score:6d}")

        # ground
        stdscr.hline(ground_y + 1, 0, ord('-'), w)

        # player
        dino = ["  __", " (oo)", "/|/\\"]
        px_y = max(1, int(py) - 2)
        for i, line in enumerate(dino):
            if 0 <= px_y + i < h:
                stdscr.addstr(px_y + i, player_x, line[: max(0, w - player_x - 1)])

        # obstacles
        for ox, oy, ow in obstacles:
            if 0 <= oy < h and 0 <= ox < w:
                stdscr.addstr(oy, ox, "#" * ow)

        stdscr.refresh()

        score += 1
        speed = min(6.0, 1.0 + score / 800.0)
        time.sleep(TICK)

if __name__ == "__main__":
    curses.wrapper(main)
EOF

chmod +x ~/bin/claudino
```

### 2) Ensure `~/bin` is on PATH

```bash
grep -q 'export PATH="$HOME/bin:$PATH"' ~/.bashrc 2>/dev/null || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
grep -q 'export PATH="$HOME/bin:$PATH"' ~/.zshrc  2>/dev/null || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
exec "$SHELL" -l
```

### 3) Quick test

```bash
command -v claudino
claudino
```

Press `q` to exit.

---

## Add tmux toggle shortcut (Ctrl+g)

Append this to `~/.tmux.conf`:

```bash
cat >> ~/.tmux.conf <<'EOF'

# Ctrl+g toggles a bottom pane running claudino
bind-key -n C-g run-shell ' \
  if tmux list-panes -F "#{pane_id} #{pane_title}" | grep -q " claudino$"; then \
    pid="$(tmux list-panes -F "#{pane_id} #{pane_title}" | awk "/ claudino$/{print \$1; exit}")"; \
    tmux kill-pane -t "$pid"; \
  else \
    tmux split-window -v -l 12 -c "#{pane_current_path}" "bash -lc claudino"; \
    tmux select-pane -T claudino -t :.+; \
  fi'
EOF
```

Reload tmux:

```bash
tmux source-file ~/.tmux.conf
```

---

## Run Claude Code inside tmux

Start (or attach) a tmux session:

```bash
tmux new -A -s claude
```

Inside tmux, start Claude:

```bash
claude
```

While it’s running:

* Press **Ctrl+g** → opens claudino in a bottom pane
* Press **Ctrl+g** again → closes the pane

---

If `claude` is not installed yet, install and authenticate first:

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude auth login
```

---

## Optional: one-command launcher (auto-start Claude Code)

Create `~/bin/claude-tmux`:

```bash
cat > ~/bin/claude-tmux <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

if tmux has-session -t claude 2>/dev/null; then
  exec tmux attach -t claude
fi

tmux new-session -d -s claude -n main "bash -lc 'claude'"
tmux attach -t claude
EOF

chmod +x ~/bin/claude-tmux
```

Run:

```bash
claude-tmux
```

---

## Troubleshooting

### Grey shaded bands still appear

Some terminal themes treat “black” differently. Try making tmux panes use your terminal default background:

Add to `~/.tmux.conf`:

```tmux
set -g window-style bg=default
set -g window-active-style bg=default
```

Reload:

```bash
tmux source-file ~/.tmux.conf
```

### Ctrl+g conflicts with something

Pick another key (example: Ctrl+p). Replace `C-g` with `C-p` in `~/.tmux.conf`, then reload.

---

## Notes

* This approach avoids injecting into Claude’s terminal stream.
* claudino runs in its own tmux pane, so Claude’s UI remains stable.

```
