import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from print_parts_catalog import (
        WalletCardDimensions,
        build_wallet_card,
        export_wallet_card_stl,
        starter_wallet_card_dimensions,
    )

    return (
        WalletCardDimensions,
        build_wallet_card,
        export_wallet_card_stl,
        mo,
        starter_wallet_card_dimensions,
    )


@app.cell
def _(mo):
    mo.md("""
    # Wallet card creator

    Use this app to generate and visualize a wallet-slot-sized card that holds a
    YubiKey 5C and an Apple AirTag. Starter pocket dimensions are based on published
    specs — verify against your actual hardware with calipers before printing a final version.
    """)
    return


@app.cell
def _(mo, starter_wallet_card_dimensions):
    starter = starter_wallet_card_dimensions()

    card_length_mm = mo.ui.number(
        start=60.0,
        stop=100.0,
        step=0.1,
        value=starter.card_length_mm,
        label="Card length (mm)",
    )
    card_width_mm = mo.ui.number(
        start=40.0,
        stop=70.0,
        step=0.1,
        value=starter.card_width_mm,
        label="Card width (mm)",
    )
    card_thickness_mm = mo.ui.number(
        start=3.0,
        stop=15.0,
        step=0.1,
        value=starter.card_thickness_mm,
        label="Card thickness (mm)",
    )
    corner_radius_mm = mo.ui.number(
        start=0.0,
        stop=10.0,
        step=0.1,
        value=starter.corner_radius_mm,
        label="Corner radius (mm)",
    )
    floor_thickness_mm = mo.ui.number(
        start=0.5,
        stop=4.0,
        step=0.1,
        value=starter.floor_thickness_mm,
        label="Floor thickness under pockets (mm)",
    )

    yubikey_pocket_length_mm = mo.ui.number(
        start=20.0,
        stop=60.0,
        step=0.5,
        value=starter.yubikey_pocket_length_mm,
        label="YubiKey pocket length (mm)",
    )
    yubikey_pocket_width_mm = mo.ui.number(
        start=10.0,
        stop=30.0,
        step=0.5,
        value=starter.yubikey_pocket_width_mm,
        label="YubiKey pocket width (mm)",
    )
    yubikey_pocket_depth_mm = mo.ui.number(
        start=1.0,
        stop=8.0,
        step=0.1,
        value=starter.yubikey_pocket_depth_mm,
        label="YubiKey pocket depth (mm)",
    )
    yubikey_wall_clearance_mm = mo.ui.number(
        start=0.0,
        stop=2.0,
        step=0.05,
        value=starter.yubikey_wall_clearance_mm,
        label="YubiKey wall clearance (mm)",
    )

    airtag_pocket_diameter_mm = mo.ui.number(
        start=20.0,
        stop=45.0,
        step=0.1,
        value=starter.airtag_pocket_diameter_mm,
        label="AirTag pocket diameter (mm)",
    )
    airtag_pocket_depth_mm = mo.ui.number(
        start=1.0,
        stop=10.0,
        step=0.1,
        value=starter.airtag_pocket_depth_mm,
        label="AirTag pocket depth (mm)",
    )
    airtag_wall_clearance_mm = mo.ui.number(
        start=0.0,
        stop=2.0,
        step=0.05,
        value=starter.airtag_wall_clearance_mm,
        label="AirTag wall clearance (mm)",
    )

    pocket_edge_margin_mm = mo.ui.number(
        start=0.0,
        stop=10.0,
        step=0.1,
        value=starter.pocket_edge_margin_mm,
        label="Pocket edge margin (mm)",
    )
    pocket_spacing_mm = mo.ui.number(
        start=0.0,
        stop=10.0,
        step=0.1,
        value=starter.pocket_spacing_mm,
        label="Pocket spacing (mm)",
    )

    stl_output_path = mo.ui.text(
        value="artifacts/wallet_card.stl",
        label="STL output path",
    )
    export_stl = mo.ui.checkbox(
        value=True,
        label="Export STL",
    )

    mo.vstack(
        [
            card_length_mm,
            card_width_mm,
            card_thickness_mm,
            corner_radius_mm,
            floor_thickness_mm,
            yubikey_pocket_length_mm,
            yubikey_pocket_width_mm,
            yubikey_pocket_depth_mm,
            yubikey_wall_clearance_mm,
            airtag_pocket_diameter_mm,
            airtag_pocket_depth_mm,
            airtag_wall_clearance_mm,
            pocket_edge_margin_mm,
            pocket_spacing_mm,
            stl_output_path,
            export_stl,
        ]
    )
    return (
        airtag_pocket_depth_mm,
        airtag_pocket_diameter_mm,
        airtag_wall_clearance_mm,
        card_length_mm,
        card_thickness_mm,
        card_width_mm,
        corner_radius_mm,
        export_stl,
        floor_thickness_mm,
        pocket_edge_margin_mm,
        pocket_spacing_mm,
        stl_output_path,
        yubikey_pocket_depth_mm,
        yubikey_pocket_length_mm,
        yubikey_pocket_width_mm,
        yubikey_wall_clearance_mm,
    )


@app.cell
def _(
    WalletCardDimensions,
    airtag_pocket_depth_mm,
    airtag_pocket_diameter_mm,
    airtag_wall_clearance_mm,
    card_length_mm,
    card_thickness_mm,
    card_width_mm,
    corner_radius_mm,
    floor_thickness_mm,
    mo,
    pocket_edge_margin_mm,
    pocket_spacing_mm,
    yubikey_pocket_depth_mm,
    yubikey_pocket_length_mm,
    yubikey_pocket_width_mm,
    yubikey_wall_clearance_mm,
):
    try:
        dimensions = WalletCardDimensions(
            card_length_mm=card_length_mm.value,
            card_width_mm=card_width_mm.value,
            card_thickness_mm=card_thickness_mm.value,
            corner_radius_mm=corner_radius_mm.value,
            floor_thickness_mm=floor_thickness_mm.value,
            yubikey_pocket_length_mm=yubikey_pocket_length_mm.value,
            yubikey_pocket_width_mm=yubikey_pocket_width_mm.value,
            yubikey_pocket_depth_mm=yubikey_pocket_depth_mm.value,
            yubikey_wall_clearance_mm=yubikey_wall_clearance_mm.value,
            airtag_pocket_diameter_mm=airtag_pocket_diameter_mm.value,
            airtag_pocket_depth_mm=airtag_pocket_depth_mm.value,
            airtag_wall_clearance_mm=airtag_wall_clearance_mm.value,
            pocket_edge_margin_mm=pocket_edge_margin_mm.value,
            pocket_spacing_mm=pocket_spacing_mm.value,
        )
    except ValueError as exc:
        dimensions = None
        status = mo.md(f"**Invalid dimensions:** {exc}")
    else:
        status = mo.md(
            "\n".join(
                [
                    "## Current dimensions",
                    f"- Card: {dimensions.card_length_mm:.2f} x {dimensions.card_width_mm:.2f} x {dimensions.card_thickness_mm:.1f} mm",
                    f"- YubiKey pocket: {dimensions.yubikey_pocket_effective_length_mm:.1f} x {dimensions.yubikey_pocket_effective_width_mm:.1f} x {dimensions.yubikey_pocket_depth_mm:.1f} mm",
                    f"- AirTag pocket: {dimensions.airtag_pocket_effective_diameter_mm:.1f} mm diameter x {dimensions.airtag_pocket_depth_mm:.1f} mm deep",
                ]
            )
        )

    status
    return (dimensions,)


@app.cell
def _(build_wallet_card, dimensions, mo):
    if dimensions is None:
        mo.stop(True)

    import plotly.graph_objects as go

    card = build_wallet_card(dimensions)
    shape = card.val()
    vertices, triangles = shape.tessellate(0.1)

    x = [vertex.x for vertex in vertices]
    y = [vertex.y for vertex in vertices]
    z = [vertex.z for vertex in vertices]

    i = [triangle[0] for triangle in triangles]
    j = [triangle[1] for triangle in triangles]
    k = [triangle[2] for triangle in triangles]

    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=x,
                y=y,
                z=z,
                i=i,
                j=j,
                k=k,
                color="#3F6FB4",
                opacity=1.0,
                flatshading=False,
                lighting={"ambient": 0.6, "diffuse": 0.7, "specular": 0.2, "roughness": 0.7},
                lightposition={"x": 120, "y": 160, "z": 220},
            )
        ]
    )
    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        scene={
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "zaxis": {"visible": False},
            "aspectmode": "data",
            "camera": {"eye": {"x": 1.4, "y": 1.2, "z": 0.9}},
        },
        paper_bgcolor="white",
    )

    mo.vstack([
        mo.md("## 3D Preview (drag to rotate)"),
        mo.ui.plotly(fig),
    ])
    return


@app.cell
def _(dimensions, export_stl, export_wallet_card_stl, mo, stl_output_path):
    from pathlib import Path

    if dimensions is None:
        mo.stop(True)

    def render_export_status():
        if not export_stl.value:
            return mo.md("STL export is disabled. Enable **Export STL** to write a file.")

        output_path = stl_output_path.value.strip() or "artifacts/wallet_card.stl"

        try:
            written_path = export_wallet_card_stl(dimensions, output_path)
        except Exception as exc:
            return mo.md(f"**STL export failed:** {exc}")

        resolved = Path(written_path).resolve()
        size_bytes = resolved.stat().st_size if resolved.exists() else 0
        return mo.md(
            "\n".join(
                [
                    "**STL exported successfully**",
                    f"- Path: `{resolved}`",
                    f"- Size: {size_bytes} bytes",
                ]
            )
        )

    render_export_status()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
