"""Export native B3/S23 preloaded gliders, not image-frame instructions.

Usage:
    python -m life.export_native_lyric_word > patterns/native_we_glider_written_world.rle
    python -m life.export_native_lyric_word --word-only > patterns/native_we_glider_only.rle
"""
import argparse
from .native_lyric_word import composed_universe,local_universe
from .export_operational import compact_rle

if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--word-only',action='store_true',help='exclude distant singer/bubble')
    args=cli.parse_args()
    cells=local_universe() if args.word_only else composed_universe()
    print(compact_rle(cells,(
        'MadeOfMaybe: B3/S23 with native glider-written and erased WE (35 physical glyph pixels)',
        'WE begins assembling at g220, complete by g268, erased by g442',
        'Suno alignment WE 11.224-11.479s at 24 gen/sec; deletion lags audio',
        'All gliders are in generation-zero seed; no runtime insertions or image switching',
        'Word-only export' if args.word_only else 'Complete singer, unchanged bubble + isolated lyric stage',
    )),end='')
