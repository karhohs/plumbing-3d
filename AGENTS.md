# AGENTS.md

Guidance for AI coding agents working in this repo. See https://agents.md for the format spec.

## Project overview

`plumbing-3d` is a small Python + CadQuery + marimo project for designing parametric plumbing
parts and exporting them as printable STL files. The current featured part is a garbage-disposal
elbow extension. See `README.md` for the project pitch and
`docs/elbow_extension/README.md` for the design rationale, baseline dimensions, and print/install
notes behind that part — read it before changing dimensions or geometry logic.

## Layout

- `src/plumbing_3d/`: package code — dataclasses for part dimensions and CadQuery geometry builders
- `notebooks/`: marimo apps for interactive modeling and STL export
- `tests/`: unittest-based tests for dimension validation, geometry envelope, and STL export
- `docs/`: per-part design docs
- `artifacts/`: exported STL files — generated output, not hand-edited

## Setup and build commands

```bash
uv sync
```

CadQuery's VTK stack currently supports Python 3.10–3.12 only; `pyproject.toml` constrains this
and `uv` resolves a compatible interpreter automatically. Don't loosen `requires-python` without
confirming CadQuery/VTK support the target version.

## Test commands

```bash
uv run python -m unittest discover -s tests -v
```

Run this after any change to `src/plumbing_3d/`. Tests exercise dimension validation (invalid
inputs should raise `ValueError`), the built geometry's bounding box, and that STL export produces
a non-empty file.

## Running the notebook app

```bash
uv run marimo edit notebooks/elbow_extension_starter.py   # interactive editor
uv run marimo run notebooks/elbow_extension_starter.py    # run as an app
```

## Code style

- Represent each part's parameters as a `@dataclass(frozen=True)` with a `__post_init__` that
  validates invariants and raises `ValueError` with a descriptive message per failing check (see
  `ElbowExtensionDimensions` in `src/plumbing_3d/elbow_extension.py`).
- Suffix every length/diameter field and variable with its unit, e.g. `_mm`. Don't introduce
  unitless dimension values.
- Derive dependent values (e.g. inner diameter from outer diameter and wall thickness) as
  `@property` methods on the dataclass rather than storing them redundantly.
- Import `cadquery` inside the functions that use it rather than at module scope.
- Prefer plain `unittest` (as used in `tests/`) over introducing a new test framework.

## Gotchas

- Geometry changes should be checked against `docs/elbow_extension/README.md`'s stated tolerances
  and functional requirements (fit, seal, printability) — this is a physical part, not just code.
- `artifacts/*.stl` are generated outputs; regenerate them via the notebook or
  `export_elbow_extension_stl` rather than editing them directly.
