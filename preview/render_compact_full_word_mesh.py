"""Compact camera over exact native B3/S23 35-turner WE snapshots.

The video accelerates 7600 real Life generations into 14 seconds for
review. This camera never creates, moves or substitutes any Life glyph.
"""
from __future__ import annotations
import render_staggered_word_mesh as original

# (preview_seconds, Life_generation, camera_center_x, center_y, scale)
original.KEYFRAMES=(
 (0.,0,900.,-1050.,.29),
 (1.5,1400,900.,-900.,.33),
 (3.8,3200,900.,-510.,.43),
 (6.,4900,700.,-40.,.57),
 (8.5,5990,290.,100.,1.2),
 (9.5,6050,175.,123.,1.62),
 (10.5,6300,100.,123.,1.62),
 (12.2,7000,-35.,123.,1.62),
 (14.,7600,-35.,123.,1.62),
)

PHRASE_CAMERA=(
 (0.,0,2200.,-1250.,.25),
 (2.,2000,2000.,-800.,.30),
 (5.,4200,1600.,-200.,.37),
 (7.9,5900,850.,100.,.62),
 (9.3,6000,720.,128.,.76),
 (10.5,6500,550.,125.,.76),
 (13.,8000,-100.,125.,.76),
 (16.,10000,-80.,125.,.76)
)

if __name__=='__main__':
 import argparse
 from pathlib import Path
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--frames',type=Path,required=True)
 p.add_argument('--out',type=Path,required=True)
 p.add_argument('--thumbnail',type=Path)
 p.add_argument('--phrase',action='store_true',help='Show the qualified 107-turn WE MADE phrase')
 args=p.parse_args()
 if args.phrase:
  original.KEYFRAMES=PHRASE_CAMERA
  original.DURATION_S=16
  from PIL import ImageDraw
  old_draw=original.draw
  def word_frame(cells,g,t):
   im=old_draw(cells,g,t)
   d=ImageDraw.Draw(im)
   d.rectangle((0,0,1280,82),fill=(6,11,26))
   d.text((32,20),'WE MADE / COMPACT STAGGERED NATIVE CONWAY WORDS',
          font=original.font(25,True),fill=(237,239,253))
   d.text((33,59),'ONE B3/S23 WORLD  |  107 VERTICAL LWSS INPUTS  →  107 MOVING LETTER PIXELS',
          font=original.font(13),fill=(167,191,217))
   return im
  original.draw=word_frame
 original.render(args.frames,args.out,thumbnail=args.thumbnail)
