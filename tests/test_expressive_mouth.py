"""Actual whole-universe qualification of toothless open mouth and return."""
import unittest
from life.core import evolve,place,parse_rle
from life.glider_controlled_mouth import BLOCK
from life.expressive_mouth import (
    components,universe,QUALIFICATION_END,START_LINE,LINE_CELLS,
    EXPRESSIVE_CHECKPOINTS,LEFT_EYE_GLINT,RIGHT_EYE_GLINT
)
from life.symmetric_full_mouth import target_blocks

class ExpressiveSingerQualification(unittest.TestCase):
    def test_only_real_life_signals_and_all_composition_independent(self):
        parts=components(with_bubble=True)
        world=universe(with_bubble=True)
        self.assertTrue(len(parts)>40)
        permanent=('outline','eyes_nose','bubble_outline','bubble_lyrics')
        fixed=set().union(*(parts[k] for k in permanent))
        mouth_shapes={state:target_blocks(state) for state in ('medium','open')}
        for g in range(QUALIFICATION_END):
            self.assertEqual(world,set().union(*parts.values()), f'cross-component event at g{g}')
            self.assertTrue(fixed<=world, f'fixed features modified at g{g}')
            if g in EXPRESSIVE_CHECKPOINTS:
                state=EXPRESSIVE_CHECKPOINTS[g]
                if state in mouth_shapes:
                    self.assertTrue(mouth_shapes[state]<=world,(g,state))
                if state=='closed':
                    self.assertTrue(LINE_CELLS<=world,(g,'closed lip missing'))
                else:
                    for pos in START_LINE:
                        self.assertFalse(place(BLOCK,*pos)<=world,(g,'teeth remain',pos))
            world=evolve(world)
            parts={k:evolve(cells) for k,cells in parts.items()}

    def test_two_eye_glints_are_native_period_2_oscillators(self):
        for glint in (LEFT_EYE_GLINT,RIGHT_EYE_GLINT):
            self.assertNotEqual(evolve(glint),glint)
            self.assertEqual(evolve(evolve(glint)),glint)

    def test_end_state_and_closed_line_are_stable(self):
        self.assertEqual(evolve(set(LINE_CELLS)),set(LINE_CELLS))
        self.assertEqual(len(START_LINE),5)
        self.assertEqual(len(LINE_CELLS),20)

if __name__=='__main__': unittest.main()
