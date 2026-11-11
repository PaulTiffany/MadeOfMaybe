"""Print combined Life scene RLE: python -m life.export_scene > singer_bubble.rle"""
from .core import encode_rle
from .composition import scene
if __name__=='__main__':
    print(encode_rle(scene(),[
        'One constant-clock B3/S23 singer + bubble + pulsar; preloaded controls',
        'Mouth actuator Luke Kiernan 2023 https://conwaylife.com/wiki/Glider_to_block',
        'Pulsar https://conwaylife.com/wiki/Pulsar',
    ]),end='')
