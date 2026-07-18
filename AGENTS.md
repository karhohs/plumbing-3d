# AGENTS.md

Guidance for AI coding agents working in this repo. See https://agents.md for the format spec.

## Project overview

`print-parts-catalog` is a Python + CadQuery + marimo project for designing parametric,
3D-printable parts and exporting them as STL files. It's a growing catalog of unrelated parts
(e.g. plumbing fittings, wallet accessories) — there's no shared theme beyond "parametric and
3D-printed." Each part gets its own module, doc, test file, and notebook (see Layout below). See
`README.md` for the project pitch and part list, and each part's `docs/<part>/README.md` for that
part's design rationale, baseline dimensions, and print/install notes — read the relevant one
before changing dimensions or geometry logic for that part.

## Layout

- `src/print_parts_catalog/`: package code — one module per part, each with a dataclass for
  dimensions and CadQuery geometry builders (e.g. `elbow_extension.py`)
- `notebooks/`: one marimo app per part for interactive modeling and STL export
  (`<part>_starter.py`)
- `tests/`: unittest-based tests per part for dimension validation, geometry envelope, and STL
  export (`test_<part>.py`)
- `docs/`: per-part design docs (`<part>/README.md`)
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

Run this after any change to `src/print_parts_catalog/`. Tests exercise dimension validation
(invalid inputs should raise `ValueError`), the built geometry's bounding box, and that STL export
produces a non-empty file.

## Running a notebook app

Each part has its own notebook at `notebooks/<part>_starter.py`, e.g.:

```bash
uv run marimo edit notebooks/elbow_extension_starter.py   # interactive editor
uv run marimo run notebooks/elbow_extension_starter.py    # run as an app
```

## Code style

- Represent each part's parameters as a `@dataclass(frozen=True)` with a `__post_init__` that
  validates invariants and raises `ValueError` with a descriptive message per failing check (see
  `ElbowExtensionDimensions` in `src/print_parts_catalog/elbow_extension.py`).
- Suffix every length/diameter field and variable with its unit, e.g. `_mm`. Don't introduce
  unitless dimension values.
- Derive dependent values (e.g. inner diameter from outer diameter and wall thickness) as
  `@property` methods on the dataclass rather than storing them redundantly.
- Import `cadquery` inside the functions that use it rather than at module scope.
- Prefer plain `unittest` (as used in `tests/`) over introducing a new test framework.

## Gotchas

- Geometry changes should be checked against the part's own `docs/<part>/README.md` for stated
  tolerances and functional requirements (fit, seal, printability) — these are physical parts,
  not just code. Starter dimensions for parts that hold third-party hardware (e.g. a specific
  YubiKey model) are based on public specs and should be flagged as needing physical verification
  until confirmed.
- `artifacts/*.stl` are generated outputs; regenerate them via the relevant notebook or
  `export_*_stl` function rather than editing them directly.
