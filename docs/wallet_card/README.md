# Wallet Card for YubiKey 5C + Apple AirTag

This document describes the wallet card insert defined in `src/print_parts_catalog/wallet_card.py`.

## Purpose

The part is a printable card that:

- Matches a standard ID/credit-card footprint (85.60 x 53.98 mm) so it slots into a wallet card
  pocket alongside your other cards.
- Carries two blind pockets cut into one face: a rectangular pocket sized for a YubiKey 5C, and a
  circular pocket sized for an Apple AirTag.
- Uses rounded corners matching the ISO/IEC 7810 ID-1 corner radius (3.18 mm / 1/8 in).

## Design Rationale

- **Card footprint, not card thickness.** A real ID card is about 0.76 mm thick — far too thin to
  hold an 8 mm-thick AirTag. This design keeps the length/width of a standard card (so it still
  fits the footprint of a wallet slot) but is deliberately much thicker (~9 mm starter value) to
  fully house both items. It will feel like several stacked cards, not one — check it against your
  own wallet's card slots before committing to a final print.
- **Blind pockets, not through-holes.** Both pockets are cut from the top face down to a floor
  (`floor_thickness_mm`), rather than cutting all the way through the card, so items don't fall
  out the back and the card keeps a solid base.
- **Explicit wall clearance per item.** `yubikey_wall_clearance_mm` and `airtag_wall_clearance_mm`
  are added per side to each pocket's nominal size, independent of edge margins, so fit can be
  tuned per item without touching the other.
- **Side-by-side layout.** The YubiKey pocket and AirTag pocket sit end-to-end along the card's
  long axis, separated by `pocket_spacing_mm` and bounded by `pocket_edge_margin_mm` on all sides.
  At the standard card footprint this layout is tight (see baseline dimensions below) — there is
  little room to grow either pocket without increasing the card length.

## Functional Requirement And Validation Notes

The core requirement is that a real YubiKey 5C and a real Apple AirTag both seat in their pockets
without excessive slop, and that the card doesn't crack at the thin floor beneath either pocket.

**The starter pocket dimensions are approximate — verify before printing a final version.** The
YubiKey 5C pocket size (45.6 x 18.6 mm effective) is based on Yubico's published 5C dimensions
(~45 x 18 x 3 mm); the AirTag pocket size (32.5 mm effective diameter) is based on Apple's
published AirTag spec (31.9 mm diameter x 8 mm thick). Measure your actual hardware with calipers
and adjust `yubikey_pocket_*_mm` / `airtag_pocket_*_mm` and the clearance fields before treating
any print as final — this is the same caution the elbow extension doc gives around O-ring sizing.

## Current baseline dimensions

- Card length: 85.60 mm
- Card width: 53.98 mm
- Card thickness: 9.0 mm
- Corner radius: 3.18 mm
- Floor thickness under pockets: 1.2 mm
- YubiKey pocket (nominal): 45.0 x 18.0 mm, 3.0 mm deep
- YubiKey wall clearance: 0.3 mm per side
- AirTag pocket (nominal): 31.9 mm diameter, 7.0 mm deep
- AirTag wall clearance: 0.3 mm per side
- Pocket edge margin: 2.0 mm
- Pocket spacing (between the two pockets): 3.0 mm

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
- Both pockets sit fully within the card, with visible margin from the edges and from each other.
- Neither pocket cuts through to the bottom face (there should be a visible floor).

If the preview does not look right, adjust the dimensions in the notebook before exporting.

## Export And Print

Once the preview looks correct, export the STL from the notebook and use that STL for 3D printing.

## Installation notes

1. Print one copy at the baseline dimensions first — don't commit to a batch until fit is confirmed.
2. Test-fit your actual YubiKey 5C and AirTag in their pockets.
3. If either item is loose or too tight, adjust that item's pocket size and clearance fields and
   reprint just that item's fit — the two pockets are independent.
4. Confirm the overall card still fits your wallet's card slot before relying on it day to day.

## Iteration workflow

1. Print the baseline card.
2. Test-fit both the YubiKey and the AirTag; note which is loose/tight and by roughly how much.
3. Adjust the corresponding pocket's clearance (not just its nominal size) and reprint.
4. Repeat until both items seat securely and the card still fits your wallet.
