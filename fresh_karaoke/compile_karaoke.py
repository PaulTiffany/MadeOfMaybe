"""Made of Maybe / START FRESH / isolated one-line moving-LWSS karaoke.

No singer, mouth, bubble, converters, eater, or old multi-lane architecture.
One generation-zero world with 403 words, four common physical LWSS rows.
Every pixel is a native c/2 westbound LWSS, no runtime insertion.
Native B3/S23 is used to obtain the orbit and independently check clearance.

Reuses only old 3x4 font bitmaps, native 9-cell LWSS phase, and 403-word
quantized Suno alignment. The original 468 alignment tokens are in the old
repository at data/made_of_maybe_suno_alignment.json; this self-contained
source score was extracted from that alignment's existing 403-word compiler.
"""
from __future__ import annotations
import argparse,bisect,gzip,json
from pathlib import Path
from collections import Counter

HERE=Path(__file__).resolve().parent
SONG_DURATION=238.875
ORIGINAL_GPS=192
GPS=1920  # 10x the original tick clock, constant for the ENTIRE song.
FPS=48
PITCH=8
WORD_GAP=24
LWSS=frozenset({(1,0),(4,0),(0,1),(0,2),(4,2),(0,3),(1,3),(2,3),(3,3)})


def evolve(cells):
    n=Counter((x+dx,y+dy) for x,y in cells
              for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy)
    return {p for p,count in n.items() if count==3 or count==2 and p in cells}


def orbit():
    p=[set(LWSS)]
    for _ in range(3):p.append(evolve(p[-1]))
    assert evolve(p[-1])=={(x-2,y) for x,y in LWSS}, 'not a real westbound Life LWSS'
    return tuple(tuple(sorted(q)) for q in p)


def compact_font():
    f=json.loads((HERE/'reference/reference_font_5x7.json').read_text())
    out={k:tuple(''.join(v[r][c] for c in (0,2,4)) for r in (0,2,4,6))
          for k,v in f.items()}
    out['W']=('101','101','111','101') # Preserve original 3x4 LWSS font.
    return out


def word_pixels(text,font):
    return [(4*i+c,r) for i,ch in enumerate(text.upper())
            for r,row in enumerate(font[ch]) for c,lit in enumerate(row) if lit=='1']


def even_ceil(x):
    return x+(x%2)


def compile_score():
    source=json.loads((HERE/'reference/suno_403_word_score.json').read_text())
    assert len(source)==403 and source[0]['text']=='WE' and source[1]['text']=='MADE'
    assert source[-1]['text']=='NOW.'
    font=compact_font()
    words=[];positions=[]
    previous_right=None
    for a in source:
        pixels=word_pixels(a['text'],font)
        if not pixels:raise ValueError(('empty word',a))
        low=min(c for c,r in pixels); high=max(c for c,r in pixels)
        # Preserves original quantized alignment (192gps -> 1920gps) when
        # physically possible. If onsets are too close for a shared four-row
        # track, delay the new word just enough to avoid overlapping ships.
        desired_g=a['onset_g192']*(GPS//ORIGINAL_GPS)
        desired_x=desired_g//2
        base=desired_x
        if previous_right is not None:
            base=max(base,previous_right+WORD_GAP-PITCH*low)
        base=even_ceil(base)
        assert base>=desired_x
        # Store actual physical coordinates, not per-word stages or switches.
        origins=[(base+PITCH*c,PITCH*r) for c,r in pixels]
        current_left=min(x for x,y in origins)
        current_right=max(x for x,y in origins)
        if previous_right is not None and current_left-previous_right<WORD_GAP:
            raise AssertionError('world not sufficiently spaced')
        previous_right=current_right
        actual_g=2*base
        actual_s=actual_g/GPS
        target_s=a['onset_g192']/ORIGINAL_GPS
        words.append({'index':a['index'],'text':a['text'],
                      'source_onset_g192':a['onset_g192'],
                      'target_s_from_quantized_Suno':target_s,
                      'actual_readhead_s':actual_s,
                      'delay_ms':round(1000*(actual_s-target_s),4),
                      'leftmost_ship_g0':current_left,'rightmost_ship_g0':current_right,
                      'glyph_ship_count':len(origins),
                      'reference_origin_g0_x':base})
        positions.extend(origins)
    assert len(positions)==10366, f'alphabet or song changed: {len(positions)}'
    assert len(set(positions))==len(positions), 'two ships share a source origin'
    positions.sort()
    phases=orbit()
    # All four phases must be Moore-neighborhood disjoint for ALL 10,366
    # ships. Since all ships share the same orbit and velocity, this remains
    # true for the full song, without 500k expensive global native steps.
    # Test each distinct relative neighbor offset within 15 x 15 region.
    rels=set();posset=set(positions)
    for x,y in positions:
        for yy in (y-24,y-16,y-8,y,y+8,y+16,y+24):
            for xx in range(x-14,x+15,2):
                if (xx,yy) in posset and (xx,yy)!=(x,y):
                    rels.add((xx-x,yy-y))
    for phase in phases:
        c=set(phase)
        neighbor={(x+dx,y+dy) for x,y in c
                  for dx in (-1,0,1) for dy in (-1,0,1)}
        for dx,dy in rels:
            if any((x+dx,y+dy) in neighbor for x,y in c):
                raise AssertionError(('native B3/S23 ship crosstalk',dx,dy))
    # A second geometric check of all rows with sorted spacings. There are
    # no auxiliary cells; the world is exactly a union of separated LWSSs.
    for row in range(4):
        xs=sorted(x for x,y in positions if y==PITCH*row)
        assert all(b-a>=8 for a,b in zip(xs,xs[1:]))
    return words,positions,phases


def export(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    words,positions,phases=compile_score()
    with gzip.open(out/'LWSS_one_line_generation_zero.tsv.gz','wt',compresslevel=6) as f:
        for sx,sy in positions:
            for x,y in sorted(LWSS):f.write(f'{sx+x} {sy+y}\n')
    # Spaceship-glyph coordinate score; not renderer generated text.
    with gzip.open(out/'native_LWSS_ship_origins.csv.gz','wt',compresslevel=6) as f:
        f.write('x,y\n')
        for x,y in positions:f.write(f'{x},{y}\n')
    max_delay=max(w['delay_ms'] for w in words)
    delayed=[w for w in words if w['delay_ms']>0.01]
    report={'purpose':'Full-song FIRST ACCEPTANCE GATE / isolated karaoke only',
            'rule':'B3/S23','song_id':'53610991-7381-4749-96e1-79b8e3b1c28b',
            'video_duration_seconds':SONG_DURATION,
            'word_count':len(words),'LWSS_glyph_pixel_count':len(positions),
            'initial_world_live_cell_count':len(positions)*len(LWSS),
            'shared_physical_rows':[0,8,16,24],
            'independent_caption_stages':0,'word_lanes':1,
            'single_initial_condition':True,'source_is_preloaded_westbound':True,
            'genuine_native_LWSS_orbit_period':4,
            'native_generations_per_music_second':GPS,
            'native_video_frames_per_second':FPS,
            'native_frame_step_generations':GPS//FPS,
            'LWSS_velocity_cells_per_native_4_generations':-2,
            'font_columns_per_char':4,'font_pixels_pitch':PITCH,
            'required_blank_cells_between_words':WORD_GAP,
            'native_orbit_disjoint_all_phases':True,
            'max_additional_word_delay_ms':max_delay,
            'shifted_word_count':len(delayed),
            'shifted_words':delayed,
            'has_singer':False,'has_eaters':False,'has_converters':False,
            'has_mouth_sensors':False,'has_optical_lyrics':False,
            'camera_cuts':0,
            'caveat':'Suno start times quantized to 192gps in previous alignment compiler; baseline timing error up to 10.4ms plus reported space-delay.'}
    (out/'single_line_score_report.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'all_403_words_physical_arrivals.json').write_text(json.dumps(words,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('shifted_words',)},indent=2))
    return words,positions,phases

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default=str(HERE/'output'))
    a=p.parse_args();export(a.out)
