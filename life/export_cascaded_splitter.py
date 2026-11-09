"""Export verified 1→4 Life glider cascade as a standalone Golly RLE."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import encode_rle,parse_rle,place
from .cascaded_lyric_splitter import seed,check


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,default=Path('patterns/one_to_four_word_glider_splitter.rle'))
    p.add_argument('--report',type=Path,default=Path('output/one_to_four_word_glider_splitter.json'))
    args=p.parse_args()
    report=check()
    initial=seed()
    rle=encode_rle(initial,comments=[
      'One initial glider, 3 independent stable 84-cell duplicators, FOUR output gliders by g683.',
      'B3/S23 no runtime edits. Standalone fanout circuit, not yet wired to full mouth.',
    ])
    xs=[x for x,y in initial];ys=[y for x,y in initial]
    offset=(min(xs),min(ys))
    assert parse_rle(rle)==place(initial,-offset[0],-offset[1])
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(rle,encoding='ascii')
    args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'Golly 1-to-4 native Life circuit: {args.out}; g={report["generation"]}')

if __name__=='__main__':main()
