"""Render genuine B3/S23 glider-written 5x7 WE; no simulated glyph overlays.

For artistic legibility, the RIGHT viewport maps each ACTUALLY PRESENT 2x2
Life block to a larger display pixel. The LEFT viewport shows raw Life cells,
including in-flight gliders, without modifying or hiding any cells.
Both are taken from the exact same evolved world at each generation.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from life.native_lyric_word import routes,local_universe,pixel_target,VERIFY_THROUGH
from life.core import evolve
OUT=Path(__file__).resolve().parent
SAMPLES=set([0,180,200,219,220,228,232,240,248,256,260,264,267,268,276,288,304,326,348,366,374,386,394,398,402,410,420,422,426,430,438,441,442,450,460])
FRAMES=set(range(196,457,8))|SAMPLES
try:
    FONT=ImageFont.truetype('DejaVuSans.ttf',20)
    BOLD=ImageFont.truetype('DejaVuSans-Bold.ttf',26)
    SMALL=ImageFont.truetype('DejaVuSans.ttf',15)
except OSError:
    FONT=BOLD=SMALL=ImageFont.load_default()
BACKGROUND='#091522'
PANEL='#122231'
INK='#e6f2f6'
WEAK='#8295ad'
GLIDER='#526c84'
PIX='#65dfc9'

def render(gen,cells):
    im=Image.new('RGB',(1180,560),BACKGROUND)
    d=ImageDraw.Draw(im)
    d.text((30,16),'Made of Maybe  /  Native-Life lyrics experiment',font=BOLD,fill=INK)
    d.text((30,52),f'One fixed-speed B3/S23 universe · Generation {gen:03d} · {gen/24:.3f} seconds',font=SMALL,fill=WEAK)
    d.rounded_rectangle((30,98,570,485),radius=18,fill=PANEL)
    d.rounded_rectangle((590,98,1150,485),radius=18,fill=PANEL)
    d.text((52,110),'RAW CELLS · SIGNAL TRAFFIC',font=FONT,fill=INK)
    d.text((614,110),'ACTUAL 2×2 BLOCKS · DISPLAY ENLARGED',font=FONT,fill=INK)
    # Left view: every raw live cell is faithfully plotted, including gliders.
    # The camera is fixed and shows the target glyph's whole region.
    scale=1.55
    for x,y in cells:
        px=int(135+(x+20)*scale);py=int(192+(y+12)*scale)
        if 55<=px<552 and 160<=py<465:
            d.rectangle((px,py,px+1,py+1),fill=GLIDER)
    # Paint target pixels in different color only when all four constituent
    # cells are physically alive (no renderer-created Life cells).
    count=0
    for route in routes():
        if pixel_target(route)<=cells:
            count+=1
            px=int(135+(route.x+20)*scale);py=int(192+(route.y+12)*scale)
            d.rectangle((px,py,px+3,py+3),fill=PIX)
            # Right viewport: optical magnification from actual living block.
            xgrid=route.x//20; ygrid=route.y//20
            ox=660+xgrid*34;oy=207+ygrid*34
            d.rounded_rectangle((ox,oy,ox+28,oy+28),radius=4,fill=PIX)
    d.text((55,447),'Unfiltered live cells (no erased glider pixels)',font=SMALL,fill=WEAK)
    d.text((614,447),'One display square = one real stable 2×2 Life block',font=SMALL,fill=WEAK)
    d.line((30,512,1150,512),fill='#314253',width=2)
    info=f'WE  ·  {count:02d}/35 character pixels  ·  Complete at g268  ·  Clear at g442'
    d.text((34,519),info,font=SMALL,fill=INK)
    return im

def main():
    state=local_universe()
    frames=[];bygen={}
    for gen in range(max(FRAMES)+1):
        if gen in FRAMES:
            im=render(gen,state)
            bygen[gen]=im
            if gen>=196 and (gen%8==4 or gen in (268,442)):
                frames.append(im.resize((885,420),Image.Resampling.NEAREST))
        if gen<max(FRAMES):state=evolve(state)
    if frames:
        frames[0].save(OUT/'native_we_physical_letters.gif',save_all=True,
            append_images=frames[1:],duration=145,loop=0,optimize=True)
    picks=[220,268,398,442]
    sheet=Image.new('RGB',(1180*2,560*2),BACKGROUND)
    for i,g in enumerate(picks):
        sheet.paste(bygen[g],((i%2)*1180,(i//2)*560))
    sheet.save(OUT/'native_we_build_erase_contact.png',optimize=True)
    bygen[268].save(OUT/'native_we_complete_at_cue.png',optimize=True)
    print('Exported actual Life glider text reveal/erase GIF, contact sheet and cue still.')
if __name__=='__main__':main()
