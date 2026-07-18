# Wallet Card for YubiKey 5C + Apple AirTag

This document describes the wallet card insert defined in `src/print_parts_catalog/wallet_card.py`.

## Purpose

The part is a printable card that:

- Matches a standard ID/credit-card footprint (85.60 x 53.98 mm) so it slots into a wallet card
  pocket alongside your other cards.
- Is thin (3.6 mm starter value) rather than a thick block — cavities are cut almost fully through
  it, and items are held by friction/flex against a necked cavity wall, not by resting in a floored
  recess.
- Carries two cavities cut into the card: a keyed slot with a retention "shoe" sized for a
  YubiKey 5C, and an ellipsoid-of-revolution cavity sized for an Apple AirTag.
- Uses rounded corners matching the ISO/IEC 7810 ID-1 corner radius (3.18 mm / 1/8 in).

## Design Rationale

- **Thin card, snap-fit cavities, not a thick block with floored pockets.** Both cavities are cut
  almost fully through the card's thickness. Each one necks in (narrower) at the top and bottom
  faces and bulges out (wider) at mid-thickness, so the item is gripped by the flex of the
  surrounding plastic — a real snap fit — rather than dropped into a recess with a solid floor
  beneath it. This is the design used by the reference model this part is based on.
- **AirTag cavity is an ellipsoid of revolution, not a cylinder.** The cavity's diameter follows a
  smooth curve from `airtag_pocket_face_diameter_mm` at both faces up to
  `airtag_pocket_max_diameter_mm` at mid-thickness (a sine-interpolated loft through 5 circular
  cross-sections). This grips the AirTag's own rounded edge at its widest point and resists it
  popping out of either face.
- **YubiKey cavity is a straight slot with a "shoe" at one end, not a plain rectangle.** One end of
  the slot (the open end) is a straight, untapered wall through the full thickness. The other end
  (the shoe) necks outward by `yubikey_shoe_bulge_mm` at mid-thickness, tapering back to the
  nominal slot size at both faces — a localized retention catch on just that one end, matching what
  was found in the reference model rather than a symmetric taper on both ends.
- **wall_clearance fields default to 0mm.** Unlike a design derived from raw hardware specs, the
  starter dimensions here are *measured cavity sizes* from a proven, already-printed reference file
  — they're already the target cavity size, not a raw item dimension that needs clearance added on
  top. Use `yubikey_wall_clearance_mm` / `airtag_wall_clearance_mm` to fine-tune fit from there.
- **Side-by-side layout.** The YubiKey slot and AirTag cavity sit end-to-end along the card's long
  axis, separated by `pocket_spacing_mm` and bounded by `pocket_edge_margin_mm` on all sides — same
  layout convention as before.
- **Print orientation and material.** Print with the card flat on the bed (thickness along Z), so
  the necking inside each cavity is a shallow internal overhang well within typical FDM tolerance
  and prints without supports. Prefer a print material with some flex (e.g. PETG) over a stiff one
  (e.g. PLA) — retention depends on the cavity walls flexing slightly as the item is pushed past
  the neck, not just tight tolerances.

## Functional Requirement And Validation Notes

The core requirement is that a real YubiKey 5C and a real Apple AirTag both seat securely in their
cavities (retained by the necked profile, not falling out under normal handling), and that neither
cavity's thin necked wall cracks during insertion.

**The starter cavity dimensions are measured from a reference STL, not calipered against your own
hardware — verify before printing a final version.** Since retention here depends on plastic flex
(not just a floored recess), fit is also more sensitive to your printer's dimensional accuracy and
chosen material than the elbow extension's pockets were. Print one copy at the baseline dimensions
first and test-fit both items before adjusting.

## Current baseline dimensions

- Card length: 85.60 mm
- Card width: 53.98 mm
- Card thickness: 3.6 mm
- Corner radius: 3.18 mm
- AirTag cavity: 29.5 mm diameter at the faces → 31.7 mm at mid-thickness
- AirTag wall clearance: 0.0 mm (fine-tune from here if needed)
- YubiKey slot: 42.4 mm long (open end to shoe base) x 17.95 mm wide, corner radius 1.5 mm
- YubiKey shoe bulge: 2.6 mm extra length at mid-thickness on the shoe end only
- YubiKey wall clearance: 0.0 mm (fine-tune from here if needed)
- Pocket edge margin: 2.0 mm
- Pocket spacing (between the two cavities): 3.0 mm

The source defaults are defined by `starter_wallet_card_dimensions()`.

## Launch the notebook

From the repository root, open the interactive notebook app with:

```bash
uv run marimo edit notebooks/wallet_card_starter.py
```

## Run Unit Tests

From the repository root, run:

```bash
uv run python -m unittest discover -s tests -v
```

## Inspect The Model

After the notebook opens, rebuild the cells and visually inspect the generated card in the 3D
preview.

Rotate the model and confirm:

- The overall card footprint and rounded corners look right.
- The AirTag cavity visibly bulges outward at mid-thickness and necks in at both faces.
- The YubiKey slot has one flat, untapered end and one end that bulges outward at mid-thickness.
- Both cavities sit fully within the card, with visible margin from the edges and from each other.

If the preview does not look right, adjust the dimensions in the notebook before exporting.

## Export And Print

Once the preview looks correct, export the STL from the notebook and use that STL for 3D printing.

## Installation notes

1. Print one copy at the baseline dimensions first — don't commit to a batch until fit is confirmed.
2. Test-fit your actual YubiKey 5C and AirTag by pushing them through the necked opening; expect
   some resistance at the neck, then a secure seat once past it.
3. If either item is loose or won't seat, adjust that item's bulge/max-diameter fields (for more
   grip) or its face-diameter/nominal-length fields (for an easier push-in) and reprint just that
   item's cavity — the two cavities are independent.
4. Confirm the overall card still fits your wallet's card slot before relying on it day to day.

## Iteration workflow

1. Print the baseline card.
2. Test-fit both the YubiKey and the AirTag; note which is loose/tight and by roughly how much.
3. Adjust the corresponding cavity's bulge amount and clearance (not just its nominal size) and
   reprint.
4. Repeat until both items seat securely and the card still fits your wallet.
