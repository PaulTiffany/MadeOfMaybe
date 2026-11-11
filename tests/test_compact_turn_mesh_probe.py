"""Real collision sweep: does a simple stagger protect seven LWSS turners?"""
import unittest
from life.compact_turn_mesh_probe import (
    components,first_interference,qualify,ROW_COUNT,ROW_PITCH,X_STEP
)

class CompactTurnMeshProbeTests(unittest.TestCase):
    def test_dense_stacked_station_collides_immediately(self):
        self.assertEqual(first_interference(row_pitch=8,x_step=0,until=40),1)

    def test_simple_alternating_checkerboard_still_interacts(self):
        self.assertEqual(first_interference(
            row_pitch=8,x_step=-24,offsets=(0,-24,0,-24,0,-24,0),
            until=40),1)

    def test_small_vertical_expansion_without_stagger_is_not_enough(self):
        self.assertEqual(first_interference(row_pitch=18,x_step=0,
                                            until=250),190)

    def test_one_row_one_cell_spaced_staircase_is_independent_and_aligned(self):
        c=qualify()
        self.assertEqual((c['row_pitch'],c['horizontal_step_per_row']),(18,-36))
        self.assertEqual(c['native_generations_checked'],3200)
        self.assertEqual(len(c['output_rows']),7)
        self.assertTrue(c['whole_world_equals_independent_rows_at_each_tick'])
        self.assertFalse(c['corner_is_reusable'])
        self.assertFalse(c['complete_word_compacted'])

    def test_source_ablation_removes_only_one_aligned_output(self):
        c=qualify(enabled=(0,1,2,3,4,5))
        self.assertEqual(set(c['output_rows']),set(map(str,range(6))))
        self.assertEqual(len(components()),7)

if __name__=='__main__': unittest.main()
