"""Golly RLE for the real physically relocated controller and singer."""
import argparse,json
from pathlib import Path
from .relocated_singer_anchor import qualified_integration,universe
from .export_full_song_karaoke import sparse_rle_stream

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=Path('patterns/relocated_singer_word_anchor.rle'))
    p.add_argument('--report',type=Path,default=Path('output/relocated_singer_word_anchor.json'))
    a=p.parse_args()
    certificate=qualified_integration()
    world=universe()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('w',encoding='utf-8') as handle:
        rle=sparse_rle_stream(iter(world),handle,comments=(
            'One B3/S23 native singer, speech bubble and physically below-bubble 84-cell splitter.',
            '2 Suno word-cued glyphs, at g2156 and g2976, no runtime cell edits.',
            'The narrower/lower face lip control remains independently timed.'))
    a.report.parent.mkdir(parents=True,exist_ok=True)
    data={**certificate,'rle':rle,'initial_live_cells':len(world)}
    a.report.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('Exported native Golly universe:',a.out, 'cells',len(world))
    return data
if __name__=='__main__':main()
