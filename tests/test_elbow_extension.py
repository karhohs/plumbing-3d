import tempfile
import unittest
from pathlib import Path

from print_parts_catalog import (
    ElbowExtensionDimensions,
    build_elbow_extension,
    export_elbow_extension_stl,
    starter_elbow_extension_dimensions,
)


class ElbowExtensionDimensionsTests(unittest.TestCase):
    def test_starter_dimensions_are_usable(self) -> None:
        dimensions = starter_elbow_extension_dimensions()

        self.assertEqual(dimensions.insert_outer_diameter_mm, 33.0)
        self.assertEqual(dimensions.insert_inner_diameter_mm, 27.0)
        self.assertEqual(dimensions.body_outer_diameter_mm, 38.0)
        self.assertEqual(dimensions.inner_diameter_mm, 33.0)
        self.assertEqual(dimensions.insert_wall_thickness_mm, 3.0)
        self.assertEqual(dimensions.insert_depth_mm, 13.0)
        self.assertEqual(dimensions.extension_length_mm, 25.0)
        self.assertEqual(dimensions.inner_transition_straight_length_mm, 5.0)
        self.assertEqual(dimensions.inner_transition_ramp_length_mm, 5.0)
        self.assertEqual(dimensions.total_straight_length_mm, 38.0)
        self.assertFalse(dimensions.has_o_ring_groove)
        self.assertEqual(dimensions.end_bead_outer_diameter_mm, 40.0)
        self.assertEqual(dimensions.end_bead_thickness_mm, 1.0)
        self.assertEqual(dimensions.o_ring_groove_width_mm, 1.8)
        self.assertEqual(dimensions.o_ring_groove_depth_mm, 1.3)
        self.assertEqual(dimensions.o_ring_groove_backset_from_flange_mm, 2.0)

    def test_starter_geometry_matches_expected_envelope(self) -> None:
        dimensions = starter_elbow_extension_dimensions()
        shape = build_elbow_extension(dimensions).val()
        bounding_box = shape.BoundingBox()

        self.assertAlmostEqual(bounding_box.xlen, dimensions.end_bead_outer_diameter_mm, places=6)
        self.assertAlmostEqual(bounding_box.ylen, dimensions.end_bead_outer_diameter_mm, places=6)
        self.assertAlmostEqual(bounding_box.zlen, dimensions.total_straight_length_mm, places=6)

    def test_export_writes_nonempty_stl(self) -> None:
        dimensions = starter_elbow_extension_dimensions()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "elbow_extension.stl"
            written_path = export_elbow_extension_stl(dimensions, str(output_path))

            resolved_path = Path(written_path)
            self.assertTrue(resolved_path.exists())
            self.assertGreater(resolved_path.stat().st_size, 0)

    def test_build_with_enabled_o_ring_groove(self) -> None:
        starter = starter_elbow_extension_dimensions()
        dimensions = ElbowExtensionDimensions(
            insert_outer_diameter_mm=starter.insert_outer_diameter_mm,
            insert_inner_diameter_mm=starter.insert_inner_diameter_mm,
            body_outer_diameter_mm=starter.body_outer_diameter_mm,
            wall_thickness_mm=starter.wall_thickness_mm,
            insert_depth_mm=starter.insert_depth_mm,
            extension_length_mm=starter.extension_length_mm,
            inner_transition_straight_length_mm=starter.inner_transition_straight_length_mm,
            inner_transition_ramp_length_mm=starter.inner_transition_ramp_length_mm,
            end_bead_outer_diameter_mm=starter.end_bead_outer_diameter_mm,
            end_bead_thickness_mm=starter.end_bead_thickness_mm,
            o_ring_groove_width_mm=starter.o_ring_groove_width_mm,
            o_ring_groove_depth_mm=starter.o_ring_groove_depth_mm,
            o_ring_groove_backset_from_flange_mm=starter.o_ring_groove_backset_from_flange_mm,
            o_ring_groove_enabled=True,
        )

        shape = build_elbow_extension(dimensions).val()
        self.assertGreater(shape.Volume(), 0)

    def test_inner_transition_segments_must_fit_in_extension(self) -> None:
        with self.assertRaises(ValueError):
            ElbowExtensionDimensions(
                insert_outer_diameter_mm=33.0,
                insert_inner_diameter_mm=29.0,
                body_outer_diameter_mm=38.0,
                wall_thickness_mm=2.5,
                insert_depth_mm=10.0,
                extension_length_mm=5.0,
                inner_transition_straight_length_mm=3.0,
                inner_transition_ramp_length_mm=14.0,
                end_bead_outer_diameter_mm=40.0,
                end_bead_thickness_mm=2.0,
            )

    def test_end_bead_must_be_at_least_main_body_diameter(self) -> None:
        with self.assertRaises(ValueError):
            ElbowExtensionDimensions(
                insert_outer_diameter_mm=33.0,
                insert_inner_diameter_mm=29.0,
                body_outer_diameter_mm=38.0,
                wall_thickness_mm=2.5,
                insert_depth_mm=18.0,
                extension_length_mm=20.0,
                inner_transition_straight_length_mm=3.0,
                inner_transition_ramp_length_mm=3.0,
                end_bead_outer_diameter_mm=37.5,
                end_bead_thickness_mm=2.0,
            )

    def test_o_ring_groove_depth_must_be_less_than_wall(self) -> None:
        with self.assertRaises(ValueError):
            ElbowExtensionDimensions(
                insert_outer_diameter_mm=33.0,
                insert_inner_diameter_mm=29.0,
                body_outer_diameter_mm=38.0,
                wall_thickness_mm=2.5,
                insert_depth_mm=18.0,
                extension_length_mm=20.0,
                inner_transition_straight_length_mm=3.0,
                inner_transition_ramp_length_mm=3.0,
                end_bead_outer_diameter_mm=40.0,
                end_bead_thickness_mm=2.0,
                o_ring_groove_width_mm=2.4,
                o_ring_groove_depth_mm=2.5,
                o_ring_groove_backset_from_flange_mm=1.0,
                o_ring_groove_enabled=True,
            )

    def test_o_ring_groove_must_fit_in_insert_section(self) -> None:
        with self.assertRaises(ValueError):
            ElbowExtensionDimensions(
                insert_outer_diameter_mm=33.0,
                insert_inner_diameter_mm=29.0,
                body_outer_diameter_mm=38.0,
                wall_thickness_mm=2.5,
                insert_depth_mm=18.0,
                extension_length_mm=20.0,
                inner_transition_straight_length_mm=3.0,
                inner_transition_ramp_length_mm=3.0,
                end_bead_outer_diameter_mm=40.0,
                end_bead_thickness_mm=2.0,
                o_ring_groove_width_mm=5.0,
                o_ring_groove_depth_mm=1.0,
                o_ring_groove_backset_from_flange_mm=14.0,
                o_ring_groove_enabled=True,
            )

    def test_invalid_inner_diameter_raises(self) -> None:
        with self.assertRaises(ValueError):
            ElbowExtensionDimensions(
                insert_outer_diameter_mm=20.0,
                insert_inner_diameter_mm=19.0,
                body_outer_diameter_mm=20.0,
                wall_thickness_mm=10.5,
                insert_depth_mm=10.0,
                extension_length_mm=10.0,
                inner_transition_straight_length_mm=3.0,
                inner_transition_ramp_length_mm=3.0,
                end_bead_outer_diameter_mm=22.0,
                end_bead_thickness_mm=1.0,
            )

    def test_invalid_end_bead_thickness_raises(self) -> None:
        with self.assertRaises(ValueError):
            ElbowExtensionDimensions(
                insert_outer_diameter_mm=33.0,
                insert_inner_diameter_mm=29.0,
                body_outer_diameter_mm=30.0,
                wall_thickness_mm=2.0,
                insert_depth_mm=10.0,
                extension_length_mm=8.0,
                inner_transition_straight_length_mm=3.0,
                inner_transition_ramp_length_mm=3.0,
                end_bead_outer_diameter_mm=32.0,
                end_bead_thickness_mm=19.0,
            )


if __name__ == "__main__":
    unittest.main()