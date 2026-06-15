import unittest

from plumbing_3d import PipeDimensions, starter_pipe_dimensions


class PipeDimensionsTests(unittest.TestCase):
    def test_starter_dimensions_are_usable(self) -> None:
        dimensions = starter_pipe_dimensions()

        self.assertEqual(dimensions.outer_diameter_mm, 40.0)
        self.assertEqual(dimensions.inner_diameter_mm, 36.0)
        self.assertEqual(dimensions.length_mm, 100.0)

    def test_invalid_dimensions_raise(self) -> None:
        with self.assertRaises(ValueError):
            PipeDimensions(outer_diameter_mm=10.0, wall_thickness_mm=5.5, length_mm=25.0)


if __name__ == "__main__":
    unittest.main()
