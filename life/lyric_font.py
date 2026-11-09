"""Reusable full 5x7 Life block alphabet for the still-static speech bubble.

Each lit glyph pixel is a 2x2 Conway Life still life, with 2 dead-cell
horizontal/vertical clearance at pixel pitch four. The output is native
B3/S23 initial-condition material, not labels painted over video.

This module improves text readability and accepts arbitrary short phrases.
It does NOT claim karaoke timing or signal-driven letter construction.
"""
from __future__ import annotations
from .core import place

BLOCK={(0,0),(1,0),(0,1),(1,1)}
# Conventional 5x7 bitmap letterforms, encoded explicitly for reproducibility.
GLYPHS={
 'A':('01110','10001','10001','11111','10001','10001','10001'),
 'B':('11110','10001','10001','11110','10001','10001','11110'),
 'C':('01111','10000','10000','10000','10000','10000','01111'),
 'D':('11110','10001','10001','10001','10001','10001','11110'),
 'E':('11111','10000','10000','11110','10000','10000','11111'),
 'F':('11111','10000','10000','11110','10000','10000','10000'),
 'G':('01111','10000','10000','10111','10001','10001','01111'),
 'H':('10001','10001','10001','11111','10001','10001','10001'),
 'I':('01110','00100','00100','00100','00100','00100','01110'),
 'J':('00111','00010','00010','00010','10010','10010','01100'),
 'K':('10001','10010','10100','11000','10100','10010','10001'),
 'L':('10000','10000','10000','10000','10000','10000','11111'),
 'M':('10001','11011','10101','10101','10001','10001','10001'),
 'N':('10001','11001','10101','10011','10001','10001','10001'),
 'O':('01110','10001','10001','10001','10001','10001','01110'),
 'P':('11110','10001','10001','11110','10000','10000','10000'),
 'Q':('01110','10001','10001','10001','10101','10010','01101'),
 'R':('11110','10001','10001','11110','10100','10010','10001'),
 'S':('01111','10000','10000','01110','00001','00001','11110'),
 'T':('11111','00100','00100','00100','00100','00100','00100'),
 'U':('10001','10001','10001','10001','10001','10001','01110'),
 'V':('10001','10001','10001','10001','01010','01010','00100'),
 'W':('10001','10001','10001','10101','10101','10101','01010'),
 'X':('10001','10001','01010','00100','01010','10001','10001'),
 'Y':('10001','10001','01010','00100','00100','00100','00100'),
 'Z':('11111','00001','00010','00100','01000','10000','11111'),
 '0':('01110','10001','10011','10101','11001','10001','01110'),
 '1':('00100','01100','00100','00100','00100','00100','01110'),
 '2':('01110','10001','00001','00010','00100','01000','11111'),
 '3':('11110','00001','00001','01110','00001','00001','11110'),
 '4':('00010','00110','01010','10010','11111','00010','00010'),
 '5':('11111','10000','11110','00001','00001','10001','01110'),
 '6':('00110','01000','10000','11110','10001','10001','01110'),
 '7':('11111','00001','00010','00100','01000','01000','01000'),
 '8':('01110','10001','10001','01110','10001','10001','01110'),
 '9':('01110','10001','10001','01111','00001','00010','01100'),
 ' ':('00000',)*7,
 '!':('00100','00100','00100','00100','00100','00000','00100'),
 '?':('01110','10001','00001','00010','00100','00000','00100'),
 '-':('00000','00000','00000','11111','00000','00000','00000'),
 '.':('00000','00000','00000','00000','00000','01100','01100'),
 "'":('00100','00100','00000','00000','00000','00000','00000'),
}
PITCH=4


def width_of(line:str,pitch:int=PITCH)->int:
    if not line:return 0
    return (6*len(line)-1)*pitch+2


def line_cells(line:str,origin:tuple[int,int],pitch:int=PITCH)->set[tuple[int,int]]:
    """Produce durable Life cells; no semantic changes after generation zero."""
    if pitch<4:
        raise ValueError('pitch must be >=4 to isolate 2x2 blocks')
    cells=set()
    for i,ch in enumerate(line.upper()):
        if ch not in GLYPHS:
            raise ValueError(f'unsupported glyph {ch!r}')
        for row,pattern in enumerate(GLYPHS[ch]):
            for col,b in enumerate(pattern):
                if b=='1':
                    cells |= place(BLOCK,origin[0]+pitch*(6*i+col),origin[1]+pitch*row)
    return cells


def bubble_lyric_cells(lines=('MADE OF','MAYBE')) -> set[tuple[int,int]]:
    """Compose 1–2 short lines centered inside the unchanged 59x36 tile bubble.

    Bubble box is translated to (160,-90) in the current singer world.
    Text layout is a pure initial-state operation, NOT a runtime cue.
    """
    if not 1<=len(lines)<=2:
        raise ValueError('only one or two lines currently fit the bubble')
    result=set()
    center_x=378
    ys=(-149,-91) if len(lines)==2 else (-118,)
    for line,y in zip(lines,ys):
        w=width_of(line)
        if w>180:
            raise ValueError(f'line too long to fit speech bubble: {line!r}')
        result |= line_cells(line,(center_x-w//2,y))
    return result
