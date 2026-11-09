"""Curated real B3/S23 symbolic patterns; cited at https://conwaylife.com/wiki/."""
from .core import parse_rle
RLES={
'pulsar': '''x = 13, y = 13, rule = B3/S23
2b3o3b3o$13b$o4bobo4bo$o4bobo4bo$o4bobo4bo$2b3o3b3o$13b$2b3o3b3o$o4bobo4bo$o4bobo4bo$o4bobo4bo$13b$2b3o3b3o!''',
'heart': '''x = 11, y = 11, rule = B3/S23
5bo$4bo2bo$bo2bo2bo$obobobob2o$bo2bo2bo$4bo5bo$5b5o2$7bo$6bobo$7bo!''',
'smiley': '''x = 7, y = 7, rule = B3/S23
3ob3o$bobobo2$bo3bo2$obobobo$2bobo!''',
'gosper_gun': '''x = 36, y = 9, rule = B3/S23
24bo11b$22bobo11b$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o14b$2o8bo3bob2o4bobo11b$10bo5bo7bo11b$11bo3bo20b$12b2o!''',
}
CATALOG={
'pulsar':{'period':3,'kind':'bounded oscillator','source':'https://conwaylife.com/wiki/Pulsar','lyric':'A million little points of light'},
'heart':{'period':5,'kind':'bounded oscillator','source':'https://conwaylife.com/wiki/Heart','lyric':'Like a heartbeat in my hand'},
'smiley':{'period':8,'kind':'bounded oscillator','source':'https://conwaylife.com/wiki/Smiley','lyric':'Look at me looking'},
'gosper_gun':{'period':30,'kind':'unbounded gun','source':'https://conwaylife.com/wiki/Gosper_glider_gun','lyric':'Little lightning running through a cloud'},
}
def pattern(name):
    return parse_rle(RLES[name])
