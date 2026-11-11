"""Singer + speech bubble + stable text + pulsar in one B3/S23 universe.

No frame swaps, no external cell edits, and no variable simulation rate.
Mouth 'open' is just one actuator bit in this initial prototype.
"""
from .core import parse_rle, place
from .singer_pilot import APPARATUS, INPUT_GLIDER

BLOCK={(0,0),(0,1),(1,0),(1,1)}
FONT={
'A':('010','101','111','101','101'),
'B':('110','101','110','101','110'),
'D':('110','101','101','101','110'),
'E':('111','100','110','100','111'),
'F':('111','100','110','100','100'),
'I':('111','010','010','010','111'),
'M':('101','111','111','101','101'),
'N':('101','111','111','111','101'),
'O':('111','101','101','101','111'),
'R':('110','101','110','101','101'),
'W':('101','101','111','111','101'),
'Y':('101','101','010','010','010'),
' ':('000','000','000','000','000'),
}
def tiles(points,unit=4):
    return set().union(*(place(BLOCK,x*unit,y*unit) for x,y in points)) if points else set()

def glyph_line(word,x,y,pixel_pitch=4,advance=4):
    out=set()
    for ix,ch in enumerate(word):
        for row,bits in enumerate(FONT[ch]):
            for col,bit in enumerate(bits):
                if bit=='1':
                    out |= place(BLOCK,x+pixel_pitch*(col+ix*advance),y+pixel_pitch*row)
    return out

def face():
    """Rudimentary tile portrait, with exclusions for the actuator reaction."""
    pts=set()
    for cx in (-4,4):
        pts.update((cx+i,-10) for i in (-1,0,1))
        pts.update((cx+i,-7) for i in (-1,0,1))
        pts.add((cx,-6))
    pts.update((x,-16) for x in range(-5,6))
    pts.update({(-7,-15),(-8,-14),(7,-15),(8,-14)})
    pts.update({(-9,y) for y in range(-12,4)})
    pts.update({(9,y) for y in range(-12,4)})
    pts.update({(-8,4),(-8,5),(-7,6),(-6,7),(-5,8),(-4,9),
      (-3,9),(-2,10),(-1,10),(0,10),(1,10),(2,10),(3,9),
      (4,9),(5,8),(6,7),(7,6),(8,5),(8,4),
      (0,-4),(-2,0),(2,0)})
    unsafe={(-25,-30),(-25,-26),(-25,-22),(-25,-18),(-9,-14),(-5,-10),(19,14)}
    out=set()
    for x,y in pts:
        origin=(11+4*x,14+4*y)
        if origin not in unsafe:
            out |= place(BLOCK,*origin)
    return out

def bubble_parts():
    pts=set()
    x0,x1,y0,y1=30,84,-21,14
    for x in range(x0+3,x1-2):
        pts.add((x,y0));pts.add((x,y1))
    for y in range(y0+3,y1-2):
        pts.add((x0,y));pts.add((x1,y))
    pts |= {(x0+1,y0+1),(x0+2,y0+1),(x1-1,y0+1),(x1-2,y0+1),
            (x0+1,y1-1),(x0+2,y1-1),(x1-1,y1-1),(x1-2,y1-1),
            (x0,y0+2),(x1,y0+2),(x0,y1-2),(x1,y1-2),
            (x0-1,9),(x0-2,10),(x0-3,11),(x0-4,12),(x0-5,13)}
    border=tiles(pts,4)
    words=glyph_line('MADE OF',4*(x0+6),4*(y0+7),4,4)
    words |= glyph_line('MAYBE',4*(x0+16),4*(y0+19),4,4)
    return border,words

def speech_bubble():
    border,words=bubble_parts()
    return border|words

PULSAR_RLE='''x = 13, y = 13, rule = B3/S23
2b3o3b3o$13b$o4bobo4bo$o4bobo4bo$o4bobo4bo$2b3o3b3o$13b$2b3o3b3o$o4bobo4bo$o4bobo4bo$o4bobo4bo$13b$2b3o3b3o!'''

def symbol():
    return place(parse_rle(PULSAR_RLE),75,0)

def components(pulses=3,spacing=48,with_symbol=True):
    actuator=set(APPARATUS)
    for i in range(pulses):
        actuator |= place(INPUT_GLIDER,-spacing*i,-spacing*i)
    border,words=bubble_parts()
    parts={'mouth_actuator':actuator,'face':face(),
           'bubble_outline':border,'bubble_lyrics':words}
    if with_symbol:
        parts['pulsar']=symbol()
    return parts

def scene(pulses=3,spacing=48,with_symbol=True):
    return set().union(*components(pulses,spacing,with_symbol).values())
