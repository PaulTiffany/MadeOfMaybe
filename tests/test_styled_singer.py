"""Native Life proof for a new oval face while the original glider show plays."""
import unittest
from life.core import evolve,place
from life.glider_controlled_mouth import BLOCK
from life.styled_singer import (
    components,universe,prepared_portrait,QUALIFICATION_END,
    LEFT_GLINT,RIGHT_GLINT,ART_TYPES
)
from life.expressive_mouth import LINE_CELLS,EXPRESSIVE_CHECKPOINTS
from life.symmetric_full_mouth import target_blocks

class StyledSingerQualification(unittest.TestCase):
    def test_oval_portrait_is_all_stable_disjoint_life_blocks(self):
        art=prepared_portrait()
        self.assertEqual(set(art),set(ART_TYPES))
        used=set()
        for kind,live in art.items():
            cells=set(live)
            self.assertEqual(evolve(cells),cells,kind)
            self.assertFalse(cells&used,kind)
            self.assertEqual(len(cells)%4,0)
            used|=cells
        self.assertGreaterEqual(len(art['art_eye_liner'] if 'art_eye_liner' in art else art['eye_liner'])//4,30)
        self.assertGreaterEqual(len(art['nose'])//4,5)
        self.assertGreaterEqual(len(art['contour'])//4,75)

    def test_real_eye_glints_are_period_two(self):
        for glint in (LEFT_GLINT,RIGHT_GLINT):
            self.assertEqual(len(glint),3)
            self.assertNotEqual(evolve(glint),glint)
            self.assertEqual(evolve(evolve(glint)),glint)

    def test_one_world_equals_all_independently_evolved_components(self):
        parts=components(True)
        self.assertGreaterEqual(len(parts),50)
        combined=universe(True)
        fixed=set().union(*(cells for key,cells in parts.items() if key.startswith('art_')))
        checkpoints={g:state for g,state in EXPRESSIVE_CHECKPOINTS.items()}
        for gen in range(QUALIFICATION_END):
            self.assertEqual(combined,set().union(*parts.values()),f'cross-component event g{gen}')
            self.assertTrue(fixed <= combined,f'static-face corruption g{gen}')
            if gen in checkpoints:
                state=checkpoints[gen]
                if state in ('medium','open'):
                    self.assertTrue(target_blocks(state)<=combined,(gen,state))
                if state=='closed':
                    self.assertTrue(LINE_CELLS<=combined,(gen,'closed line missing'))
            combined=evolve(combined)
            parts={name:evolve(cells) for name,cells in parts.items()}

    def test_art_shaped_like_oval_not_circle(self):
        cells=prepared_portrait()['contour']
        xs=[x for x,y in cells];ys=[y for x,y in cells]
        self.assertGreater((max(ys)-min(ys))/(max(xs)-min(xs)),1.2)

if __name__=='__main__':unittest.main()
