"""Render actual native-Life word states from one continuous preloaded universe.

Output enlarges all ACTUALLY COMPLETE 2x2 Life block pixels for legibility;
no text glyphs are painted from a script and no world cells are inserted.
Control gliders remain present outside the tightly framed lyric camera.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import evolve
from life.first_line_karaoke import (score,target_blocks,universe,
   ERASE_GENERATION,PITCH,GPS)

OUT=Path(__file__).resolve().parent
try:
    FONT=ImageFont.truetype('DejaVuSans.ttf',18)
    HEADER=ImageFont.truetype('DejaVuSans-Bold.ttf',29)
except OSError:
    FONT=HEADER=ImageFont.load_default()
INK='#e8f1f5';MUTED='#89a1b7';BG='#091522';LIT='#9befd9'
WORDS=score();TARGETS=[target_blocks(w) for w in WORDS]
PICKS=[WORDS[0].make_g-1]+[w.make_g for w in WORDS]+[ERASE_GENERATION]
FRAMES=sorted(set(PICKS)|set(range(2110,ERASE_GENERATION+1,8)))
WIDTH,HEIGHT=1320,392


def render(gen,live):
    img=Image.new('RGB',(WIDTH,HEIGHT),BG)
    d=ImageDraw.Draw(img)
    d.text((37,14),'MADE OF MAYBE  /  7 PHYSICAL LYRIC WORDS',font=HEADER,fill=INK)
    d.text((38,53),'One constant B3/S23 universe · 192 Life generations/audio-second · music at 1×',
           font=FONT,fill=MUTED)
    lit=[]
    for w,targets in zip(WORDS,TARGETS):
        count=0
        for (x,y),target in zip(w.targets,targets):
            if target<=live:
                count+=1
                X=85+(x//PITCH)*12
                Y=104+(y//PITCH)*12
                d.rounded_rectangle((X,Y,X+9,Y+9),radius=2,fill=LIT)
        lit.append(count)
    d.line((37,327,1283,327),fill='#375065',width=1)
    d.text((38,337),f'g{gen:04d}  /  {gen/GPS:06.3f}s   ·   '+
           ' '.join(f'{w.text}:{got}/{len(w.targets)}' for w,got in zip(WORDS,lit)),
           font=FONT,fill=INK)
    d.text((38,366),'Only actual completed block pixels are optically enlarged; all 1,083 gliders are simulated.',
           font=FONT,fill=MUTED)
    return img


def main():
    world=universe();shots={};movie=[]
    for gen in range(max(FRAMES)+1):
        if gen in FRAMES:
            frame=render(gen,world)
            if gen in PICKS:shots[gen]=frame
            if gen>=2110:movie.append(frame.resize((990,294)))
        if gen<max(FRAMES):world=evolve(world)
    card=Image.new('RGB',(WIDTH*3,HEIGHT*3),BG)
    for i,g in enumerate(PICKS):card.paste(shots[g],((i%3)*WIDTH,(i//3)*HEIGHT))
    card.save(OUT/'seven_real_words_contact_sheet.png',optimize=True)
    shots[WORDS[-1].make_g].save(OUT/'seven_real_words_complete.png',optimize=True)
    movie[0].save(OUT/'seven_real_words_glider_karaoke.gif',save_all=True,
                  append_images=movie[1:],duration=42,loop=0,optimize=True)
    print('Rendered seven real words evolving in one B3/S23 universe')

if __name__=='__main__':main()
