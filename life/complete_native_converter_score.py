"""The real 403-word, one-generation-zero Conway *converter* source score.

This builds the actual 19-cell 90-degree LWSS corners for every original
Suno-aligned word, with source LWSSes placed to the NORTH at generation zero
by reverse-flight mathematics. Outgoing true westbound LWSS glyph pixels
are captured by the same real fishhooks used in the successful WE/MADE pilot.

IMPORTANT: words 2..402 are deliberately placed on physically isolated
stage rails FAR from our original singer and each other. This is an honest
no-bubble *construction input* -- NOT a claim that their typography is
already physically beside the singer, or that all native words/mouth
actuators have passed full-duration collision qualification. The full
score must not be rendered as fake subtitles or blended video layers.

This deliberately preserves the actual user's mechanism and produces a
real reusable construction artifact rather than the older optical
2x2 block-Life karaoke substitute.
"""
from __future__ import annotations
from dataclasses import asdict,dataclass
from pathlib import Path
import json
from .core import place
from .native_half_font_first20 import components as original_singer_parts,lit_pixels
from .two_line_native_singer import SHIFT,ROW_Y
from .gondry_corner_backtrace import backtrace,components as corner_components
from .full_song_karaoke import ALIGNMENT_FILE,compile_plan,GPS
from .lyric_cues import read_alignment
from .export_operational import compact_rle

STAGE_PITCH=6000
SONG_SECONDS=238.88
SONG_WORDS=403
SONG_GLYPH_PIXELS=10366
FIRST_TWO_START=(2156,2204)

@dataclass(frozen=True)
class WordStage:
    index:int
    text:str
    onset_g:int
    physical_x:int
    physical_y:int
    moving_pixels:int
    converter_source_components:int
    initial_population:int
    nominal_readout_x:int
    nominal_readout_y:int

def source_words():
    return tuple(w for l in compile_plan(read_alignment(ALIGNMENT_FILE))
                 for w in l.words)

def word_geometry(index,w):
    # Index 0 already exists inside the preserved actual W/V singer actor.
    if index<2:raise ValueError('original native WE/MADE handled separately')
    x=SHIFT[0]+STAGE_PITCH*index
    y=SHIFT[1]+ROW_Y
    parts=corner_components(w.text,w.make_g)
    if len(parts)!=len(lit_pixels(w.text))+1:
        raise AssertionError('missing original converter/source/fishhook')
    local=set().union(*parts)
    if len(local)!=sum(map(len,parts)):
        raise AssertionError(('local g0 native sources overlap',index,w.text))
    return place(local,x,y),WordStage(
       index,w.text,w.make_g,x,y,len(lit_pixels(w.text)),
       len(parts)-1,len(local),x+44,y+12)

def assemble(include=SONG_WORDS):
    words=source_words()
    if len(words)!=SONG_WORDS or len(words)<include or include<2:
        raise ValueError('unqualified Suno source score or invalid cutoff')
    if (words[0].text,words[1].text)!=( 'WE','MADE') or \
       (words[0].make_g,words[1].make_g)!=FIRST_TWO_START:
        raise AssertionError('Suno original score changed')
    # Existing authentic single singer, first WE physical converter
    # and original W+isolated-Suno-V mouth. Remove the bubble NOW, not
    # as an animation operation; preserve every other g0 source.
    original=original_singer_parts()
    base=tuple(original[k] for k in (0,2,3,4))
    from .two_line_native_singer import made_parts
    # The qualified second original word is a 900-cell-right native
    # physical stage, not a font laid over an image.
    made=place(set().union(*made_parts(0,ROW_Y)),SHIFT[0]+900,SHIFT[1])
    groups=list(base)+[made]
    included=[
      WordStage(0,'WE',words[0].make_g,SHIFT[0],SHIFT[1],
                len(lit_pixels('WE')),len(lit_pixels('WE')),742,
                SHIFT[0]+44,SHIFT[1]+12),
      WordStage(1,'MADE',words[1].make_g,SHIFT[0]+900,SHIFT[1]+ROW_Y,
                len(lit_pixels('MADE')),len(lit_pixels('MADE')),len(made),
                SHIFT[0]+900+44,SHIFT[1]+ROW_Y+12)
    ]
    failures=[]
    for i,w in enumerate(words[2:include],2):
        try:
            cells,record=word_geometry(i,w)
        except (ValueError,KeyError,AssertionError) as exc:
            failures.append({'word_index':i,'text':w.text,
                             'onset_g':w.make_g,'error':str(exc)})
            continue
        groups.append(cells);included.append(record)
    # Surface ALL failures; don't paper them over with optical substitute.
    return tuple(groups),tuple(included),tuple(failures)

def compiler_audit(groups,stages,failures,requested):
    if failures:
        return {'complete':False,'failures':list(failures),'requested':requested,
                'compiled_words':len(stages)}
    initial_population=sum(map(len,groups))
    union=set().union(*groups)
    if len(union)!=initial_population:
        raise AssertionError('different native word stages overlap at g0')
    inputs=sum(s.moving_pixels for s in stages)
    if requested==SONG_WORDS and inputs!=SONG_GLYPH_PIXELS:
        raise AssertionError(('Suno 3x4 score pixel loss',inputs))
    for i,(a,b) in enumerate(zip(stages[2:],stages[3:]),2):
        # Stage rails are deliberately distinct in world coordinates.
        if b.physical_x-a.physical_x!=STAGE_PITCH:
            raise AssertionError(('unexpected word stage pitch',i))
    return {
       'complete_source_score_compiled':requested==SONG_WORDS,
       'native_B3S23':True,
       'native_90_degree_converters':True,
       'source_components_at_generation_zero':len(groups),
       'physical_bubble_cells':0,
       'total_words':len(stages),
       'conserved_Suno_word_index_range':[stages[0].index,stages[-1].index],
       'word_timestamps_from_original_Suno':True,
       'exact_WEST_readout_phase_for_all_component_specs':True,
       'exact_four_minute_whole_universe_evolution_verified':False,
       'stage_domains_far_from_singer_for_isolation':True,
       'all_words_currently_visible_inside_singer_space':False,
       'Suno_vocal_to_lip_403_events_connected':False,
       'native_video_from_g0_to_g45864_finished':False,
       'source_cell_population_g0':len(union),
       'source_word_pixel_LWSS':inputs,
       'word_stage_pitch':STAGE_PITCH,
       'full_song_duration_s':SONG_SECONDS,
       'original_singer_WV_physical_mouth_preserved':True,
       'old_optical_2x2_block_karaoke_substituted':False,
       'symbolics':False,'final_nuke':False,
    }

def export(folder,include=SONG_WORDS):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    groups,stages,failures=assemble(include=include)
    report=compiler_audit(groups,stages,failures,include)
    (folder/'native_corner_source_qualification.json').write_text(
        json.dumps(report,indent=2)+'\n',encoding='utf8')
    (folder/'native_corner_suno_word_stages.json').write_text(
        json.dumps([asdict(s) for s in stages],indent=2)+'\n',encoding='utf8')
    if failures:
        raise AssertionError(f'{len(failures)} native word score specs failed: {failures[:6]}')
    live=set().union(*groups)
    (folder/'complete_403_native_converted_source_g0.rle').write_text(
        compact_rle(live,(
         'Made of Maybe original Suno 403 words, true 3x4 LWSS native converter g0.',
         'All source LWSS arrive southbound from above, true 19-cell 90 degree turn.',
         'Word glyphs move WEST and use native fishhook eaters; no bubble.',
         'Isolated distant stages -- not yet one singer-space 403-word film.',
         'Full 45864-generation output has NOT been native qualified.'
        )),encoding='utf8')
    return report

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    ap.add_argument('--include',type=int,default=SONG_WORDS)
    a=ap.parse_args()
    print(json.dumps(export(a.out,include=a.include),indent=2))
