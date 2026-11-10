"""Dual lyrics + isolated-vocals input score for a future native B3/S23 mouth gate.

A timing feasibility study, NOT a physically connected Life circuit.  No
movie frames or native cells are edited by this module.  An isolated vocal
stem is mandatory for real vocal activity; the mixed MP3 is NOT a stem.
"""
from __future__ import annotations
from array import array
from dataclasses import asdict,dataclass
from math import ceil,sqrt
from pathlib import Path
import json,sys,wave
from .full_song_karaoke import GPS,ALIGNMENT_FILE,compile_plan
from .lyric_cues import read_alignment

STATES=('closed','medium','open')
DEFAULT_DWELL_G=120
DEFAULT_ATTACK_G=48

@dataclass(frozen=True)
class PoseEvent:
    generation:int
    state:str
    reason:str
    voice_active:bool
    word_active:bool
    word_attacks:tuple[str,...]

def time_to_g(s:float)->int:
    if s<0:raise ValueError('negative source time')
    return 4*ceil(s*GPS/4-1e-9)

def vocal_activity_from_wav(path,*,hop_s=.02,relative_threshold=.14,
                            min_active_s=.08,bridge_gap_s=.09):
    """Threshold a previously isolated PCM16 vocal WAV, not the full mix."""
    if not 0<relative_threshold<1 or not 0<hop_s<=.1:
        raise ValueError('invalid vocal analysis settings')
    with wave.open(str(path),'rb') as f:
        rate=f.getframerate();channels=f.getnchannels()
        if f.getsampwidth()!=2 or not 1<=channels<=2 or rate<8000:
            raise ValueError('expected mono/stereo PCM16 vocal stem >=8kHz')
        hop=max(1,round(rate*hop_s));rms=[]
        while True:
            data=f.readframes(hop)
            if not data:break
            s=array('h');s.frombytes(data)
            if sys.byteorder!='little':s.byteswap()
            rms.append(sqrt(sum(x*x for x in s)/len(s))/32768 if s else 0.)
    if not rms:return ()
    hi=sorted(rms)[min(len(rms)-1,int(len(rms)*.9))]
    if hi<.0002:return ()
    threshold=max(.0002,hi*relative_threshold)
    active=[x>=threshold for x in rms]
    holes=max(0,round(bridge_gap_s/hop_s))
    for k in range(len(active)):
        if active[k]:continue
        j=k
        while j<len(active) and not active[j]:j+=1
        if k>0 and active[k-1] and j<len(active) and j-k<=holes:
            active[k:j]=[True]*(j-k)
    min_hops=max(1,round(min_active_s/hop_s))
    intervals=[];k=0
    while k<len(active):
        if not active[k]:k+=1;continue
        j=k
        while j<len(active) and active[j]:j+=1
        if j-k>=min_hops:
            intervals.append((round(k*hop_s,5),round(j*hop_s,5)))
        k=j
    return tuple(intervals)

def compile_score(vocal_intervals,*,alignment_path=ALIGNMENT_FILE,
                  dwell_g=DEFAULT_DWELL_G,attack_g=DEFAULT_ATTACK_G,
                  end_s=238.88,provenance='unverified input'):
    """Requests only. A synthetic voice timeline is allowed in tests only."""
    if dwell_g<48 or dwell_g%4 or attack_g<4 or attack_g%4:
        raise ValueError('mouth switch candidate must be c/4 aligned')
    if end_s<=0:raise ValueError('no song duration')
    voc=[];previous=-1.
    for start,end in vocal_intervals:
        if not(0<=start<end<=end_s) or start<previous:
            raise ValueError('non-monotone or invalid vocal intervals')
        voc.append((time_to_g(start),time_to_g(end)));previous=end
    lines=compile_plan(read_alignment(alignment_path))
    words=tuple(w for line in lines for w in line.words)
    attacks={};begins={};ends={}
    for w in words:
        start=w.make_g;end=max(start+4,time_to_g(w.end_s))
        attacks.setdefault(start,[]).append(w.text)
        begins[start]=begins.get(start,0)+1
        ends[end]=ends.get(end,0)+1
    current='closed';last_change=-dwell_g
    attack_until=0;active_words=0;vi=0
    events=[];ignored_attacks=0;vocal_only_ticks=0
    for g in range(0,time_to_g(end_s)+1,4):
        active_words+=begins.get(g,0)-ends.get(g,0)
        if active_words<0:raise AssertionError('negative word occupancy')
        word_on=active_words>0
        while vi<len(voc) and voc[vi][1]<=g:vi+=1
        voice_on=vi<len(voc) and voc[vi][0]<=g<voc[vi][1]
        onset=tuple(attacks.get(g,()))
        if onset:
            attack_until=max(attack_until,g+attack_g)
            if current=='open':ignored_attacks+=len(onset)
        if voice_on and not word_on:vocal_only_ticks+=1
        if not word_on and not voice_on:
            target='closed';reason='source_silence'
        elif g<attack_until or (word_on and not voice_on):
            target='open';reason='word_attack_or_alignment'
        elif voice_on:
            target=('open' if current=='closed' else
                    'medium' if current=='open' else 'open')
            reason='isolated_vocal_oscillator'
        else:
            target='open';reason='word_interval'
        if target!=current and g-last_change>=dwell_g:
            current=target;last_change=g
            events.append(PoseEvent(g,current,reason,voice_on,word_on,onset))
    return {'source':'isolated-vocal-intervals + exact Suno word alignment',
            'vocal_source_provenance':provenance,
            'gps':GPS,'word_count':len(words),'vocal_episodes':len(voc),
            'vocal_only_generations':4*vocal_only_ticks,
            'word_attacks_while_already_open':ignored_attacks,
            'dwell_g':dwell_g,'attack_g':attack_g,'time_s':end_s,
            'transitions':[asdict(x) for x in events],
            'physical_gate_built':False,'lip_actuation_qualified':False,
            'native_B3S23_control_circuit_qualified':False,
            'is_phoneme_recognition':False}

def save_audit(score,path):
    Path(path).write_text(json.dumps(score,indent=2)+'\n',encoding='utf8')
