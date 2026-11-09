"""Singing character + physical first-line lettering; one B3/S23 world.

This is a split-view camera of two spatially independent parts of ONE initial
universe. The character uses native mouth glider trajectories retimed from the
first word, but its lip gliders are *not* yet children of the word splitter.
At 192 generation/audio-second, the singer does not change playback tempo.

Run:
  python preview/render_first_line_singer.py
  python preview/render_first_line_singer.py --audio /path/to/MadeOfMaybe.wav
"""
from __future__ import annotations
import argparse,sys,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from life.core import evolve,place
from life.glider_controlled_mouth import BLOCK
from life.first_line_singing_character import dynamic_seed,art_seed,safe_art,anchor_delay
from life.first_line_karaoke import GPS,PITCH,ERASE_GENERATION,score
from life.life_cell_sampler import block_alive_at
from life.symmetric_full_mouth import target_blocks
from life.expressive_mouth import START_LINE

W,H=1280,720
BG=(8,14,26)
PALETTE={
 'art_contour':(219,234,244),'art_eye_liner':(234,226,250),
 'art_iris':(123,241,223),'art_nose':(246,188,198),
 'art_cheekbones':(237,150,184),'art_hair_mass':(133,111,202),
 'art_hair_waves':(194,148,234),'art_hair_gloss':(240,213,252),
 'art_brows':(252,165,196),'art_lashes':(248,209,225),
 'art_jewelry':(243,202,139),
}
LIP=(255,116,172)
CENTER=(255,201,168)

def font(n,bold=False):
 for f in (('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'),
           '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
  try:return ImageFont.truetype(f,n)
  except OSError:pass
 return ImageFont.load_default()

STATIC_FONTS={size:font(size,True) for size in (16,19,26)}
FACE_SX=0.81;FACE_OX=280;FACE_OY=369


def portrait_points(draw,points,color,side=2):
 for x,y in points:
  px=int(FACE_OX+x*FACE_SX);py=int(FACE_OY+y*FACE_SX)
  if 12<px<550 and 74<py<688:
   draw.rectangle((px,py,px+side,py+side),fill=color)

MEDIUM_TILES=[];OPEN_TILES=[]
for state,arr in (('medium',MEDIUM_TILES),('open',OPEN_TILES)):
 all_cells=target_blocks(state)
 for x,y in all_cells:
  if (x-1,y) not in all_cells and (x,y-1) not in all_cells:
   arr.append(place(BLOCK,x,y))
CENTER_TILES=[place(BLOCK,*xy) for xy in START_LINE]


def make_image(g,world,art,*,diagnostic=False,first_glyph_pixel_alive=None):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 d.rounded_rectangle((16,61,555,684),radius=14,outline=(76,66,118),width=2)
 d.rounded_rectangle((571,61,1263,684),radius=14,outline=(52,111,117),width=2)
 d.text((26,22),'MADE OF MAYBE',font=STATIC_FONTS[26],fill=(240,230,252))
 d.text((1250,25),'B3/S23  |  192 GENERATIONS / SECOND',font=STATIC_FONTS[16],fill=(130,221,203),anchor='ra')
 # Low-contrast substrate paths are actual glider cells in the singer region.
 portrait_points(d,(xy for xy in world if -340<xy[0]<340 and -440<xy[1]<350),(39,46,67),1)
 for key,pixels in art.items():portrait_points(d,pixels,PALETTE.get(key,(220,220,220)),2)
 for state_tiles in (MEDIUM_TILES,OPEN_TILES):
  colored=set().union(*(tile for tile in state_tiles if tile<=world)) if state_tiles else set()
  portrait_points(d,colored,LIP,3)
 center=set().union(*(tile for tile in CENTER_TILES if tile<=world))
 portrait_points(d,center,CENTER,3)
 # This block count is calculated from native-Life target occupancy, not a drawing instruction.
 active=[w for w in score() if block_alive_at(w.make_g,ERASE_GENERATION,g)]
 now=active[-1].text if active else '—'
 status='SINGING' if active else ('PRELUDE' if g<score()[0].make_g else 'BREATH')
 d.text((29,645),status,font=STATIC_FONTS[19],fill=(246,151,197))
 d.text((535,648),f'{now}',font=STATIC_FONTS[19],fill=(226,214,244),anchor='ra')
 d.text((593,83),'THE LYRICS ARE ALSO LIFE',font=STATIC_FONTS[19],fill=(177,238,225))
 # Camera maps occupied real 2x2 sites by a single row-preserving affine
 # coordinate map. It never writes letters over the source live-cell state.
 row1=[w for i,w in enumerate(score()) if i<4]
 row2=[w for i,w in enumerate(score()) if i>=4]
 cell_pitch=7
 def ink_row(words,logical_row_y,base_y):
  if not words:return
  maxcol=max(x//PITCH for w in words for x,y in w.targets)
  left=607+(620-(maxcol+2)*cell_pitch)//2
  for w in words:
   live=block_alive_at(w.make_g,ERASE_GENERATION,g)
   if not live:continue
   color=(255,226,157) if w==active[-1] else (104,213,202)
   for tx,ty in w.targets:
    if first_glyph_pixel_alive is False and w==score()[0] and (tx,ty)==(0,0):
     continue
    xcol=tx//PITCH; yrow=ty//PITCH-logical_row_y
    px=left+xcol*cell_pitch;py=base_y+yrow*cell_pitch
    d.rounded_rectangle((px,py,px+cell_pitch-2,py+cell_pitch-2),radius=1,fill=color)
 ink_row(row1,0,280)
 ink_row(row2,10,410)
 d.text((606,541),'REAL 2×2 STILL-LIFE GLYPH CELLS',font=STATIC_FONTS[16],fill=(126,183,182))
 d.text((606,571),'WORD CONSTRUCTION: +2 GLIDERS  |  ERASE: +1',font=STATIC_FONTS[16],fill=(106,151,169))
 time_s=g/GPS
 d.text((606,629),f'{time_s:06.3f}s',font=STATIC_FONTS[26],fill=(237,236,242))
 d.text((1229,634),f'GEN {g:,}',font=STATIC_FONTS[16],fill=(154,180,186),anchor='ra')
 d.text((604,656),'ONE WORLD  •  TWO CAMERAS  •  NO RUNTIME CELL EDITS',font=STATIC_FONTS[16],fill=(136,157,169))
 return im


def render(output:Path,*,start_s=10.93,end_s=15.43,fps=24,audio=None):
 if GPS%fps:raise ValueError('frame rate must divide native Life rate')
 art=safe_art();moving=set(dynamic_seed())
 first=round(start_s*fps);last=round(end_s*fps)
 init_gen=first*(GPS//fps)
 for _ in range(init_gen):moving=evolve(moving)
 output.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
      '-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(fps),
      '-i','pipe:0']
 if audio:
  cmd+=['-ss',str(start_s),'-i',str(audio),'-map','0:v','-map','1:a',
        '-c:a','aac','-b:a','192k','-shortest']
 cmd+=['-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p',
       '-movflags','+faststart',str(output)]
 process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 stills={};sample_ticks={anchor_delay()+g for g in (60,180,288,420,540,960)}
 preview_dir=output.parent
 try:
  for frame in range(first,last):
   g=frame*(GPS//fps)
   pic=make_image(g,moving,art)
   process.stdin.write(pic.tobytes())
   if frame in (first,first+14,first+35,first+55,last-1):
    stills[frame]=pic.copy()
   for _ in range(GPS//fps):moving=evolve(moving)
  process.stdin.close()
  err=process.stderr.read().decode(errors='replace')
  if process.wait()!=0:raise RuntimeError('ffmpeg failed: '+err[-2000:])
 except Exception:
  process.kill();raise
 if stills:
  cols=2;tw,th=640,360
  sheet=Image.new('RGB',(tw*cols,th*3),BG)
  for idx,pic in enumerate(stills.values()):
   sheet.paste(pic.resize((tw,th)),((idx%cols)*tw,(idx//cols)*th))
  sheet.save(preview_dir/'first_line_singing_character_contact.png')
  list(stills.values())[3].save(preview_dir/'first_line_singing_character_frame.png')
 return {'start_seconds':start_s,'end_seconds':end_s,'fps':fps,'frames':last-first,
         'original_audio_unchanged':True,'audio_included':bool(audio),
         'source_life_constant_gps':GPS,'performer_source_cue':'LINE_CLEAR',
         'performer_source_generation':ERASE_GENERATION,
         'character_shift_generations':anchor_delay(),
         'full_lip_physical_fanout':False}


def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--out',type=Path,default=Path('preview/first_line_singing_character.mp4'))
 ap.add_argument('--audio',type=Path)
 args=ap.parse_args()
 import json
 out=render(args.out,audio=args.audio)
 (args.out.parent/'first_line_singing_character_video_metadata.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
