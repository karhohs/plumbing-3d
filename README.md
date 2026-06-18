# plumbing-3d

Small plumbing projects can be solved quickly by combining simple parametric code with 3D printing.

This repository uses Python + CadQuery + marimo so you can iterate dimensions in code, inspect geometry visually, and export printable STL files.

## Featured project

The current focus is a garbage-disposal elbow extension:

- [docs/elbow_extension/README.md](docs/elbow_extension/README.md)

## Project layout

- `src/plumbing_3d/`: package code for reusable plumbing part helpers and geometry builders
- `notebooks/`: marimo apps for interactive modeling and STL export
- `tests/`: unit tests for dimensions, geometry behavior, and export checks

## Quick start

```bash
uv sync
uv run python -m unittest discover -s tests -v
```

CadQuery is a normal package dependency. On this platform, its VTK stack currently supports Python 3.10 through 3.12, and the project metadata constrains `uv` to a compatible version automatically.

## Launch the app

From the repository root, launch the elbow extension app with:

```bash
uv sync
uv run marimo edit notebooks/elbow_extension_starter.py
```

This opens the interactive marimo editor in your browser.

If you want to run it as an app instead of opening the editor, use:

```bash
uv run marimo run notebooks/elbow_extension_starter.py
```

The app lets you adjust dimensions, inspect the model, and export STL files for printing.
