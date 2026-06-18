# Elbow Extension for Garbage Disposal

This document describes the elbow extension insert part defined in `src/plumbing_3d/elbow_extension.py`.

## Purpose

The part is a printable insert that:

- Fits inside the disposal elbow.
- Uses a fixed insertion depth.
- Bridges a gap using a configurable exposed extension length.
- Carries insert ID into the extension for a configurable straight distance, then uses an internal taper up to extension ID.
- Uses elbow-matching dimensions on the exposed extension section.
- Includes a required end bead at the exposed end.
- Optionally includes a rounded O-ring groove near the insert section end for improved sealing and printability.

## Design Rationale

The geometry is intentionally conservative in the areas that matter most for fit and durability:

- The insert section is sized to maintain a controlled interference fit inside the elbow.
- The internal transition carries the insert bore forward before tapering, which helps the joint behave more like a supported socket than a sharp step.
- The end bead provides a clear stop and helps keep the part seated during use.
- ASA is a good default material for this part because it offers better toughness and heat resistance than many commodity plastics, which is useful in plumbing and garbage disposal service.

The O-ring groove is optional on purpose. A silicone grease seal is often good enough for this kind of insert, and a fully optimized O-ring gland is difficult to standardize because actual O-ring cross-sections vary by hardware store source, brand, and nominal size. Leaving the groove optional lets you print a simpler part when grease alone is sufficient, while still keeping the sealing feature available for cases that need it.

## Functional Requirement And Validation Notes

An extension with an O-ring is not required to satisfy the core functional requirement of this part: fill a plumbing gap and avoid leaks. In practice, this can be achieved with the non-O-ring extension when a small amount of plumber's silicone grease is applied.

The O-ring path was pursued as an intentional overshoot of the baseline design requirement to target a tighter seal and potentially better long-term performance.

The current groove defaults were validated with an O-ring sized:

- OD: 1 3/16 in
- ID: 1 1/16 in
- Cord diameter: 1/16 in

Silicone grease was also applied with this O-ring setup.

Both extension variants (with and without O-ring) were tested under:

- Hot and cold running water
- A flood test: filling a stock pot with water and dumping it down the sink

## Current baseline dimensions

- Insert outer diameter: 33.0 mm
- Insert inner diameter: 27.0 mm
- Body outer diameter: 38.0 mm
- Body inner diameter: 33.0 mm
- End bead outer diameter: 40.0 mm
- End bead thickness: 1.0 mm
- O-ring groove: disabled by default
- O-ring groove width: 3.8 mm
- O-ring groove depth: 1.5 mm
- O-ring groove backset from insert end: 2.0 mm
- Insert depth: 13.0 mm
- Extension length: 25.0 mm default (print multiple variants)
- Inner transition straight length: 5.0 mm
- Inner transition ramp length: 5.0 mm

The source defaults are defined by `starter_elbow_extension_dimensions()`.

## Launch the notebook

From the repository root, open the interactive notebook app with:

```bash
uv run marimo edit notebooks/elbow_extension_starter.py
```

## Run Unit Tests

From the repository root, run:

```bash
uv run python -m unittest discover -s tests -v
```

## Inspect The Model

After the notebook opens, rebuild the cells and visually inspect the generated part in the 3D preview.

Rotate the model and confirm:

- The insert fits the intended elbow entry geometry.
- The inner carry-through and taper look smooth.
- The end bead appears consistent with the stop geometry.
- The O-ring groove is only enabled when you actually want to use it.

If the preview does not look right, adjust the dimensions in the notebook before exporting.

## Export And Print

Once the preview looks correct, export the STL from the notebook and use that STL for 3D printing.

For this part, ASA is the recommended starting material because it is tougher and better suited to plumbing-adjacent use than more brittle or temperature-sensitive materials.

## Installation notes

1. Print the extension with the desired `extension_length_mm`.
2. Insert into the elbow to the desired depth.
3. Expect a somewhat tight fit by design.
4. Use plumber's grease as the first assembly aid.
5. If grease is not sufficient for sealing, apply RTV as needed.

## Iteration workflow

1. Print several extension-length variants.
2. Test fit and seal in the installed elbow.
3. Select the shortest variant that reliably bridges the gap and seals.
