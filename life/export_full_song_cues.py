"""Export full lyric line and word times plus a camera stage schedule.

External camera framing is permitted, but the caption TEXT is always made
by native Life glider collisions (no runtime glyph-cell injection).
"""
import argparse
import csv
from pathlib import Path
from .full_song_karaoke import compile_plan,ALIGNMENT_FILE
from .lyric_cues import read_alignment,_srt_clock


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--alignment',type=Path,default=ALIGNMENT_FILE)
    parser.add_argument('--out',type=Path,default=Path('output/full_song_native_life'))
    a=parser.parse_args(argv)
    lines=compile_plan(read_alignment(a.alignment))
    a.out.mkdir(parents=True,exist_ok=True)
    camera=[];words=[];subs=[]
    for line in lines:
        x_center=line.glyph_columns*line.pitch//2
        y_center=line.y_origin+3*line.pitch
        camera.append({'line':line.line_index,'starts_at_audio_s':line.start_s,
           'through_audio_s':round(line.clear_g/192,4),'center_x':x_center,
           'center_y':y_center,'pixel_pitch':line.pitch,
           'glyph_columns':line.glyph_columns,'glyph_rows':7,'text':line.text})
        for w in line.words:
            words.append({'line':line.line_index,'index':w.word_index,
               'word':w.text,'source_onset_s':w.start_s,'source_end_s':w.end_s,
               'real_make_generation':w.make_g,'real_make_s':round(w.make_g/192,4),
               'real_clear_generation':line.clear_g,'real_clear_s':round(line.clear_g/192,4),
               'glyph_pixels':w.pixel_count,'flagged':int(w.flagged)})
        subs.extend([str(line.line_index+1),
             f'{_srt_clock(line.start_s)} --> {_srt_clock(line.clear_g/192)}',
             line.text,''])
    for name,data in [('camera_schedule.csv',camera),('word_onsets.csv',words)]:
        with (a.out/name).open('w',newline='',encoding='utf-8') as f:
            wr=csv.DictWriter(f,fieldnames=list(data[0]));wr.writeheader();wr.writerows(data)
    (a.out/'full_song_native_life.srt').write_text('\n'.join(subs)+'\n',encoding='utf-8')
    print(f'Wrote camera and native-word score for {len(lines)} Life stages, {len(words)} words')

if __name__=='__main__':main()
