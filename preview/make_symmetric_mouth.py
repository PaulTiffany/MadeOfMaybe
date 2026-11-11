"""Render real glider-evolved singer and original bubble with Pillow.

All drawn cells exist in the B3/S23 initial universe. No runtime insertions.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import evolve
from life.symmetric_full_mouth import components,universe,POSE_SAMPLES,FULL_DURATION,target_blocks
from life.export_operational import compact_rle

OUT=Path(__file__).resolve().parent
BG=(10,17,29);FACE=(225,239,242);EYES=(238,248,251)
LIP=(252,149,160);TEETH=(250,219,187);SIGNAL=(47,69,89)
BUBBLE=(236,222,158);PULSAR=(167,190,231)
try:
    TITLE=ImageFont.truetype('DejaVuSans-Bold.ttf',30)
    FONT=ImageFont.truetype('DejaVuSans.ttf',18)
except OSError:
    TITLE=FONT=ImageFont.load_default()

def snapshot(parts,gen,size=(670,645),scale=1.45,stage=False):
    W,H=size;ox=310 if not stage else 430;oy=345
    image=Image.new('RGB',size,BG);draw=ImageDraw.Draw(image)
    state=POSE_SAMPLES.get(gen)
    targets=target_blocks(state) if state else set()
    for key,cells in parts.items():
        col=(FACE if key=='outline' else
             EYES if key=='eyes_nose' else
             TEETH if key=='rest_line' else
             BUBBLE if key.startswith('bubble') else
             PULSAR if key=='pulsar' else SIGNAL)
        for x,y in cells:
            X=round(ox+scale*x);Y=round(oy+scale*y)
            if 5<=X<W-3 and 3<=Y<H-4:
                color=LIP if key.startswith(('lower_','upper_')) and (x,y) in targets else col
                side=max(2,round(scale*2))
                draw.rectangle((X,Y,X+side-1,Y+side-1),fill=color)
    draw.text((20,15),f'{(state or "EVOLVING").upper()}  •  G{gen}',fill=FACE,font=TITLE)
    draw.text((22,58),'Native Life: mirrored moving lips / protected eyes',
              fill=(147,163,180),font=FONT)
    return image

def render():
    parts=components(with_bubble=False)
    stage=components(with_bubble=True)
    snaps={};gif=[]
    for g in range(FULL_DURATION):
        if g in (60,180,288,420,540,680,778):
            snaps[g]=({k:set(v) for k,v in parts.items()},
                      {k:set(v) for k,v in stage.items()})
        if g%18==0:
            gif.append(snapshot(parts,g).resize((500,481),Image.Resampling.NEAREST))
        parts={k:evolve(v) for k,v in parts.items()}
        stage={k:evolve(v) for k,v in stage.items()}
    width,height=670,645
    sheet=Image.new('RGB',(3*width,height),BG)
    for i,g in enumerate((60,180,288)):
        sheet.paste(snapshot(snaps[g][0],g),(i*width,0))
    sheet.save(OUT/'symmetric_mouth_three_states.png',optimize=True)
    snapshot(snaps[288][1],288,size=(1480,720),scale=1.33,stage=True).save(
        OUT/'symmetric_singer_bubble.png',optimize=True)
    gif[0].save(OUT/'symmetric_mouth_gliders.gif',save_all=True,
                append_images=gif[1:],duration=130,loop=0,optimize=True)
    rle=OUT.parent/'patterns'/'symmetric_moving_lips.rle'
    rle.write_text(compact_rle(universe(with_bubble=True),(
        'One B3/S23 initial universe. Glider-controlled moving upper/lower lips.',
        'CLOSED MEDIUM OPEN MEDIUM CLOSED OPEN CLOSED (direct skip).',
        'A short central resting band is permanent, pending another actuator.',
    )),encoding='utf-8')
    print('Generated live simulation GIF, checkpoint sheet, stage and RLE.')

if __name__=='__main__':
    render()
