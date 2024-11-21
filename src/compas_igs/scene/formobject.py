import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401
import scriptcontext as sc  # type: ignore  # noqa: F401

import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas.geometry import Cylinder
from compas.scene.descriptors.color import ColorAttribute
from compas.scene.descriptors.colordict import ColorDictAttribute
from compas_ags.diagrams import FormDiagram
from compas_igs.forms import EdgeForcesForm
from compas_igs.session import IGSSession
from compas_rui.scene import RUIMeshObject


class RhinoFormObject(RUIMeshObject):
    session = IGSSession()

    vertexcolor = ColorDictAttribute(default=Color.black())
    vertexcolor_fixed = ColorAttribute(Color.red())
    vertexcolor_lineconstraint = ColorAttribute(Color.white())

    edgecolor = ColorDictAttribute(default=Color.black())
    edgecolor_independent = ColorAttribute(Color.cyan())
    edgecolor_external = ColorAttribute(Color.green())
    edgecolor_reaction = ColorAttribute(Color.green())
    edgecolor_load = ColorAttribute(Color.green())
    edgecolor_targetforce = ColorAttribute(Color.white())
    edgecolor_targetvector = ColorAttribute(Color.white())

    facecolor = ColorDictAttribute(default=Color.grey().lightened(50))

    vertexlabelcolor = ColorAttribute(Color.white())
    edgelabelcolor = ColorAttribute(Color.black())

    compressioncolor = ColorAttribute(Color.blue())
    tensioncolor = ColorAttribute(Color.red())

    def __init__(
        self,
        disjoint=True,
        **kwargs,
    ):
        super().__init__(disjoint=disjoint, **kwargs)

        self.show_faces = False
        self.show_edges = True
        self.show_vertices = True

        self.show_external_forcelabels = False

        self.show_internal_forcepipes = False
        self.scale_internal_forcepipes = 1.0
        self.tol_internal_forcepipes = 1e-3
        self.internal_forcepipes_group = None
        self._guids_internal_forcepipes = []

        self.show_angles = False
        self._guids_angles = []

    @property
    def diagram(self) -> FormDiagram:
        return self.mesh

    @diagram.setter
    def diagram(self, diagram: FormDiagram) -> None:
        self.mesh = diagram

    # =============================================================================
    # Draw
    # =============================================================================

    def draw(self):
        super().draw()

        if self.show_angles:
            self.draw_angles()

        if self.show_internal_forcepipes:
            self.draw_internal_forcepipes()

        return self.guids

    def draw_vertices(self):
        for vertex in self.diagram.vertices():
            if self.diagram.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.vertexcolor_fixed
            elif self.diagram.vertex_attribute(vertex, "line_constraint"):
                self.vertexcolor[vertex] = self.vertexcolor_lineconstraint

        return super().draw_vertices()

    def draw_edges(self):
        for edge in self.diagram.edges():
            if self.diagram.edge_attribute(edge, "is_ind"):
                self.edgecolor[edge] = self.edgecolor_independent
            elif self.diagram.edge_attribute(edge, "is_external"):
                self.edgecolor[edge] = self.edgecolor_external
            elif self.diagram.edge_attribute(edge, "is_reaction"):
                self.edgecolor[edge] = self.edgecolor_reaction
            elif self.diagram.edge_attribute(edge, "is_load"):
                self.edgecolor[edge] = self.edgecolor_load

        return super().draw_edges()

    def draw_angles(self):
        guids = []
        self._guids_angles = guids
        self._guids += guids
        return guids

    def draw_internal_forcepipes(self):
        guids = []

        scale = self.scale_internal_forcepipes
        tol = self.tol_internal_forcepipes

        color_compression = Color.blue()
        color_tension = Color.red()

        for edge in self.diagram.edges_where(is_external=False):
            force = self.diagram.edge_force(edge)

            if force != 0:
                color = color_compression if force < 0 else color_tension
                line = self.diagram.edge_line(edge)
                radius = abs(force) * scale

                if radius > tol:
                    pipe = Cylinder.from_line_and_radius(line, radius)
                    name = "{}.edge.{}.force".format(self.diagram.name, edge)
                    attr = self.compile_attributes(name=name, color=color)
                    guid = sc.doc.Objects.AddBrep(compas_rhino.conversions.cylinder_to_rhino_brep(pipe), attr)
                    guids.append(guid)

        if guids:
            if self.internal_forcepipes_group:
                self.add_to_group(self.internal_forcepipes_group, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids_internal_forcepipes = guids
        self._guids += guids
        return guids

    def draw_independent_labels(self):
        pass

    def draw_external_labels(self):
        pass

    # =============================================================================
    # Clear
    # =============================================================================

    def clear(self):
        super().clear()
        self.clear_angles()
        self.clear_internal_forcepipes()

    def clear_angles(self):
        compas_rhino.objects.delete_objects(self._guids_angles, purge=True)
        self._guids_angles = []

    def clear_internal_forcepipes(self):
        compas_rhino.objects.delete_objects(self._guids_internal_forcepipes, purge=True)
        self._guids_internal_forcepipes = []

    # =============================================================================
    # Redraw
    # =============================================================================

    def redraw(self):
        rs.EnableRedraw(False)
        self.clear()
        self.draw()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_vertices(self):
        rs.EnableRedraw(False)
        self.clear_vertices()
        self.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_edges(self):
        rs.EnableRedraw(False)
        self.clear_edges()
        self.draw_edges()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_internal_forcepipes(self):
        rs.EnableRedraw(False)
        self.clear_internal_forcepipes()
        self.draw_internal_forcepipes()
        rs.EnableRedraw(True)
        rs.Redraw()

    # =============================================================================
    # Select
    # =============================================================================

    def select_fixed_vertices(self):
        selected = self.select_vertices_manual(message="Select ALL fixed vertices (others will be unfixed).")
        if selected:
            self.diagram.vertices_attribute(name="is_fixed", value=False)
            self.diagram.vertices_attribute(name="is_fixed", value=True, keys=selected)

        return selected

    def select_independent_edges(self):
        selected = self.select_edges_manual(message="Select ALL independent edges.")
        if selected:
            self.diagram.edges_attribute(name="is_ind", value=False)
            self.diagram.edges_attribute(name="is_ind", value=True, keys=selected)

        return selected

    # =============================================================================
    # Other
    # =============================================================================

    def assign_forces(self):
        edges = list(self.diagram.edges_where(is_ind=True))
        if not edges:
            return rs.MessageBox(message="Please identify the independent edges first.")

        self.draw_edgelabels(text={edge: index for index, edge in enumerate(edges)}, color=self.edgecolor)
        rs.Redraw()

        rows = [[index, edge, self.diagram.edge_attribute(edge, name="f")] for index, edge in enumerate(edges)]

        form = EdgeForcesForm(rows, title="Assign Forces")
        if form.show():
            for row in form.rows:
                index, edge, force = row
                length = self.diagram.edge_length(edge)
                fd = force / length
                self.diagram.edge_attribute(edge, name="f", value=force)
                self.diagram.edge_attribute(edge, name="q", value=fd)
