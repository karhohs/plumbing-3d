import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from plumbing_3d import (
        ElbowExtensionDimensions,
        build_elbow_extension,
        export_elbow_extension_stl,
        starter_elbow_extension_dimensions,
    )

    return (
        ElbowExtensionDimensions,
        build_elbow_extension,
        export_elbow_extension_stl,
        mo,
        starter_elbow_extension_dimensions,
    )


@app.cell
def _(mo):
    mo.md("""
    # Elbow extension creator

    Use this app to generate and visualize the disposal elbow extension.
    The baseline design keeps the O-ring groove disabled.
    """)
    return


@app.cell
def _(mo, starter_elbow_extension_dimensions):
    starter = starter_elbow_extension_dimensions()

    insert_outer_diameter_mm = mo.ui.number(
        start=20.0,
        stop=60.0,
        step=0.5,
        value=starter.insert_outer_diameter_mm,
        label="Insert outer diameter (mm)",
    )
    insert_inner_diameter_mm = mo.ui.number(
        start=10.0,
        stop=59.0,
        step=0.5,
        value=starter.insert_inner_diameter_mm,
        label="Insert inner diameter (mm)",
    )

    body_outer_diameter_mm = mo.ui.number(
        start=20.0,
        stop=80.0,
        step=0.5,
        value=starter.body_outer_diameter_mm,
        label="Body outer diameter (mm)",
    )
    wall_thickness_mm = mo.ui.number(
        start=1.0,
        stop=8.0,
        step=0.1,
        value=starter.wall_thickness_mm,
        label="Wall thickness (mm)",
    )
    insert_depth_mm = mo.ui.number(
        start=5.0,
        stop=60.0,
        step=1.0,
        value=starter.insert_depth_mm,
        label="Insert depth (mm)",
    )
    extension_length_mm = mo.ui.number(
        start=0.0,
        stop=80.0,
        step=1.0,
        value=starter.extension_length_mm,
        label="Extension length (mm)",
    )
    inner_transition_straight_length_mm = mo.ui.number(
        start=0.0,
        stop=30.0,
        step=0.5,
        value=starter.inner_transition_straight_length_mm,
        label="Inner transition straight length (mm)",
    )
    inner_transition_ramp_length_mm = mo.ui.number(
        start=0.0,
        stop=20.0,
        step=0.5,
        value=starter.inner_transition_ramp_length_mm,
        label="Inner transition ramp length (mm)",
    )

    end_bead_outer_diameter_mm = mo.ui.number(
        start=20.0,
        stop=100.0,
        step=0.5,
        value=starter.end_bead_outer_diameter_mm,
        label="End bead outer diameter (mm)",
    )

    end_bead_thickness_mm = mo.ui.number(
        start=0.5,
        stop=8.0,
        step=0.5,
        value=starter.end_bead_thickness_mm,
        label="End bead thickness (mm)",
    )

    enable_o_ring = mo.ui.checkbox(
        value=False,
        label="Enable O-ring groove",
    )
    o_ring_groove_width_mm = mo.ui.number(
        start=0.5,
        stop=8.0,
        step=0.1,
        value=starter.o_ring_groove_width_mm,
        label="O-ring groove width (mm)",
    )
    o_ring_groove_depth_mm = mo.ui.number(
        start=0.1,
        stop=4.0,
        step=0.1,
        value=starter.o_ring_groove_depth_mm,
        label="O-ring groove depth (mm)",
    )
    o_ring_groove_backset_from_flange_mm = mo.ui.number(
        start=0.0,
        stop=20.0,
        step=0.1,
        value=starter.o_ring_groove_backset_from_flange_mm,
        label="O-ring groove backset from insert end (mm)",
    )
    stl_output_path = mo.ui.text(
        value="artifacts/elbow_extension.stl",
        label="STL output path",
    )
    export_stl = mo.ui.checkbox(
        value=True,
        label="Export STL",
    )

    mo.vstack(
        [
            insert_outer_diameter_mm,
            insert_inner_diameter_mm,
            body_outer_diameter_mm,
            wall_thickness_mm,
            insert_depth_mm,
            extension_length_mm,
            inner_transition_straight_length_mm,
            inner_transition_ramp_length_mm,
            end_bead_outer_diameter_mm,
            end_bead_thickness_mm,
            enable_o_ring,
            o_ring_groove_width_mm,
            o_ring_groove_depth_mm,
            o_ring_groove_backset_from_flange_mm,
            stl_output_path,
            export_stl,
        ]
    )
    return (
        body_outer_diameter_mm,
        enable_o_ring,
        end_bead_outer_diameter_mm,
        end_bead_thickness_mm,
        export_stl,
        extension_length_mm,
        inner_transition_ramp_length_mm,
        inner_transition_straight_length_mm,
        insert_depth_mm,
        insert_inner_diameter_mm,
        insert_outer_diameter_mm,
        o_ring_groove_backset_from_flange_mm,
        o_ring_groove_depth_mm,
        o_ring_groove_width_mm,
        stl_output_path,
        wall_thickness_mm,
    )


@app.cell
def _(
    ElbowExtensionDimensions,
    body_outer_diameter_mm,
    enable_o_ring,
    end_bead_outer_diameter_mm,
    end_bead_thickness_mm,
    extension_length_mm,
    inner_transition_ramp_length_mm,
    inner_transition_straight_length_mm,
    insert_depth_mm,
    insert_inner_diameter_mm,
    insert_outer_diameter_mm,
    mo,
    o_ring_groove_backset_from_flange_mm,
    o_ring_groove_depth_mm,
    o_ring_groove_width_mm,
    wall_thickness_mm,
):
    try:
        if enable_o_ring.value:
            o_ring_groove_width = o_ring_groove_width_mm.value
            o_ring_groove_depth = o_ring_groove_depth_mm.value
            o_ring_groove_backset = o_ring_groove_backset_from_flange_mm.value
        else:
            o_ring_groove_width = 0.0
            o_ring_groove_depth = 0.0
            o_ring_groove_backset = 0.0

        dimensions = ElbowExtensionDimensions(
            insert_outer_diameter_mm=insert_outer_diameter_mm.value,
            insert_inner_diameter_mm=insert_inner_diameter_mm.value,
            body_outer_diameter_mm=body_outer_diameter_mm.value,
            wall_thickness_mm=wall_thickness_mm.value,
            insert_depth_mm=insert_depth_mm.value,
            extension_length_mm=extension_length_mm.value,
            inner_transition_straight_length_mm=inner_transition_straight_length_mm.value,
            inner_transition_ramp_length_mm=inner_transition_ramp_length_mm.value,
            end_bead_outer_diameter_mm=end_bead_outer_diameter_mm.value,
            end_bead_thickness_mm=end_bead_thickness_mm.value,
            o_ring_groove_width_mm=o_ring_groove_width,
            o_ring_groove_depth_mm=o_ring_groove_depth,
            o_ring_groove_backset_from_flange_mm=o_ring_groove_backset,
            o_ring_groove_enabled=enable_o_ring.value,
        )
    except ValueError as exc:
        dimensions = None
        status = mo.md(f"**Invalid dimensions:** {exc}")
    else:
        if dimensions.has_o_ring_groove:
            groove_lines = [
                f"- O-ring groove width: {dimensions.o_ring_groove_width_mm:.1f} mm",
                f"- O-ring groove depth: {dimensions.o_ring_groove_depth_mm:.1f} mm",
                f"- O-ring groove backset: {dimensions.o_ring_groove_backset_from_flange_mm:.1f} mm",
            ]
        else:
            groove_lines = ["- O-ring groove: disabled"]

        status = mo.md(
            "\n".join(
                [
                    "## Current dimensions",
                    f"- Insert OD: {dimensions.insert_outer_diameter_mm:.1f} mm",
                    f"- Insert ID: {dimensions.insert_inner_diameter_mm:.1f} mm",
                    f"- Body OD: {dimensions.body_outer_diameter_mm:.1f} mm",
                    f"- Body ID: {dimensions.inner_diameter_mm:.1f} mm",
                    f"- Insert depth: {dimensions.insert_depth_mm:.1f} mm",
                    f"- Extension length: {dimensions.extension_length_mm:.1f} mm",
                    f"- Inner transition straight: {dimensions.inner_transition_straight_length_mm:.1f} mm",
                    f"- Inner transition ramp: {dimensions.inner_transition_ramp_length_mm:.1f} mm",
                    f"- End bead OD: {dimensions.end_bead_outer_diameter_mm:.1f} mm",
                    f"- O-ring groove enabled: {dimensions.has_o_ring_groove}",
                    *groove_lines,
                ]
            )
        )

    status
    return (dimensions,)


@app.cell
def _(build_elbow_extension, dimensions, mo):
    if dimensions is None:
        mo.stop(True)

    import plotly.graph_objects as go

    extension = build_elbow_extension(dimensions)
    shape = extension.val()
    # Use finer tessellation so small groove changes are visible in the preview.
    vertices, triangles = shape.tessellate(0.06)

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
                color="#4E7E5D",
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
        mo.md(
            "O-ring groove is "
            + ("**enabled**" if dimensions.has_o_ring_groove else "**disabled**")
            + "."
        ),
        mo.ui.plotly(fig),
    ])
    return


@app.cell
def _(dimensions, export_elbow_extension_stl, export_stl, mo, stl_output_path):
    from pathlib import Path

    if dimensions is None:
        mo.stop(True)

    def render_export_status():
        if not export_stl.value:
            return mo.md("STL export is disabled. Enable **Export STL** to write a file.")

        output_path = stl_output_path.value.strip() or "artifacts/elbow_extension.stl"

        try:
            written_path = export_elbow_extension_stl(dimensions, output_path)
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
