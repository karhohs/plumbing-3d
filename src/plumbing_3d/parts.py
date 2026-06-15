from dataclasses import dataclass


@dataclass(frozen=True)
class PipeDimensions:
    outer_diameter_mm: float
    wall_thickness_mm: float
    length_mm: float

    def __post_init__(self) -> None:
        if self.outer_diameter_mm <= 0:
            raise ValueError("outer_diameter_mm must be greater than zero")
        if self.wall_thickness_mm <= 0:
            raise ValueError("wall_thickness_mm must be greater than zero")
        if self.length_mm <= 0:
            raise ValueError("length_mm must be greater than zero")
        if self.inner_diameter_mm <= 0:
            raise ValueError("wall_thickness_mm must leave a positive inner diameter")

    @property
    def inner_diameter_mm(self) -> float:
        return self.outer_diameter_mm - (2 * self.wall_thickness_mm)


def starter_pipe_dimensions() -> PipeDimensions:
    return PipeDimensions(outer_diameter_mm=40.0, wall_thickness_mm=2.0, length_mm=100.0)
