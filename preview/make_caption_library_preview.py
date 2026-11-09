"""Compare the first four genuinely stable Life text-page assets.

Presentation labels and colors are not simulated cells; the glyphs and bubble
are. Four panels are DIFFERENT initial conditions, not a switched Life scene.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.caption_library import bubble_frame,native_page
from life.lyric_cues import caption_pages,aligned_words,read_alignment

ROOT=Path(__file__).resolve().parents[1]
raw=read_alignment(ROOT/'data/first_verse_alignment_fixture.json')
pages=caption_pages(aligned_words(raw))
assert len(pages)==4
OUT=ROOT/'preview';OUT.mkdir(exist_ok=True)
WIDTH,HEIGHT=970,610
BACKGROUND='#081321';INK='#91ebde';LETTER='#ffcf8e';MUTED='#aabbd4'
try:
    head=ImageFont.truetype('DejaVuSans-Bold.ttf',24)
    body=ImageFont.truetype('DejaVuSans.ttf',18)
except OSError:
    head=body=ImageFont.load_default()

sheet=Image.new('RGB',(2*WIDTH,2*HEIGHT),BACKGROUND)
frame=bubble_frame()
for i,page in enumerate(pages):
    im=Image.new('RGB',(WIDTH,HEIGHT),BACKGROUND)
    pen=ImageDraw.Draw(im)
    pen.text((40,18),f'PAGE {i+1}   {page.start_s:.3f}–{page.end_s:.3f}s',font=head,fill=MUTED)
    pen.text((40,62),'STATIC NATIVE LIFE CAPTION ASSET (not a runtime switch)',font=body,fill=MUTED)
    cells=native_page(page)
    scale=2.50; origin_x,origin_y=249,-191;left,top=178,114
    for x,y in cells:
        px=int(left+(x-origin_x)*scale);py=int(top+(y-origin_y)*scale)
        if px<0 or px>=WIDTH or py<0 or py>=HEIGHT:continue
        pen.rectangle((px,py,px+3,py+3),fill=INK if (x,y) in frame else LETTER)
    sheet.paste(im,((i%2)*WIDTH,(i//2)*HEIGHT))
sheet.save(OUT/'first_lyric_pages_contact_sheet.png')
print('Previewed 4 real Life-stable caption page candidates; these are separate initial conditions.')
