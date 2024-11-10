import pathlib

import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino.objects
from compas_ags.diagrams import FormDiagram
from compas_ags.diagrams import FormGraph
from compas_igs.scene import RhinoFormObject
from compas_rui.forms import FileForm
from compas_rui.forms import NamedValuesForm


def create_from_lines():
    guids = compas_rhino.objects.select_lines()
    if not guids:
        return

    lines = compas_rhino.objects.get_line_coordinates(guids)
    graph = FormGraph.from_lines(lines)

    if not graph.is_planar_embedding():
        return rs.MessageBox(
            message="The graph is not planar. Therefore, a form diagram cannot be created.",
            title="Create FormDiagram Error",
        )

    formdiagram = FormDiagram.from_graph(graph)
    return formdiagram


def create_from_meshgrid():
    raise NotImplementedError


def create_from_obj(basedir):
    filepath = FileForm.open(basedir)
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
    return formdiagram


def assign_forces(formobject: RhinoFormObject):
    edges = list(formobject.diagram.edges_where(is_ind=True))
    if not edges:
        return rs.MessageBox(message="Please identify the independent edges first.")

    names = [str(edge) for edge in edges]
    values = [formobject.diagram.edge_attribute(edge, name="f") for edge in edges]
    form = NamedValuesForm(names, values, title="Assign Forces")
    if form.show():
        for edge, (name, value) in zip(edges, form.attributes.items()):
            formobject.diagram.edge_attribute(edge, name="f", value=value)
