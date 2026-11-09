"""Small reference Conway Game of Life simulator with no external dependencies."""
from collections import Counter
import re


def parse_rle(data):
    body = "".join(line.strip() for line in data.splitlines()
                   if line.strip() and not line.lstrip().startswith(("#", "x =")))
    cells = set()
    x = y = 0
    for match in re.finditer(r"(\d*)([ob$!])", body):
        n = int(match.group(1) or 1)
        op = match.group(2)
        if op == "o":
            cells.update((x + i, y) for i in range(n))
            x += n
        elif op == "b":
            x += n
        elif op == "$":
            y += n
            x = 0
        else:
            break
    return cells


def evolve(cells):
    counts = Counter((x + dx, y + dy) for x, y in cells
                     for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                     if dx or dy)
    return {p for p, n in counts.items() if n == 3 or (n == 2 and p in cells)}


def place(cells, dx, dy):
    return {(x + dx, y + dy) for x, y in cells}


def encode_rle(cells, comments=()):
    if not cells:
        return "x = 0, y = 0, rule = B3/S23\n!\n"
    left, right = min(x for x, _ in cells), max(x for x, _ in cells)
    top, bottom = min(y for _, y in cells), max(y for _, y in cells)
    lines = ["".join("o" if (x, y) in cells else "b"
                     for x in range(left, right + 1)).rstrip("b")
             for y in range(top, bottom + 1)]
    body = "$".join(lines) + "!"
    return ("".join("#C " + c + "\n" for c in comments)
            + f"x = {right-left+1}, y = {bottom-top+1}, rule = B3/S23\n"
            + "\n".join(body[i:i + 70] for i in range(0, len(body), 70)) + "\n")
