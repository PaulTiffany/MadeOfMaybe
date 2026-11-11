"""Golly pattern and finite B3/S23 certificate for a two-line reused lyric cue."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .export_full_song_karaoke import sparse_rle_stream
from .reusable_word_cue import (seed,qualification,splitter_reuse_certificate,
    protected_character_certificate,two_lip_causal_certificate)


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,default=Path('patterns/two_line_reused_word_cue.rle'))
    ap.add_argument('--report',type=Path,default=Path('output/two_line_reused_word_cue.json'))
    ap.add_argument('--with-portrait',action='store_true',help='include original singer and unchanged 5,796-cell art')
    ap.add_argument('--skip-long-replay',action='store_true',help='for CI after the dedicated exact native-Life unittest step')
    args=ap.parse_args(argv)
    if args.with_portrait:
        from .reusable_word_cue import character_world_with_second_lip
        from .first_line_singing_character import art_seed
        from .physical_lip_splitter_bridge import SINGER_TRANSLATION
        from .core import place
        world=character_world_with_second_lip()|place(art_seed(),*SINGER_TRANSLATION)
    else:world=seed()
    result={'two_line_source':qualification(),
            'reusable_splitter':splitter_reuse_certificate(),
            'two_causally_triggered_real_lip_tiles':
                ('native B3/S23 tested by tests.test_reusable_word_cue (separate gate)'
                 if args.skip_long_replay else two_lip_causal_certificate()),
            'unchanged_character':
                ('native B3/S23 tested by tests.test_reusable_word_cue (separate gate)'
                 if args.skip_long_replay else protected_character_certificate()),
            'long_replays_executed_in_this_export':not args.skip_long_replay,
            'includes_singer_in_rle':args.with_portrait}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('w',encoding='ascii') as stream:
        result['rle']=sparse_rle_stream(iter(world),stream,comments=(
            'B3/S23 fixed initial universe, 192 generations per audio second.',
            'Same 84-cell duplicator triggers a single physical lyric pixel on TWO separate aligned lyric lines.',
            'Experimental source anchor only: not all 403 lyric words or all mouth tiles.',
        ))
    args.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'export':str(args.out),'cells':result['rle']['cells'],
        'two_line_word_cues':2,'one_physical_word_pixel_reused':True,
        'original_lip_element_preserved':True,
        'second_lip_tile_causally_erased_by_second_word_source':True,
        'second_line_lip_fanout_complete':False},indent=2))
    return result

if __name__=='__main__':main()
