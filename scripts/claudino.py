#!/usr/bin/env python3
import curses
import random
import time

TICK = 0.05


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    # Prevent tmux grey background bands on some themes.
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, -1, curses.COLOR_BLACK)
    stdscr.bkgd(" ", curses.color_pair(1))
    stdscr.clear()

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
    last_spawn = 0.0

    while True:
        h, w = stdscr.getmaxyx()
        ground_y = h - 3

        ch = stdscr.getch()
        if ch in (ord("q"), 27):  # q or ESC
            break
        if ch in (ord(" "), ord("w"), curses.KEY_UP):
            if y >= ground_y:
                vy = jump_v

        vy += gravity
        y += vy * 0.25
        if y > ground_y:
            y = ground_y
            vy = 0.0

        now = time.time()
        if now - last_spawn > max(0.6, 1.2 - speed * 0.1):
            if random.random() < 0.8:
                obstacles.append([w - 2, ground_y, 1])  # cactus
            else:
                obstacles.append([w - 2, ground_y - 2, 2])  # bird
            last_spawn = now

        for obstacle in obstacles:
            obstacle[0] -= max(1, int(1 + speed))
        obstacles = [o for o in obstacles if o[0] + o[2] > 0]

        py = int(round(y))
        for ox, oy, ow in obstacles:
            hit_x = (player_x in range(ox, ox + ow)) or ((player_x + 1) in range(ox, ox + ow))
            hit_y = abs(py - oy) <= 0
            if hit_x and hit_y:
                stdscr.nodelay(False)
                stdscr.addstr(1, 2, f"GAME OVER - score {score}. Press r to restart, q to quit.")
                while True:
                    c = stdscr.getch()
                    if c in (ord("q"), 27):
                        return
                    if c == ord("r"):
                        obstacles.clear()
                        score = 0
                        speed = 1.0
                        y = ground_y
                        vy = 0.0
                        stdscr.nodelay(True)
                        break

        stdscr.erase()
        stdscr.addstr(0, 2, "claudino - Space/Up jump, q quit, ESC quit")
        stdscr.addstr(0, max(0, w - 20), f"Score {score:6d}")

        stdscr.hline(ground_y + 1, 0, ord("-"), w)

        dino = ["  __", " (oo)", "/|/\\"]
        px_y = max(1, py - 2)
        for i, line in enumerate(dino):
            if 0 <= px_y + i < h:
                stdscr.addstr(px_y + i, player_x, line[: max(0, w - player_x - 1)])

        for ox, oy, ow in obstacles:
            if 0 <= oy < h and 0 <= ox < w:
                stdscr.addstr(oy, ox, "#" * ow)

        stdscr.refresh()
        score += 1
        speed = min(6.0, 1.0 + score / 800.0)
        time.sleep(TICK)


if __name__ == "__main__":
    curses.wrapper(main)
