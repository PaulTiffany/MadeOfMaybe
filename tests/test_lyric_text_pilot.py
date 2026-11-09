"""Actual physical word control, with optional fast full-scene qualification."""
from pathlib import Path
import unittest
from life.core import evolve,place,parse_rle
from life.glider_controlled_mouth import BLOCK
from life.lyric_text_pilot import (
    LAMPS,END_GENERATION,caption_cells,components,universe,
    lamp_seed,lamp_target,actual_lamp_states,
)
from life.export_operational import compact_rle

class NativeLyricProgressTests(unittest.TestCase):
    def test_text_remains_native_life_still_life(self):
        parts=components()
        text=caption_cells()
        self.assertEqual(evolve(text),text)
        self.assertEqual(evolve(text|parts['bubble_outline']), text|parts['bubble_outline'])
        self.assertNotIn('bubble_lyrics',parts)
        self.assertGreaterEqual(len(text)//4,200)

    def test_each_lyric_word_has_real_make_hold_erase(self):
        for lamp in LAMPS:
            with self.subTest(word=lamp.word):
                state=lamp_seed(lamp)
                target=lamp_target(lamp)
                for gen in range(345):
                    if gen in (lamp.activation_generation-1,
                               lamp.activation_generation,300,320,326,344):
                        expected=lamp.activation_generation<=gen<END_GENERATION
                        self.assertEqual(target<=state,expected,(lamp.word,gen))
                    state=evolve(state)
                self.assertFalse(state)

    def test_complete_golly_initial_universe_round_trip(self):
        cells=universe()
        text=compact_rle(cells,('real text pilot',))
        restored=parse_rle(text)
        minx=min(x for x,y in cells);miny=min(y for x,y in cells)
        self.assertEqual(restored,{(x-minx,y-miny) for x,y in cells})

    def test_all_350_generations_exact_b3_s23_and_independence(self):
        try:
            import numpy as np
            from scipy.ndimage import convolve
        except ImportError:
            self.skipTest('SciPy fast exact replay unavailable; use pip install scipy')
        parts=components()
        base=set().union(*(v for key,v in parts.items() if not key.startswith('lyric_progress_') and key not in ('bubble_outline','caption_stable_5x7')))
        caption=parts['bubble_outline']|parts['caption_stable_5x7']
        signals=set().union(*(parts[f'lyric_progress_{w.word.lower()}'] for w in LAMPS))
        controlled=caption|signals
        entire=base|controlled
        left,top=-500,-600
        width,height=1700,1250
        kernel=np.ones((3,3),dtype=np.uint8);kernel[1,1]=0
        def grid(cells):
            z=np.zeros((height,width),dtype=np.uint8)
            if cells:
                xx=np.fromiter((x-left for x,y in cells),dtype=np.int32)
                yy=np.fromiter((y-top for x,y in cells),dtype=np.int32)
                self.assertTrue(np.all((xx>4)&(xx<width-5)))
                self.assertTrue(np.all((yy>4)&(yy<height-5)))
                z[yy,xx]=1
            return z
        def step(z):
            n=convolve(z,kernel,mode='constant',cval=0)
            return np.asarray((n==3)|((z!=0)&(n==2)),dtype=np.uint8)
        whole=grid(entire);b=grid(base);c=grid(controlled)
        snapshots={267:(False,False,False,False),
                   268:(True,False,False,False),
                   276:(True,True,False,False),
                   284:(True,True,True,False),
                   288:(True,True,True,True),
                   320:(True,True,True,True),
                   326:(False,False,False,False),
                   345:(False,False,False,False)}
        for gen in range(350):
            self.assertTrue(np.array_equal(whole,b|c),f'cross-component interaction at gen {gen}')
            self.assertFalse(whole[0].any() or whole[-1].any() or whole[:,0].any() or whole[:,-1].any())
            if gen in snapshots:
                states=[]
                for lamp in LAMPS:
                    states.append(all(whole[y-top,x-left] for x,y in lamp_target(lamp)))
                self.assertEqual(tuple(states),snapshots[gen],gen)
            whole=step(whole);b=step(b);c=step(c)

if __name__=='__main__':unittest.main()
