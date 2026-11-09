"""Export exactly ONE native B3/S23 source shared by a WE pixel and lip tile.

No cells are inserted, switched, or hidden by a renderer. The export is the
actual 7-word karaoke plus the pre-existing singer, with one retargeted glider.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .export_full_song_karaoke import sparse_rle_stream
from .first_line_karaoke import GPS, ERASE_GENERATION
from .physical_lip_splitter_bridge import (
    complete_world_seed,assert_exact_signal_match,spatial_certificate,
    assert_portrait_protected,FULL_CHECK_G,SINGER_TRANSLATION,CAUSAL_WORD_G,
    LIP_NAME,LIP_TARGET,WORD_PIXEL,
)


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,default=Path('patterns/first_line_physical_lip_bridge.rle'))
    ap.add_argument('--report',type=Path,default=Path('output/first_line_physical_lip_bridge.json'))
    args=ap.parse_args(argv)
    exact=assert_exact_signal_match()
    spatial=spatial_certificate()
    protection=assert_portrait_protected(end=FULL_CHECK_G)
    initial=complete_world_seed()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('w',encoding='ascii') as fd:
        exported=sparse_rle_stream(iter(initial),fd,comments=(
            'Made of Maybe: same real input glider causes one WE glyph pixel AND one existing lip tile.',
            'One fixed B3/S23 initial world, 192 generations per audio second.',
            'Conservative one-lip experimental connection; other lip tile routes unchanged.',
            'One shared source glider, 84 stable catalyst cells; no runtime insertions.',
            'Finite-horizon qualification ends at native generation 3068.',
        ))
    cert={
        'qualification_scope':'ONE shared lyric pixel and ONE actual moving lip pixel',
        'clock_generations_per_audio_second':GPS,
        'first_word_cue_g':CAUSAL_WORD_G,
        'line_clear_g':ERASE_GENERATION,
        'tested_until_generation':FULL_CHECK_G,
        'lip_name':LIP_NAME,
        'lip_tile_local_origin':LIP_TARGET,
        'word_tile_global_origin':WORD_PIXEL,
        'portrait_global_translation':SINGER_TRANSLATION,
        'same_source_glider_controls_both':True,
        'surviving_seven_word_karaoke':True,
        'rest_of_portrait_unchanged':True,
        'full_song_mouth_fanout_complete':False,
        'other_lip_tiles_fanout_complete':False,
        'single_initial_world':True,
        'exact_glider_match':exact,
        'finite_spatial_certificate':spatial,
        'native_art_clearance':protection,
        'golly_export':exported,
    }
    args.report.write_text(json.dumps(cert,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in cert.items() if k not in ('finite_spatial_certificate','native_art_clearance','exact_glider_match')},indent=2))
    return cert


if __name__=='__main__':
    main()
