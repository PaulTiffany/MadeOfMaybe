"""Export actual first-line singer + seven-word karaoke as ONE initial B3/S23 world.

The first sung word is the retiming source for all 255 existing lip gliders;
this stage is lyric-cued but not yet a physical fanout into the lip bank.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .first_line_singing_character import combined_seed, spatial_certificate
from .export_full_song_karaoke import sparse_rle_stream


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=Path('patterns/first_line_singing_character.rle'))
    parser.add_argument('--report',type=Path,default=Path('output/first_line_singing_character_report.json'))
    args=parser.parse_args(argv)
    args.out.parent.mkdir(exist_ok=True,parents=True)
    args.report.parent.mkdir(exist_ok=True,parents=True)
    with args.out.open('w',encoding='ascii') as f:
        info=sparse_rle_stream(iter(combined_seed()),f,comments=(
            'Made of Maybe: physical Life singer AND 7 glider-written words at 192 gen/s.',
            'One initial world. Singer gliders are retimed from WE onset; 7 words are Suno aligned.',
            'The experimental 1->2 fanout is NOT yet connected to these full lips.',
            'Camera split-screen is presentational. No runtime cell edits.',
        ))
    cert={**spatial_certificate(),'export':info,'full_lip_fanout':False}
    args.report.write_text(json.dumps(cert,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'path':str(args.out),'report':str(args.report),**cert},indent=2))

if __name__=='__main__':main()
