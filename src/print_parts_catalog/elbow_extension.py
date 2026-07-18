"""Parametric elbow extension insert for garbage disposal plumbing.

Installation guidance:
- Print the extension with your selected extension length variant.
- Insert the printed part into the elbow to the target insertion depth.
- Expect a somewhat tight fit inside the elbow by design.
- Use plumber's grease as the first assembly aid.
- If grease is not sufficient for sealing, apply RTV as needed.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ElbowExtensionDimensions:
    insert_outer_diameter_mm: float
    insert_inner_diameter_mm: float
    body_outer_diameter_mm: float
    wall_thickness_mm: float
    insert_depth_mm: float
    extension_length_mm: float
    inner_transition_straight_length_mm: float
    inner_transition_ramp_length_mm: float
    end_bead_outer_diameter_mm: float
    end_bead_thickness_mm: float
    o_ring_groove_width_mm: float = 0.0
    o_ring_groove_depth_mm: float = 0.0
    o_ring_groove_backset_from_flange_mm: float = 0.0
    o_ring_groove_enabled: bool = False

    def __post_init__(self) -> None:
        if self.insert_outer_diameter_mm <= 0:
            raise ValueError("insert_outer_diameter_mm must be greater than zero")
        if self.insert_inner_diameter_mm <= 0:
            raise ValueError("insert_inner_diameter_mm must be greater than zero")
        if self.insert_inner_diameter_mm >= self.insert_outer_diameter_mm:
            raise ValueError("insert_inner_diameter_mm must be less than insert_outer_diameter_mm")
        if self.body_outer_diameter_mm <= 0:
            raise ValueError("body_outer_diameter_mm must be greater than zero")
        if self.wall_thickness_mm <= 0:
            raise ValueError("wall_thickness_mm must be greater than zero")
        if self.insert_depth_mm <= 0:
            raise ValueError("insert_depth_mm must be greater than zero")
        if self.extension_length_mm <= 0:
            raise ValueError("extension_length_mm must be greater than zero")
        if self.inner_transition_straight_length_mm < 0:
            raise ValueError("inner_transition_straight_length_mm must be greater than or equal to zero")
        if self.inner_transition_straight_length_mm > self.extension_length_mm:
            raise ValueError("inner_transition_straight_length_mm must be less than or equal to extension_length_mm")
        if self.inner_transition_ramp_length_mm < 0:
            raise ValueError("inner_transition_ramp_length_mm must be greater than or equal to zero")
        if self.inner_transition_straight_length_mm + self.inner_transition_ramp_length_mm > self.extension_length_mm:
            raise ValueError(
                "inner transition straight length plus ramp length must be less than or equal to extension_length_mm"
            )
        if self.end_bead_outer_diameter_mm <= 0:
            raise ValueError("end_bead_outer_diameter_mm must be greater than zero")
        if self.end_bead_thickness_mm <= 0:
            raise ValueError("end_bead_thickness_mm must be greater than zero")
        if self.inner_diameter_mm <= 0:
            raise ValueError("wall_thickness_mm must leave a positive inner diameter")
        if self.end_bead_outer_diameter_mm < max(self.body_outer_diameter_mm, self.insert_outer_diameter_mm):
            raise ValueError("end_bead_outer_diameter_mm must be at least the larger of body and insert diameters")
        if self.end_bead_thickness_mm > self.total_straight_length_mm:
            raise ValueError("end_bead_thickness_mm must be less than or equal to total straight length")
        if self.o_ring_groove_enabled:
            if self.o_ring_groove_width_mm < 0:
                raise ValueError("o_ring_groove_width_mm must be greater than or equal to zero")
            if self.o_ring_groove_depth_mm < 0:
                raise ValueError("o_ring_groove_depth_mm must be greater than or equal to zero")
            if self.o_ring_groove_backset_from_flange_mm < 0:
                raise ValueError("o_ring_groove_backset_from_flange_mm must be greater than or equal to zero")
            if self.o_ring_groove_width_mm <= 0:
                raise ValueError("o_ring_groove_width_mm must be greater than zero when O-ring groove is enabled")
            if self.o_ring_groove_depth_mm <= 0:
                raise ValueError("o_ring_groove_depth_mm must be greater than zero when O-ring groove is enabled")
            if self.o_ring_groove_depth_mm >= self.insert_wall_thickness_mm:
                raise ValueError("o_ring_groove_depth_mm must be less than insert wall thickness")
            if self.o_ring_groove_backset_from_flange_mm + self.o_ring_groove_width_mm > self.insert_depth_mm:
                raise ValueError("O-ring groove must fit inside the insertion section")

    @property
    def inner_diameter_mm(self) -> float:
        return self.body_outer_diameter_mm - (2 * self.wall_thickness_mm)

    @property
    def total_straight_length_mm(self) -> float:
        return self.insert_depth_mm + self.extension_length_mm

    @property
    def insert_wall_thickness_mm(self) -> float:
        return (self.insert_outer_diameter_mm - self.insert_inner_diameter_mm) / 2

    @property
    def has_o_ring_groove(self) -> bool:
        return self.o_ring_groove_enabled

def starter_elbow_extension_dimensions() -> ElbowExtensionDimensions:
    return ElbowExtensionDimensions(
        insert_outer_diameter_mm=33.0,
        insert_inner_diameter_mm=27.0,
        body_outer_diameter_mm=38.0,
        wall_thickness_mm=2.5,
        insert_depth_mm=13.0,
        extension_length_mm=25.0,
        inner_transition_straight_length_mm=5.0,
        inner_transition_ramp_length_mm=5.0,
        end_bead_outer_diameter_mm=40.0,
        end_bead_thickness_mm=1.0,
        o_ring_groove_width_mm=1.8,
        o_ring_groove_depth_mm=1.3,
        o_ring_groove_backset_from_flange_mm=2.0,
        o_ring_groove_enabled=False,
    )


def build_elbow_extension(dimensions: ElbowExtensionDimensions):
    import cadquery as cq

    insert_outer = (
        cq.Workplane("XY")
        .circle(dimensions.insert_outer_diameter_mm / 2)
        .extrude(dimensions.insert_depth_mm)
    )

    extension_outer = (
        cq.Workplane("XY")
        .workplane(offset=dimensions.insert_depth_mm)
        .circle(dimensions.body_outer_diameter_mm / 2)
        .extrude(dimensions.extension_length_mm)
    )

    extension = insert_outer.union(extension_outer)

    inner_transition_straight_end_mm = dimensions.insert_depth_mm + dimensions.inner_transition_straight_length_mm
    insert_bore = (
        cq.Workplane("XY")
        .circle(dimensions.insert_inner_diameter_mm / 2)
        .extrude(inner_transition_straight_end_mm)
    )
    extension = extension.cut(insert_bore)

    if dimensions.inner_transition_ramp_length_mm > 0:
        ramp_start_mm = inner_transition_straight_end_mm
        inner_transition_cutter = (
            cq.Workplane("XY")
            .workplane(offset=ramp_start_mm)
            .circle(dimensions.insert_inner_diameter_mm / 2)
            .workplane(offset=dimensions.inner_transition_ramp_length_mm)
            .circle(dimensions.inner_diameter_mm / 2)
            .loft(combine=True)
        )
        extension = extension.cut(inner_transition_cutter)

    body_bore_start_mm = inner_transition_straight_end_mm + dimensions.inner_transition_ramp_length_mm
    body_bore_length_mm = dimensions.total_straight_length_mm - body_bore_start_mm
    if body_bore_length_mm > 0:
        body_bore = (
            cq.Workplane("XY")
            .workplane(offset=body_bore_start_mm)
            .circle(dimensions.inner_diameter_mm / 2)
            .extrude(body_bore_length_mm)
        )
        extension = extension.cut(body_bore)

    if dimensions.has_o_ring_groove:
        groove_center_z_mm = (
            dimensions.insert_depth_mm
            - dimensions.o_ring_groove_backset_from_flange_mm
            - (dimensions.o_ring_groove_width_mm / 2)
        )

        # Build a circular groove profile that matches the requested surface width and radial depth.
        half_width_mm = dimensions.o_ring_groove_width_mm / 2
        groove_depth_mm = dimensions.o_ring_groove_depth_mm
        groove_minor_radius_mm = ((half_width_mm * half_width_mm) + (groove_depth_mm * groove_depth_mm)) / (
            2 * groove_depth_mm
        )

        groove_outer_radius_mm = dimensions.insert_outer_diameter_mm / 2
        groove_center_radius_mm = groove_outer_radius_mm - groove_depth_mm + groove_minor_radius_mm
        o_ring_groove_cutter = cq.Workplane(
            obj=cq.Solid.makeTorus(groove_center_radius_mm, groove_minor_radius_mm)
            .translate((0, 0, groove_center_z_mm))
        )
        extension = extension.cut(o_ring_groove_cutter)

    end_bead_start_mm = dimensions.total_straight_length_mm - dimensions.end_bead_thickness_mm
    end_bead = (
        cq.Workplane("XY")
        .workplane(offset=end_bead_start_mm)
        .circle(dimensions.end_bead_outer_diameter_mm / 2)
        .circle(dimensions.inner_diameter_mm / 2)
        .extrude(dimensions.end_bead_thickness_mm)
    )
    return extension.union(end_bead)


def export_elbow_extension_stl(dimensions: ElbowExtensionDimensions, file_path: str) -> str:
    from cadquery import exporters

    output_path = Path(file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    extension = build_elbow_extension(dimensions)
    exporters.export(extension, str(output_path))

    return str(output_path)