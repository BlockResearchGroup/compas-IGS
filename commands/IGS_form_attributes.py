#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore

from compas_igs.forms import Attribute
from compas_igs.forms import EdgeAttributesForm
from compas_igs.forms import VertexAttributesForm
from compas_igs.session import IGSSession

# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    form = session.find_formdiagram(warn=True)
    if not form:
        return

    # =============================================================================
    # Attributes
    # =============================================================================

    option = rs.GetString("Form Attributes", strings=["VertexAttributes", "EdgeAttributes"])
    if not option:
        return

    if option == "VertexAttributes":
        attributes = [
            Attribute(name="x", text="X", value=float, width=48, editable=False),
            Attribute(name="y", text="Y", value=float, width=48, editable=False),
            Attribute(name="z", text="Z", value=float, width=48, editable=False),
            Attribute(name="is_fixed", text="FIXED", value=bool, width=48, editable=False),
            Attribute(name="cx", text="CX", value=float, width=48, editable=False),
            Attribute(name="cy", text="CY", value=float, width=48, editable=False),
        ]

        vertices = {}
        for vertex in form.diagram.vertices():
            vertices[vertex] = {}
            for attr in attributes:
                vertices[vertex][attr.name] = form.diagram.vertex_attribute(vertex, name=attr.name)

        form = VertexAttributesForm(attributes, vertices)
        if form.show():
            pass

    elif option == "EdgeAttributes":
        attributes = [
            Attribute(name="l", text="L", value=float, width=64, editable=False),
            Attribute(name="q", text="Q", value=float, width=64, editable=False),
            Attribute(name="f", text="F", value=float, width=64, editable=False),
            Attribute(name="is_ind", text="IND", value=bool, width=48, editable=False),
        ]

        edges = {}
        for edge in form.diagram.edges():
            edges[edge] = {}
            for attr in attributes:
                edges[edge][attr.name] = form.diagram.edge_attribute(edge, name=attr.name)

        form = EdgeAttributesForm(attributes, edges)
        if form.show():
            pass

    # =============================================================================
    # Update scene
    # =============================================================================

    # if session.settings.autosave:
    #     session.record(name="Form Attributes")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
