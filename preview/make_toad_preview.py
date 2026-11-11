"""Render native Toad mouth states from *actual* B3/S23 generations.

Requires Pillow: python -m pip install Pillow
Run: python preview/make_toad_preview.py
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw
from life.core import evolve
from life.toad_mouth_study import initial,FACE

OUT=Path(__file__).resolve().parent

def draw(cells):
    scale=20; left=-15; top=-15
    image=Image.new('RGB',(640,620),(9,15,27))
    pen=ImageDraw.Draw(image)
    for x,y in cells:
        X=(x-left)*scale
        Y=(y-top)*scale
        pen.rectangle((X,Y,X+scale-2,Y+scale-2),fill=(218,246,238))
    return image

a=initial()
b=evolve(a)
assert evolve(b)==a
closed=draw(a)
opened=draw(b)
closed.save(OUT/'toad_band.png')
opened.save(OUT/'toad_open.png')
joined=Image.new('RGB',(1300,620),(14,20,34))
joined.paste(closed,(0,0))
joined.paste(opened,(660,0))
joined.save(OUT/'toad_mouth_compare.png')
frames=[]
s=a
for _ in range(12):
    frames.append(draw(s).resize((320,310)))
    s=evolve(s)
frames[0].save(OUT/'toad_mouth_natural_oscillator.gif',
               save_all=True,append_images=frames[1:],
               duration=370,loop=0,optimize=True)
