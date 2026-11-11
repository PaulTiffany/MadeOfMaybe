"""Reuse the existing speech bubble with a glider-controlled beehive face.

All parts are genuine cells in one uninterrupted B3/S23 universe.
"""
from .beehive_mouth import APPARATUS, FACE, INPUT
from .composition import bubble_parts, symbol
from .core import place

def components(pulses=3, spacing=48):
    circuit=set(APPARATUS)
    for i in range(pulses):
        circuit |= place(INPUT,-i*spacing,-i*spacing)
    bubble,text=bubble_parts()
    return {
        'mouth_actuator': circuit,
        'face': set(FACE),
        'bubble_outline': bubble,
        'bubble_lyrics': text,
        'pulsar': symbol(),
    }

def scene(pulses=3, spacing=48):
    return set().union(*components(pulses, spacing).values())
