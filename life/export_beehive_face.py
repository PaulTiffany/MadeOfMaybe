"""python -m life.export_beehive_face > beehive_face.rle"""
from .core import encode_rle
from .beehive_scene import scene

if __name__ == '__main__':
    print(encode_rle(scene(), [
        'B3/S23 singer plus original bubble and pulsar; all gliders preloaded.',
        'Beehive: Mitchell Riley 2023, LifeWiki G-to-X (November 2023)',
    ]), end='')
