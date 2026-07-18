# print-parts-catalog

Small physical problems can often be solved quickly by combining simple parametric code with 3D printing.

This repository uses Python + CadQuery + marimo so you can iterate dimensions in code, inspect geometry visually, and export printable STL files. It's a catalog of unrelated parts — no shared theme beyond "parametric and 3D-printed."

## Parts

- [Elbow extension](docs/elbow_extension/README.md) — a printable insert for a garbage-disposal elbow
- [Wallet card](docs/wallet_card/README.md) — a wallet-slot-sized card that holds a YubiKey 5C and an Apple AirTag

## Project layout

- `src/print_parts_catalog/`: package code — one module per part, with reusable geometry-builder helpers
- `notebooks/`: marimo apps for interactive modeling and STL export
- `tests/`: unit tests for dimensions, geometry behavior, and export checks

## Quick start

```bash
uv sync
uv run python -m unittest discover -s tests -v
```

CadQuery is a normal package dependency. On this platform, its VTK stack currently supports Python 3.10 through 3.12, and the project metadata constrains `uv` to a compatible version automatically.

## Launch a part's app

Each part has its own notebook at `notebooks/<part>_starter.py`. From the repository root, launch one with:

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
