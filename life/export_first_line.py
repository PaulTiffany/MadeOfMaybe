"""Write native first-lyric-line B3/S23 starting universe to stdout."""
from .export_operational import compact_rle
from .lyric_text_scene import universe

if __name__=='__main__':
    print(compact_rle(universe(), (
        'MadeOfMaybe: seven Suno-aligned cue lights over two still-life pages.',
        '24 Life generations/second. Native gliders preloaded at g0.',
        'Lyrics static; dots glider-timed; pages selected by camera only.',
    )),end='')
