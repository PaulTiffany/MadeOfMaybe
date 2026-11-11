"""Export physical 1-to-2 glider splitter / lyric-pixel / 3-state mouth pilot.

Run: python -m life.export_lyric_mouth_fanout \
  --out patterns/lyric_mouth_shared_splitter.rle \
  --manifest output/lyric_mouth_shared_splitter.json
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .lyric_mouth_fanout import (events,universe,GPS,CATALYSTS,
                                 PRIMARY_INPUT,full_song_mouth_intent,FINAL_QUALIFICATION_G)
from .export_operational import compact_rle


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,default=Path('patterns/lyric_mouth_shared_splitter.rle'))
    ap.add_argument('--manifest',type=Path,default=Path('output/lyric_mouth_shared_splitter.json'))
    args=ap.parse_args()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.manifest.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(compact_rle(universe(),(
        'Made of Maybe: genuine FOUR physical 1-glider -> 2-glider word/mouth fanouts.',
        'One output constructs ONE lyric pixel with a preloaded partner glider.',
        'Other output switches ONE 2x2 mouth port. Modes: C M O M C.',
        'Suno starts: WE, MADE, A, WINDOW; 192 Life gen/audio-second.',
        'Original stable splitter: https://conwaylife.com/wiki/Glider_duplicator',
        'Full singer lips and 403 sung word fanouts are NOT yet physically wired.',
    )),encoding='utf-8')
    intent=full_song_mouth_intent()
    manifest={'rule':'B3/S23','gps':GPS,'external_cell_insertion':False,
              'full_song_intent_count':len(intent),'full_song_intent':intent,
              'physical_pilot_events':[vars(x) for x in events()],
              'splitter_catalysts_per_event':len(CATALYSTS),
              'input_gliders_per_event':1,
              'output_gliders_per_event':2,
              'qualified_until_generation':FINAL_QUALIFICATION_G,
              'rle_seed_cells':len(universe()),
              'limitations':['one lyric pixel, not whole glyph, is causally gated per event',
                             'mouth ports are control register, not singer lip contours',
                             'remaining song intent is not physically routed',
                             'line-clear closure not routed']}
    args.manifest.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k!='full_song_intent'},indent=2))

if __name__=='__main__':main()
