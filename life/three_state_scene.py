"""Candidate stable singer states with the existing bubble, letters, pulsar.

This composes each state *as its own independent starting universe*. It does
not yet provide or imply runtime switching between mouth states.
"""
from .three_state_mouth import scene as singer_pose
from .composition import bubble_parts, symbol
from .core import place


def parts(state: str):
    border,letters=bubble_parts()
    return {
        'face_and_mouth':singer_pose(state),
        'bubble_outline':border,
        'bubble_lyrics':letters,
        # Original symbol at x=75 overlaps the larger face; shift it clear.
        'pulsar':place(symbol(),340,0),
    }


def universe(state: str):
    return set().union(*parts(state).values())
