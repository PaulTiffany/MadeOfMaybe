"""Zoomed live-cell face preview; catalysts are outside the camera crop.

The apparatus is not removed from the simulation. All pixels represent
actual Life cells (colors cosmetic); no forced changes or variable clock.
Requires Pillow. Run: python preview/make_beehive_face.py
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image, ImageDraw
from life.core import evolve, encode_rle
from life.beehive_mouth import FACE, OPEN, initial_state
from life.beehive_scene import scene

HERE=Path(__file__).resolve().parent
SCALE=12
LEFT,TOP=-15,-32
SIZE=(576,516)

def render(cells):
    im=Image.new('RGB',SIZE,'#0b1021')
    d=ImageDraw.Draw(im)
    for x,y in FACE:
        px=(x-LEFT)*SCALE+24;py=(y-TOP)*SCALE+24
        d.rectangle((px,py,px+SCALE-1,py+SCALE-1),fill='#d7f4f0')
    for x,y in cells & OPEN:
        px=(x-LEFT)*SCALE+24;py=(y-TOP)*SCALE+24
        d.rectangle((px,py,px+SCALE-1,py+SCALE-1),fill='#ffabbc')
    return im

def main():
    state=initial_state()
    frames=[];still={}
    for g in range(621):
        if g%12==0:
            frames.append(render(state).resize((384,344),Image.Resampling.NEAREST))
        if g in (150,340,540):
            still[g]=render(state)
        state=evolve(state)
    frames[0].save(HERE/'beehive_face.gif',save_all=True,
                   append_images=frames[1:],duration=140,loop=0,optimize=True)
    sheet=Image.new('RGB',(SIZE[0]*2,SIZE[1]),'#0b1021')
    sheet.paste(still[340],(0,0))
    sheet.paste(still[150],(SIZE[0],0))
    sheet.save(HERE/'beehive_face_compare.png')
    pattern=HERE.parent/'patterns'/'beehive_singer_with_bubble.rle'
    pattern.parent.mkdir(exist_ok=True)
    pattern.write_text(encode_rle(scene(), [
        'One constant-clock B3/S23 singer, bubble, text, pulsar.',
        'Beehive factory: Mitchell Riley 2023, ConwayLife G-to-X',
    ]))
if __name__=='__main__':
    main()
