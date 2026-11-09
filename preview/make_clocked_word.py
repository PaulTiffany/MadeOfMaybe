"""Verify/render real Life word construction on the faster audio clock.

Projection is strictly from actually completed 2x2 Life output blocks.
No text is inserted into the universe or frame-swapped. Control gliders
remain in the real simulation even though this camera excludes their lanes.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import evolve
from life.lyric_clock import plan_we,physical_initial,physical_targets,retimed_routes

OUT=Path(__file__).resolve().parent
try:
    HEAD=ImageFont.truetype('DejaVuSans-Bold.ttf',27)
    SUB=ImageFont.truetype('DejaVuSans.ttf',17)
except OSError:
    HEAD=SUB=ImageFont.load_default()
BG='#0b1424';MUTED='#92a7bc';LIT='#8cf1c8';FG='#e5ecf5'
PLAN=plan_we(192)
PITCH=160
ROUTES=retimed_routes(PLAN)
TARGETS=physical_targets(PLAN,PITCH)
SAMPLES=[PLAN.first_make-1,PLAN.first_make,PLAN.make_at,
         PLAN.make_at+24,PLAN.first_erase,PLAN.erase_by]
FRAMES=set(SAMPLES)|set(range(2050,2610,8))


def render(g,alive):
    im=Image.new('RGB',(780,470),BG);d=ImageDraw.Draw(im)
    d.text((35,22),'MADE OF MAYBE  ·  LYRIC ACTUATOR',font=HEAD,fill=FG)
    d.text((35,65),f'Song at normal speed  ·  Life at 192 generations/audio-second',
           font=SUB,fill=MUTED)
    count=0
    for r,target in zip(ROUTES,TARGETS):
        if target <= alive:
            count+=1
            x=130+(r.x//20)*45
            y=123+(r.y//20)*39
            d.rounded_rectangle((x,y,x+33,y+32),radius=4,fill=LIT)
    d.line((35,408,747,408),fill='#36465a',width=1)
    d.text((36,420),f'g{g:04d}   ·   {g/PLAN.gps:06.3f}s   ·   actual 2×2 blocks: {count}/35',
           font=SUB,fill=FG)
    d.text((36,446),'No speech bubble; glider traffic continues outside this text viewport.',
           font=SUB,fill=MUTED)
    return im


def main():
    cells=physical_initial(PLAN,PITCH)
    imgs={};frames=[]
    for g in range(max(FRAMES)+1):
        if g in FRAMES:
            img=render(g,cells)
            if g in SAMPLES:imgs[g]=img
            if 2050<=g<=2610:frames.append(img)
        if g<max(FRAMES):cells=evolve(cells)
    contact=Image.new('RGB',(780*3,470*2),BG)
    for i,g in enumerate(SAMPLES):
        contact.paste(imgs[g],((i%3)*780,(i//3)*470))
    contact.save(OUT/'clocked_we_six_checkpoints.png',optimize=True)
    frames[0].save(OUT/'clocked_we_192_life.gif',save_all=True,
                   append_images=frames[1:],duration=80,loop=0,optimize=True)
    print('Exported exact native-Life word timing at 8× nominal clock')

if __name__=='__main__':main()
