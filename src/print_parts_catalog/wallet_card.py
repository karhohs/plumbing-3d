"""Parametric wallet card insert that holds a YubiKey 5C and an Apple AirTag.

Fit guidance:
- Starter pocket dimensions are based on published specs (Yubico YubiKey 5C, Apple AirTag)
  and should be verified against your actual hardware with calipers before finalizing a print.
- The card footprint matches a standard ID/credit card (85.60 x 53.98mm), but the card is
  thicker than a standard card by design since it has to fully house an 8mm-thick AirTag.
  Check the starter thickness against your specific wallet's card slots before relying on it.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WalletCardDimensions:
    card_length_mm: float
    card_width_mm: float
    card_thickness_mm: float
    corner_radius_mm: float
    floor_thickness_mm: float
    yubikey_pocket_length_mm: float
    yubikey_pocket_width_mm: float
    yubikey_pocket_depth_mm: float
    yubikey_wall_clearance_mm: float
    airtag_pocket_diameter_mm: float
    airtag_pocket_depth_mm: float
    airtag_wall_clearance_mm: float
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
        if self.floor_thickness_mm <= 0:
            raise ValueError("floor_thickness_mm must be greater than zero")
        if self.yubikey_pocket_length_mm <= 0:
            raise ValueError("yubikey_pocket_length_mm must be greater than zero")
        if self.yubikey_pocket_width_mm <= 0:
            raise ValueError("yubikey_pocket_width_mm must be greater than zero")
        if self.yubikey_pocket_depth_mm <= 0:
            raise ValueError("yubikey_pocket_depth_mm must be greater than zero")
        if self.yubikey_wall_clearance_mm < 0:
            raise ValueError("yubikey_wall_clearance_mm must be greater than or equal to zero")
        if self.airtag_pocket_diameter_mm <= 0:
            raise ValueError("airtag_pocket_diameter_mm must be greater than zero")
        if self.airtag_pocket_depth_mm <= 0:
            raise ValueError("airtag_pocket_depth_mm must be greater than zero")
        if self.airtag_wall_clearance_mm < 0:
            raise ValueError("airtag_wall_clearance_mm must be greater than or equal to zero")
        if self.pocket_edge_margin_mm < 0:
            raise ValueError("pocket_edge_margin_mm must be greater than or equal to zero")
        if self.pocket_spacing_mm < 0:
            raise ValueError("pocket_spacing_mm must be greater than or equal to zero")
        if self.yubikey_pocket_depth_mm + self.floor_thickness_mm > self.card_thickness_mm:
            raise ValueError("yubikey_pocket_depth_mm plus floor_thickness_mm must not exceed card_thickness_mm")
        if self.airtag_pocket_depth_mm + self.floor_thickness_mm > self.card_thickness_mm:
            raise ValueError("airtag_pocket_depth_mm plus floor_thickness_mm must not exceed card_thickness_mm")
        if self.yubikey_pocket_effective_width_mm + (2 * self.pocket_edge_margin_mm) > self.card_width_mm:
            raise ValueError("yubikey pocket width plus edge margins must not exceed card_width_mm")
        if self.airtag_pocket_effective_diameter_mm + (2 * self.pocket_edge_margin_mm) > self.card_width_mm:
            raise ValueError("airtag pocket diameter plus edge margins must not exceed card_width_mm")
        if self.pockets_occupied_length_mm + (2 * self.pocket_edge_margin_mm) > self.card_length_mm:
            raise ValueError(
                "yubikey pocket length, airtag pocket diameter, and pocket spacing, plus edge "
                "margins on both sides, must not exceed card_length_mm"
            )

    @property
    def yubikey_pocket_effective_length_mm(self) -> float:
        return self.yubikey_pocket_length_mm + (2 * self.yubikey_wall_clearance_mm)

    @property
    def yubikey_pocket_effective_width_mm(self) -> float:
        return self.yubikey_pocket_width_mm + (2 * self.yubikey_wall_clearance_mm)

    @property
    def airtag_pocket_effective_diameter_mm(self) -> float:
        return self.airtag_pocket_diameter_mm + (2 * self.airtag_wall_clearance_mm)

    @property
    def pockets_occupied_length_mm(self) -> float:
        return (
            self.yubikey_pocket_effective_length_mm
            + self.pocket_spacing_mm
            + self.airtag_pocket_effective_diameter_mm
        )

    @property
    def yubikey_pocket_center_x_mm(self) -> float:
        return (-self.pockets_occupied_length_mm / 2) + (self.yubikey_pocket_effective_length_mm / 2)

    @property
    def airtag_pocket_center_x_mm(self) -> float:
        return (self.pockets_occupied_length_mm / 2) - (self.airtag_pocket_effective_diameter_mm / 2)


def starter_wallet_card_dimensions() -> WalletCardDimensions:
    return WalletCardDimensions(
        card_length_mm=85.60,
        card_width_mm=53.98,
        card_thickness_mm=9.0,
        corner_radius_mm=3.18,
        floor_thickness_mm=1.2,
        yubikey_pocket_length_mm=45.0,
        yubikey_pocket_width_mm=18.0,
        yubikey_pocket_depth_mm=3.0,
        yubikey_wall_clearance_mm=0.3,
        airtag_pocket_diameter_mm=31.9,
        airtag_pocket_depth_mm=7.0,
        airtag_wall_clearance_mm=0.3,
        pocket_edge_margin_mm=2.0,
        pocket_spacing_mm=3.0,
    )


def build_wallet_card(dimensions: WalletCardDimensions):
    import cadquery as cq

    card = (
        cq.Workplane("XY")
        .rect(dimensions.card_length_mm, dimensions.card_width_mm)
        .extrude(dimensions.card_thickness_mm)
        .edges("|Z")
        .fillet(dimensions.corner_radius_mm)
    )

    yubikey_pocket = (
        cq.Workplane("XY")
        .workplane(offset=dimensions.card_thickness_mm - dimensions.yubikey_pocket_depth_mm)
        .center(dimensions.yubikey_pocket_center_x_mm, 0)
        .rect(dimensions.yubikey_pocket_effective_length_mm, dimensions.yubikey_pocket_effective_width_mm)
        .extrude(dimensions.yubikey_pocket_depth_mm)
    )
    card = card.cut(yubikey_pocket)

    airtag_pocket = (
        cq.Workplane("XY")
        .workplane(offset=dimensions.card_thickness_mm - dimensions.airtag_pocket_depth_mm)
        .center(dimensions.airtag_pocket_center_x_mm, 0)
        .circle(dimensions.airtag_pocket_effective_diameter_mm / 2)
        .extrude(dimensions.airtag_pocket_depth_mm)
    )
    card = card.cut(airtag_pocket)

    return card


def export_wallet_card_stl(dimensions: WalletCardDimensions, file_path: str) -> str:
    from cadquery import exporters

    output_path = Path(file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    card = build_wallet_card(dimensions)
    exporters.export(card, str(output_path))

    return str(output_path)
