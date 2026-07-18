"""Parametric wallet card insert that holds a YubiKey 5C and an Apple AirTag.

Design approach:
- This is a thin card with cavities cut almost fully through it, not a thick block with floored
  pockets. Each cavity necks in at the top/bottom faces and bulges out at mid-thickness, so items
  are gripped by friction/flex against that necked profile rather than resting in a recess.
- The AirTag cavity is a lofted ellipsoid-of-revolution (narrow at both faces, wide in the
  middle), matching the AirTag's own rounded edge profile.
- The YubiKey cavity is a straight slot with one end left open (untapered) and the other end
  carrying a small necked/bulged "shoe" that catches the key so it can't slide back out. The
  key's long axis (with the shoe) runs along the card's width, not its length: a standard-size
  card is too thick for a typical wallet slot without flexing/squeezing, so the footprint is
  scaled down to 90% of a standard ID/credit card. That shorter length can't fit both cavities
  side-by-side if the key is oriented along the length (do the math: it needs ~84mm at minimum,
  more than the 90%-scaled ~77mm length gives) — orienting it along the width instead is required
  to fit, even though it's the structurally weaker orientation at that cross-section.
- Starter dimensions are measured from a reference STL of a known, previously-printed design
  (not re-derived from raw hardware specs), so wall_clearance fields default to 0mm — the
  measured cavity sizes are already the target sizes, not raw item dimensions needing clearance
  added. Verify against your actual hardware before finalizing a print.
- Print with the card flat on the bed (thickness along Z) so the necking profile is a shallow
  internal overhang within typical FDM tolerance, and prefer a print material with some flex
  (e.g. PETG) over a stiff one (e.g. PLA), since retention relies on the walls flexing slightly
  during insertion.
"""

import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WalletCardDimensions:
    card_length_mm: float
    card_width_mm: float
    card_thickness_mm: float
    corner_radius_mm: float
    airtag_pocket_face_diameter_mm: float
    airtag_pocket_max_diameter_mm: float
    airtag_wall_clearance_mm: float
    yubikey_pocket_length_mm: float
    yubikey_pocket_width_mm: float
    yubikey_pocket_corner_radius_mm: float
    yubikey_shoe_bulge_mm: float
    yubikey_wall_clearance_mm: float
    pocket_edge_margin_mm: float
    pocket_spacing_mm: float

    def __post_init__(self) -> None:
        if self.card_length_mm <= 0:
            raise ValueError("card_length_mm must be greater than zero")
        if self.card_width_mm <= 0:
            raise ValueError("card_width_mm must be greater than zero")
        if self.card_thickness_mm <= 0:
            raise ValueError("card_thickness_mm must be greater than zero")
        if self.corner_radius_mm < 0:
            raise ValueError("corner_radius_mm must be greater than or equal to zero")
        if self.corner_radius_mm >= min(self.card_length_mm, self.card_width_mm) / 2:
            raise ValueError("corner_radius_mm must be less than half the shorter card dimension")
        if self.airtag_pocket_face_diameter_mm <= 0:
            raise ValueError("airtag_pocket_face_diameter_mm must be greater than zero")
        if self.airtag_pocket_max_diameter_mm <= 0:
            raise ValueError("airtag_pocket_max_diameter_mm must be greater than zero")
        if self.airtag_pocket_max_diameter_mm < self.airtag_pocket_face_diameter_mm:
            raise ValueError(
                "airtag_pocket_max_diameter_mm must be greater than or equal to "
                "airtag_pocket_face_diameter_mm to form a retention bulge"
            )
        if self.airtag_wall_clearance_mm < 0:
            raise ValueError("airtag_wall_clearance_mm must be greater than or equal to zero")
        if self.yubikey_pocket_length_mm <= 0:
            raise ValueError("yubikey_pocket_length_mm must be greater than zero")
        if self.yubikey_pocket_width_mm <= 0:
            raise ValueError("yubikey_pocket_width_mm must be greater than zero")
        if self.yubikey_pocket_corner_radius_mm < 0:
            raise ValueError("yubikey_pocket_corner_radius_mm must be greater than or equal to zero")
        if self.yubikey_pocket_corner_radius_mm >= min(self.yubikey_pocket_length_mm, self.yubikey_pocket_width_mm) / 2:
            raise ValueError("yubikey_pocket_corner_radius_mm must be less than half the shorter pocket dimension")
        if self.yubikey_shoe_bulge_mm < 0:
            raise ValueError("yubikey_shoe_bulge_mm must be greater than or equal to zero")
        if self.yubikey_wall_clearance_mm < 0:
            raise ValueError("yubikey_wall_clearance_mm must be greater than or equal to zero")
        if self.pocket_edge_margin_mm < 0:
            raise ValueError("pocket_edge_margin_mm must be greater than or equal to zero")
        if self.pocket_spacing_mm < 0:
            raise ValueError("pocket_spacing_mm must be greater than or equal to zero")
        if self.yubikey_pocket_effective_max_length_mm + (2 * self.pocket_edge_margin_mm) > self.card_width_mm:
            raise ValueError(
                "yubikey pocket max length (including the shoe) plus edge margins must not "
                "exceed card_width_mm"
            )
        if self.airtag_pocket_effective_max_diameter_mm + (2 * self.pocket_edge_margin_mm) > self.card_width_mm:
            raise ValueError("airtag pocket max diameter plus edge margins must not exceed card_width_mm")
        if self.pockets_occupied_length_mm + (2 * self.pocket_edge_margin_mm) > self.card_length_mm:
            raise ValueError(
                "yubikey pocket width, airtag pocket max diameter, and pocket spacing, plus "
                "edge margins on both sides, must not exceed card_length_mm"
            )

    @property
    def airtag_pocket_effective_face_diameter_mm(self) -> float:
        return self.airtag_pocket_face_diameter_mm + (2 * self.airtag_wall_clearance_mm)

    @property
    def airtag_pocket_effective_max_diameter_mm(self) -> float:
        return self.airtag_pocket_max_diameter_mm + (2 * self.airtag_wall_clearance_mm)

    @property
    def yubikey_pocket_effective_length_mm(self) -> float:
        return self.yubikey_pocket_length_mm + (2 * self.yubikey_wall_clearance_mm)

    @property
    def yubikey_pocket_effective_width_mm(self) -> float:
        return self.yubikey_pocket_width_mm + (2 * self.yubikey_wall_clearance_mm)

    @property
    def yubikey_pocket_effective_max_length_mm(self) -> float:
        return self.yubikey_pocket_effective_length_mm + self.yubikey_shoe_bulge_mm

    @property
    def pockets_occupied_length_mm(self) -> float:
        return (
            self.yubikey_pocket_effective_width_mm
            + self.pocket_spacing_mm
            + self.airtag_pocket_effective_max_diameter_mm
        )

    @property
    def yubikey_pocket_center_x_mm(self) -> float:
        return (-self.pockets_occupied_length_mm / 2) + (self.yubikey_pocket_effective_width_mm / 2)

    @property
    def airtag_pocket_center_x_mm(self) -> float:
        return (self.pockets_occupied_length_mm / 2) - (self.airtag_pocket_effective_max_diameter_mm / 2)


def starter_wallet_card_dimensions() -> WalletCardDimensions:
    return WalletCardDimensions(
        # 90% of a standard ID/credit-card footprint (85.60 x 53.98mm) — a full-size card is too
        # thick here (3.6mm vs ~0.76mm) to sit in a typical wallet slot without flexing/squeezing
        # the slot open, so the footprint is scaled down to compensate.
        card_length_mm=77.04,
        card_width_mm=48.58,
        card_thickness_mm=3.6,
        corner_radius_mm=3.18,
        airtag_pocket_face_diameter_mm=29.5,
        airtag_pocket_max_diameter_mm=31.7,
        airtag_wall_clearance_mm=0.0,
        yubikey_pocket_length_mm=42.4,
        yubikey_pocket_width_mm=17.95,
        yubikey_pocket_corner_radius_mm=1.5,
        yubikey_shoe_bulge_mm=2.6,
        yubikey_wall_clearance_mm=0.0,
        # Trimmed from 2.0mm: at the 90%-scaled card_width_mm, the YubiKey's length (with its
        # shoe) leaves only ~1.79mm of margin on each side to work with.
        pocket_edge_margin_mm=1.7,
        pocket_spacing_mm=3.0,
    )


def _bulge_samples(face_value: float, max_value: float, thickness: float, sample_count: int = 5):
    """Sample count points from z=0 to z=thickness following a sine bulge: face_value at both
    ends, max_value at mid-thickness. Used for both the AirTag radius taper and the YubiKey
    shoe's length taper."""
    return [
        (
            thickness * i / (sample_count - 1),
            face_value + (max_value - face_value) * math.sin(math.pi * i / (sample_count - 1)),
        )
        for i in range(sample_count)
    ]


def _lofted_bulge_cylinder(cq, center_xy, face_radius: float, max_radius: float, thickness: float):
    workplane = cq.Workplane("XY").center(*center_xy)
    previous_z = 0.0
    for z, radius in _bulge_samples(face_radius, max_radius, thickness):
        workplane = workplane.workplane(offset=z - previous_z).circle(radius)
        previous_z = z
    return workplane.loft(combine=True)


def _yubikey_slot_cutter(cq, dimensions: WalletCardDimensions):
    # The key's long axis (with the shoe) runs along Y (the card's width), not X (the card's
    # length) — see the module docstring for why: a length-oriented key doesn't fit the
    # 90%-scaled card footprint.
    center_x = dimensions.yubikey_pocket_center_x_mm
    width = dimensions.yubikey_pocket_effective_width_mm
    length = dimensions.yubikey_pocket_effective_length_mm
    thickness = dimensions.card_thickness_mm

    slot = (
        cq.Workplane("XY")
        .center(center_x, 0)
        .rect(width, length)
        .extrude(thickness)
        .edges("|Z")
        .fillet(dimensions.yubikey_pocket_corner_radius_mm)
    )

    # The shoe necks the slot's +Y end outward at mid-thickness, catching that end of the key.
    outer_edge_y = length / 2
    overlap_mm = min(6.0, length / 2)
    inner_edge_y = outer_edge_y - overlap_mm

    shoe = cq.Workplane("XY").center(center_x, 0)
    previous_z = 0.0
    previous_center = 0.0
    for z, bulge in _bulge_samples(0.0, dimensions.yubikey_shoe_bulge_mm, thickness):
        bulged_edge_y = outer_edge_y + bulge
        segment_center = (inner_edge_y + bulged_edge_y) / 2
        segment_length = bulged_edge_y - inner_edge_y
        shoe = shoe.workplane(offset=z - previous_z).center(0, segment_center - previous_center).rect(width, segment_length)
        previous_z = z
        previous_center = segment_center
    shoe_cutter = shoe.loft(combine=True)

    return slot.union(shoe_cutter)


def build_wallet_card(dimensions: WalletCardDimensions):
    import cadquery as cq

    card = (
        cq.Workplane("XY")
        .rect(dimensions.card_length_mm, dimensions.card_width_mm)
        .extrude(dimensions.card_thickness_mm)
        .edges("|Z")
        .fillet(dimensions.corner_radius_mm)
    )

    airtag_cutter = _lofted_bulge_cylinder(
        cq,
        center_xy=(dimensions.airtag_pocket_center_x_mm, 0),
        face_radius=dimensions.airtag_pocket_effective_face_diameter_mm / 2,
        max_radius=dimensions.airtag_pocket_effective_max_diameter_mm / 2,
        thickness=dimensions.card_thickness_mm,
    )
    card = card.cut(airtag_cutter)

    yubikey_cutter = _yubikey_slot_cutter(cq, dimensions)
    card = card.cut(yubikey_cutter)

    return card


def export_wallet_card_stl(dimensions: WalletCardDimensions, file_path: str) -> str:
    from cadquery import exporters

    output_path = Path(file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    card = build_wallet_card(dimensions)
    exporters.export(card, str(output_path))

    return str(output_path)
