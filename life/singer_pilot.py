"""Real Life signal-controlled block with a rudimentary stable-cell face.

This is NOT a paused Smiley. Glider pulses toggle one stable block without
pausing the simulation or modifying any cells after the initial generation.
Source: Luke Kiernan, Oct 2023: https://conwaylife.com/wiki/Glider_to_block
"""
from .core import parse_rle, place

SOURCE_RLE = """x = 38, y = 34, rule = B3/S23
bo$2bo$3o5$36b2o$35bobo$35bo$26b2o6b2obo$26b2o4bo3b2o$32b3o$35b3o$32b3o2bo$31bo2bobo$32b2o2b2o$33bobo$33bobo$34bo4$20b2o5b2o$19bo2bo4bobo$15b2o3bobo6bo$14bobo4bo7b2o$14bo9b2o$12bob2o8bo$11bobo11b3o$11bo2b2o11bo$12bobo$11b2o2bo$14b2o!
"""

INPUT_GLIDER = parse_rle("bo$2bo$3o!")
APPARATUS = parse_rle(SOURCE_RLE) - INPUT_GLIDER
MOUTH_BLOCK = {(11, 14), (12, 14), (11, 15), (12, 15)}

FACE_BLOCK_ORIGINS = {
    "left_eye": (1, -10), "right_eye": (21, -10),
    "left_brow": (0, -15), "right_brow": (20, -15),
    "nose": (11, -1), "left_cheek": (-6, 7),
    "top_hair": (11, -21), "right_hair": (30, -15),
}


def face_cells():
    block = {(0, 0), (0, 1), (1, 0), (1, 1)}
    return set().union(*(place(block, x, y)
                         for x, y in FACE_BLOCK_ORIGINS.values()))


def initial_state(pulses=3, spacing=48, face=True):
    if not 1 <= pulses <= 8:
        raise ValueError("pulses must be between 1 and 8")
    if spacing < 32:
        raise ValueError("spacing < 32 is not qualified")
    state = APPARATUS | (face_cells() if face else set())
    for i in range(pulses):
        state |= place(INPUT_GLIDER, -i * spacing, -i * spacing)
    return state
