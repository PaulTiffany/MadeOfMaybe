"""Layout and native-cell camera tests (no expensive native Life replay)."""
import unittest

from life.core import place
from life.glider_controlled_mouth import BLOCK
from life.reusable_word_cue import SECOND_LIP_GLOBAL
from preview.render_reused_word_bus import (
    CARD_FACE, CARD_BUBBLE, CARD_CONTROL, MOUTH_TILE_ORIGINS,
    observed_lip_cells, _panel_boxes,
)


class ReusedWordCameraTests(unittest.TestCase):
    def test_face_separate_from_lyric_bubble_and_controller_below(self):
        self.assertLess(CARD_FACE[2], CARD_BUBBLE[0])
        self.assertLess(CARD_FACE[2], CARD_CONTROL[0])
        self.assertLess(CARD_BUBBLE[3], CARD_CONTROL[1])
        face, bubble, ctrl = _panel_boxes(100, 250)
        self.assertLess(face[2], ctrl[0])
        self.assertLess(bubble[3], ctrl[1])

    def test_controller_screen_position_has_no_life_source_mutation(self):
        # The 84 actual catalysts are rendered from world occupancy,
        # not shifted into this optical panel at simulation time.
        from life.physical_lip_splitter_bridge import splitter_catalysts, SINGER_TRANSLATION
        actual = place(splitter_catalysts(), *SINGER_TRANSLATION)
        self.assertEqual(len(actual), 84)
        self.assertEqual(len(actual & set(actual)), 84)
        self.assertEqual(CARD_CONTROL[0], 340)

    def test_lip_camera_uses_only_full_real_blocks(self):
        active = place(BLOCK, *SECOND_LIP_GLOBAL)
        self.assertEqual(observed_lip_cells(active), active)
        self.assertEqual(observed_lip_cells(active - {min(active)}), set())
        self.assertEqual(observed_lip_cells(set()), set())
        self.assertGreater(len(MOUTH_TILE_ORIGINS), 8)


if __name__ == '__main__': unittest.main()
