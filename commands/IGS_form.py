#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import pathlib

import compas_rhino.conversions

import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino.objects
from compas_ags.diagrams import FormDiagram
from compas_ags.diagrams import FormGraph
from compas_igs.session import IGSSession
from compas_rui.forms import FileForm

# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    form = session.find_formdiagram(warn=False)
    if form:
        if not session.confirm("This will remove the existing digrams. Do you want to procced?"):
            return
        session.clear()

    # =============================================================================
    # Create form diagram
    # =============================================================================

    option = rs.GetString(message="FormDiagram From", strings=["RhinoLines", "OBJ"])
    if not option:
        return

    if option == "RhinoLines":
        guids = compas_rhino.objects.select_lines()
        if not guids:
            return

        lines = compas_rhino.conversions.get_line_coordinates(guids)
        graph = FormGraph.from_lines(lines)

        if not graph.is_planar_embedding():
            return rs.MessageBox(
                message="The graph is not planar. Therefore, a form diagram cannot be created.",
                title="Create FormDiagram Error",
            )

        formdiagram = FormDiagram.from_graph(graph)

    elif option == "OBJ":
        filepath = FileForm.open(session.basedir)
        if not filepath:
            return

        filepath = pathlib.Path(filepath)
        if not filepath.suffix == ".obj":
            return rs.MessageBox(
                message="The file is not an OBJ file.",
                title="Error FormDiagram",
            )

        graph = FormGraph.from_obj(filepath)

        if not graph.is_planar_embedding():
            return rs.MessageBox(
                message="The graph is not planar. Therefore, a form diagram cannot be created.",
                title="Create FormDiagram Error",
            )

        formdiagram = FormDiagram.from_graph(graph)

    elif option == "MeshGrid":
        raise NotImplementedError

    else:
        raise NotImplementedError

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    if not formdiagram:
        return

    session.settings.form.show_internal_force_pipes = False
    session.settings.form.show_external_force_labels = False
    session.settings.form.show_independent_edge_labels = False

    session.scene.add(formdiagram)
    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Create FormDiagram")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
