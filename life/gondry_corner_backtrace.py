"""Gondry staging with the ORIGINAL 90-degree Conway converter intact.

Film requirement: a real LWSS falls from above, enters a 19-cell one-shot
native B3/S23 converter, emerges WEST as a glyph pixel, and is eaten
by an actual seven-cell fishhook. Work backward only over the free
ship-flight legs to find its generation-zero DOWNWARD input location.

This is the already-qualified miniature WE geometry generalized to
arbitrary target words. The original Suno first two words provide a
bounded, independent native-Life pilot; NOT a 403-word bubble video.
The direct-downstream vertical-only Gondry experiment is not the film.
"""
from __future__ import annotations
from dataclasses import asdict,dataclass
from pathlib import Path
import json
from .core import evolve,place
from .full_song_karaoke import ALIGNMENT_FILE,compile_plan,GPS
from .lyric_cues import read_alignment
from .native_half_font_first20 import (
    lit_pixels, routes, GLYPH_PITCH, STATION_PITCH)
from .vertical_lwss_corner import STATION,INPUT
from .staggered_word_mesh import (
    EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT,
    reference_output,OUTPUT_REFERENCE_MIN_X,OUTPUT_REFERENCE_MIN_Y)
from .export_operational import compact_rle

TURN_REFERENCE_G=200
STATION_X0=152
LAST_G=3600

@dataclass(frozen=True)
class SourceBacktrace:
    pixel_index:int
    column:int
    row:int
    station_x:int
    station_y:int
    incoming_advance_periods:int
    target_generation:int
    converted_reference_generation:int
    reading_x:int
    reading_y:int
    source_x:int
    source_y:int


def first_words():
    words=tuple(w for l in compile_plan(read_alignment(ALIGNMENT_FILE))
                for w in l.words)
    if len(words)!=403 or [w.text for w in words[:2]]!=['WE','MADE']:
        raise AssertionError('unexpected original Suno lyric score')
    if [w.make_g for w in words[:2]] != [2156,2204]:
        raise AssertionError('Suno word event times have changed')
    return words[:2]


def backtrace(word, target_g):
    """Solve westbound output goal -> turner time -> upstream southbound g0.

    For the existing 19-cell catalyst, the g200 westgoing phase starts at
    (station_x-43, station_y+12). Delay input by 4k native generations:
    put the southbound input 2k cells farther NORTH at g0.
    At prescribed target G, the output x is station_x-43-(G-200-4k)/2.
    """
    if target_g%4 or target_g<400:
        raise ValueError('target must be a viable period-four song tick')
    result=[]
    for i,col,row,x,y,k in routes(word,target_g=target_g):
        e=TURN_REFERENCE_G+4*k
        read_x=1+GLYPH_PITCH*col
        read_y=OUTPUT_REFERENCE_MIN_Y+y
        if e>target_g or e%4 or k<2:
            raise ValueError(('unreachable output readout',word,target_g,i))
        predicted_x=x+OUTPUT_REFERENCE_MIN_X-(target_g-e)//2
        if predicted_x!=read_x:
            raise AssertionError(('backtrace failed',word,i))
        result.append(SourceBacktrace(i,col,row,x,y,k,target_g,e,
                            read_x,read_y,x,y-2*k))
    return tuple(result)


def components(word='WE',target_g=2156,omit=None):
    plans=backtrace(word,target_g)
    if omit is not None and not 0<=omit<len(plans):
        raise ValueError('ablation index outside existing word')
    parts=[]
    for p in plans:
        cells=(place(STATION,p.station_x,p.station_y)
            | place(EATER_NORTHEAST,p.station_x,p.station_y)
            | place(EATER_SOUTHWEST,p.station_x,p.station_y))
        if p.pixel_index!=omit:
            cells |= place(INPUT,p.source_x,p.source_y)
        parts.append(cells)
    parts.append(set().union(*(place(EATER_TEXT,0,GLYPH_PITCH*r)
                    for r in range(4))))
    if len(set().union(*parts))!=sum(map(len,parts)):
        raise AssertionError('initial input ships or converter banks collide')
    return tuple(parts)


def universe(word='WE',target_g=2156,omit=None):
    return set().union(*components(word,target_g,omit))


def fixed_eaters(word='WE',target_g=2156):
    plans=backtrace(word,target_g)
    return (set().union(*(place(EATER_NORTHEAST,p.station_x,p.station_y)
             |place(EATER_SOUTHWEST,p.station_x,p.station_y) for p in plans))
             |set().union(*(place(EATER_TEXT,0,GLYPH_PITCH*r)
                  for r in range(4))))


def expected_formation(word='WE',target_g=2156,omit=None):
    out=set(fixed_eaters(word,target_g))
    ref=reference_output()
    for p in backtrace(word,target_g):
        if p.pixel_index!=omit:
            out |= place(ref,p.reading_x-OUTPUT_REFERENCE_MIN_X,
                             p.reading_y-OUTPUT_REFERENCE_MIN_Y)
        else:
            out |= place(STATION,p.station_x,p.station_y)
    return out


def expected_cleanup(word='WE',target_g=2156,omit=None):
    end=fixed_eaters(word,target_g)
    if omit is not None:
        p=backtrace(word,target_g)[omit]
        end |= place(STATION,p.station_x,p.station_y)
    return end


def check_native_snapshots(formation,cleanup,*,word,target_g,omit=None):
    expect=expected_formation(word,target_g,omit)
    last=expected_cleanup(word,target_g,omit)
    if formation != expect:
        raise AssertionError(('wrong native output pattern',word,target_g,
                              len(formation^expect)))
    if cleanup != last or evolve(cleanup)!=cleanup:
        raise AssertionError(('unconsumed ships/debris',word,
                              len(cleanup^last)))
    return {'rule':'B3/S23','word':word,'original_Suno_onset_g':target_g,
            'physical_downward_input_LWSS':len(backtrace(word,target_g))-(omit is not None),
            'physical_leftward_output_LWSS':len(backtrace(word,target_g))-(omit is not None),
            'physical_90_degree_converters':len(backtrace(word,target_g)),
            'actual_eater_cells_at_end':len(last),
            'formation_population':len(formation),
            'cleanup_population':len(cleanup),'final_generation':LAST_G,
            'source_ablation':omit,
            'input_to_converter_to_word_to_eater_qualified':True,
            'same_singer_bubble_403_word_assembly_qualified':False,
            'full_music_video_finished':False}


def export(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    summaries=[]
    for w in first_words():
        name=w.text.lower()
        groups=components(w.text,w.make_g)
        seed=set().union(*groups)
        (folder/f'{name}_vertical_to_left_g0.rle').write_text(
            compact_rle(seed,(
                f'Original Suno {w.text}: upward-preloaded LWSS arrives from above.',
                '19-cell genuine Life 90-degree turners, left-moving glyph output.',
                'Two native side-glider eaters and four shared text-row eaters.',
                'One-shot original mechanism, NOT direct-falling text.'
            )),encoding='utf8')
        with (folder/f'{name}_parts.tsv').open('w',encoding='utf8') as f:
            f.write(f'{len(groups)}\n')
            for i,part in enumerate(groups):
                for x,y in sorted(part):
                    f.write(f'{i} {x} {y}\n')
        (folder/f'{name}_backtrace.json').write_text(
            json.dumps([asdict(p) for p in backtrace(w.text,w.make_g)],
                        indent=2)+'\n',encoding='utf8')
        summaries.append({'word':w.text,'onset_g':w.make_g,
                          'incoming':len(backtrace(w.text,w.make_g)),
                          'seed_population':len(seed)})
    (folder/'contract.json').write_text(json.dumps({
        'film_mechanism':'LWSS DOWN -> native 19-cell corner -> LWSS LEFT -> native eater',
        'method':'inverse-stage free flight; run Life forward',
        'original_Suno_words':403,
        'separately_qualified_early_words':summaries,
        'old_direct_vertical_word_stream_is_not_the_target':True,
        'singer_mouth_integration_preserved_in_existing_first20_fixture':True,
        'full_song_one_bubble_qualified':False},indent=2)+'\n')
    return summaries


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    print(json.dumps(export(ap.parse_args().out),indent=2))
