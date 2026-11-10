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
if __name__=='__main__':
 import argparse
 from pathlib import Path
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--frames',type=Path,required=True)
 p.add_argument('--out',type=Path,required=True)
 p.add_argument('--thumbnail',type=Path)
 args=p.parse_args()
 original.render(args.frames,args.out,thumbnail=args.thumbnail)
