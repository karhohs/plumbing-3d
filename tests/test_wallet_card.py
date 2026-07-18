import tempfile
import unittest
from pathlib import Path

from print_parts_catalog import (
    WalletCardDimensions,
    build_wallet_card,
    export_wallet_card_stl,
    starter_wallet_card_dimensions,
)


def _replace(starter, **overrides):
    fields = dict(
        card_length_mm=starter.card_length_mm,
        card_width_mm=starter.card_width_mm,
        card_thickness_mm=starter.card_thickness_mm,
        corner_radius_mm=starter.corner_radius_mm,
        airtag_pocket_face_diameter_mm=starter.airtag_pocket_face_diameter_mm,
        airtag_pocket_max_diameter_mm=starter.airtag_pocket_max_diameter_mm,
        airtag_wall_clearance_mm=starter.airtag_wall_clearance_mm,
        yubikey_pocket_length_mm=starter.yubikey_pocket_length_mm,
        yubikey_pocket_width_mm=starter.yubikey_pocket_width_mm,
        yubikey_pocket_corner_radius_mm=starter.yubikey_pocket_corner_radius_mm,
        yubikey_shoe_bulge_mm=starter.yubikey_shoe_bulge_mm,
        yubikey_wall_clearance_mm=starter.yubikey_wall_clearance_mm,
        pocket_edge_margin_mm=starter.pocket_edge_margin_mm,
        pocket_spacing_mm=starter.pocket_spacing_mm,
    )
    fields.update(overrides)
    return WalletCardDimensions(**fields)


class WalletCardDimensionsTests(unittest.TestCase):
    def test_starter_dimensions_are_usable(self) -> None:
        dimensions = starter_wallet_card_dimensions()

        self.assertEqual(dimensions.card_length_mm, 77.04)
        self.assertEqual(dimensions.card_width_mm, 48.58)
        self.assertEqual(dimensions.card_thickness_mm, 3.6)
        self.assertEqual(dimensions.corner_radius_mm, 3.18)
        self.assertAlmostEqual(dimensions.airtag_pocket_effective_face_diameter_mm, 29.5, places=6)
        self.assertAlmostEqual(dimensions.airtag_pocket_effective_max_diameter_mm, 31.7, places=6)
        self.assertAlmostEqual(dimensions.yubikey_pocket_effective_length_mm, 42.4, places=6)
        self.assertAlmostEqual(dimensions.yubikey_pocket_effective_width_mm, 17.95, places=6)
        self.assertAlmostEqual(dimensions.yubikey_pocket_effective_max_length_mm, 45.0, places=6)

    def test_starter_geometry_matches_expected_envelope(self) -> None:
        dimensions = starter_wallet_card_dimensions()
        shape = build_wallet_card(dimensions).val()
        bounding_box = shape.BoundingBox()

        self.assertAlmostEqual(bounding_box.xlen, dimensions.card_length_mm, places=6)
        self.assertAlmostEqual(bounding_box.ylen, dimensions.card_width_mm, places=6)
        self.assertAlmostEqual(bounding_box.zlen, dimensions.card_thickness_mm, places=6)

    def test_export_writes_nonempty_stl(self) -> None:
        dimensions = starter_wallet_card_dimensions()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "wallet_card.stl"
            written_path = export_wallet_card_stl(dimensions, str(output_path))

            resolved_path = Path(written_path)
            self.assertTrue(resolved_path.exists())
            self.assertGreater(resolved_path.stat().st_size, 0)

    def test_yubikey_length_exceeding_card_width_raises(self) -> None:
        # The key's long axis (with the shoe) runs along the card's width, not its length.
        starter = starter_wallet_card_dimensions()
        with self.assertRaises(ValueError):
            _replace(starter, yubikey_pocket_length_mm=60.0)

    def test_yubikey_width_breaking_length_layout_raises(self) -> None:
        # The key's short axis runs along the card's length, alongside the AirTag pocket.
        starter = starter_wallet_card_dimensions()
        with self.assertRaises(ValueError):
            _replace(starter, yubikey_pocket_width_mm=60.0)

    def test_airtag_max_diameter_below_face_diameter_raises(self) -> None:
        starter = starter_wallet_card_dimensions()
        with self.assertRaises(ValueError):
            _replace(starter, airtag_pocket_max_diameter_mm=starter.airtag_pocket_face_diameter_mm - 1.0)

    def test_corner_radius_too_large_raises(self) -> None:
        starter = starter_wallet_card_dimensions()
        with self.assertRaises(ValueError):
            _replace(starter, corner_radius_mm=30.0)

    def test_yubikey_pocket_corner_radius_too_large_raises(self) -> None:
        starter = starter_wallet_card_dimensions()
        with self.assertRaises(ValueError):
            _replace(starter, yubikey_pocket_corner_radius_mm=20.0)

    def test_negative_shoe_bulge_raises(self) -> None:
        starter = starter_wallet_card_dimensions()
        with self.assertRaises(ValueError):
            _replace(starter, yubikey_shoe_bulge_mm=-1.0)


if __name__ == "__main__":
    unittest.main()
