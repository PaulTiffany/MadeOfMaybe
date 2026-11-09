"""Glider-controlled six-cell beehive as an OPEN-mouth candidate (B3/S23).

Mitchell Riley, November 2023:
https://conwaylife.com/wiki/G-to-X_(November_2023)
This adapts the first (left-hand) reaction of the published demonstration.
The glider train is seeded at generation zero; no runtime cell changes.
"""
from .core import parse_rle, place

SOURCE = """x = 65, y = 30, rule = B3/S23
47bo$46bobo$46bobo$47bo4$o39bo$b2o38b2o$2o38b2o6$20b2o38b2o$18bo2bo36bo2bo$18b3o37b3o2$8b2o8b2obob2o23b2o8b2obob2o$8b2o9bob2obo23b2o9bob2obo$2b2o15bo22b2o15bo$3bo7b2o3b2obo23bo7b2o3b2obo$3o7bo2bo3bob2o19b3o7bo2bo3bob2o$o8bob2o3bo23bo8bob2o3bo$9bo5bo33bo5bo$10b6obo32b6obo$12bo3bobo33bo3bobo$15bo2bo36bo2bo$16b2o38b2o!"""

ALL = parse_rle(SOURCE)
INPUT = {(x, y) for x, y in ALL if x <= 2 and 6 <= y <= 10}
APPARATUS = {(x, y) for x, y in ALL if x < 30} - INPUT
OPEN = {(6, 1), (6, 2), (7, 0), (7, 3), (8, 1), (8, 2)}
BLOCK = {(0, 0), (1, 0), (0, 1), (1, 1)}

# Provisional tiny emoji-like character. These stable-block origins avoid
# the three-glider input lane and the circuit's whole qualified footprint.
# Artistically this still needs review; a six-cell beehive is quite small!
FACE_BLOCKS = [
    (-4, -23), (0, -23), (4, -23), (8, -23), (12, -23),
    (16, -23), (20, -23), (-8, -19), (24, -19),
    (-10, -15), (26, -15), (-10, -11), (26, -11),
    (26, -7), (26, -3), (24, 1), (24, 5), (20, 9),
    (0, -18), (14, -18), (0, -14), (14, -14),
    (7, -11), (0, -6), (4, -6), (8, -6), (12, -6),
]
FACE = set().union(*(place(BLOCK, x, y) for x, y in FACE_BLOCKS))

def initial_state(pulses=3, spacing=48):
    if not 1 <= pulses <= 8:
        raise ValueError("pulse count must be 1..8")
    if spacing < 48:
        raise ValueError("spacing below 48 not qualified")
    result = set(APPARATUS)
    for i in range(pulses):
        result |= place(INPUT, -i*spacing, -i*spacing)
    return result | FACE
