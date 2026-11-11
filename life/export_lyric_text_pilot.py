"""python -m life.export_lyric_text_pilot > patterns/first_lyric_glider_progress.rle"""
from .export_operational import compact_rle
from .lyric_text_pilot import universe
if __name__=='__main__':
    print(compact_rle(universe(),(
        'MadeOfMaybe first-verse text-control pilot, native B3/S23 g0 universe',
        '24 generations/second; timed native word lamps: WE g268, MADE g276, A g284, WINDOW g288',
        'all four lamps erased at g326; static 5x7 Life caption text is not yet changed by gliders',
        'full song Suno source: data/made_of_maybe_suno_alignment.json',
        'no runtime cell insertion, frame swap, or simulation clock changes',
    )),end='')
