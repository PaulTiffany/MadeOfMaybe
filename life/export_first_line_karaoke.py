"""Export a genuine preloaded-glider seven-word Life karaoke LINE, no bubble.

  python -m life.export_first_line_karaoke > patterns/first_line_192.rle
"""
import argparse
import json
from pathlib import Path
from .first_line_karaoke import (GPS,PITCH,ERASE_GENERATION,
   score,separation_certificate,universe)
from .export_operational import compact_rle

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',type=Path)
    args=parser.parse_args()
    cert=separation_certificate()
    info={**cert,'source':'Suno alignment, 1st verse first seven words',
          'audio_seconds':{'first_word':score()[0].start_s,
                           'line_end':13.42},
          'word_events':[{'word':w.text,'start_s':w.start_s,'end_s':w.end_s,
                          'physical_make_generation':w.make_g,
                          'actual_cue_time_s':round(w.make_g/GPS,6),
                          'source_suno_error_ms':round((w.make_g/GPS-w.start_s)*1000,3),
                          'actual_physical_glyph_pixels':len(w.targets)} for w in score()]}
    if args.manifest:
        args.manifest.parent.mkdir(parents=True,exist_ok=True)
        args.manifest.write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    print(compact_rle(universe(),(
      'MadeOfMaybe: seven TRUE glider-written 5x7 words, no bubble, 192 Life gens/audio-second',
      'WE MADE A WINDOW / OUT OF SAND, words built individually at actual Suno onset generations',
      f'All 361 pixels are 2x2 Life blocks; glider routes are isolated at physical pitch {PITCH}',
      f'Erase entire first lyric line by generation {ERASE_GENERATION} (13.427 audio seconds)',
      'All 1083 gliders present at generation zero. No runtime cell edits or video glyph overlays.',
      'Output camera may optically enlarge real blocks; underlying Life geometry is enormous.',
    )),end='')

if __name__=='__main__':main()
