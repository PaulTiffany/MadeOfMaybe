"""Export the exact complete preloaded B3/S23 universe, no dependencies.

Run: python -m life.export_dense > patterns/dense_three_state_singer.rle
"""
from .dense_glider_mouth import universe
from .export_operational import compact_rle

if __name__=='__main__':
    print(compact_rle(universe(),(
        'B3/S23: singer, unchanged bubble and letters, pulsar.',
        'Preloaded gliders control CLOSED MEDIUM OPEN and direct skips.',
        'All cells initially present; fixed clock; qualified for 785 steps.',
    )),end='')
