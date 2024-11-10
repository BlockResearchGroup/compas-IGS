import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas.colors import Color
from compas.scene.descriptors.color import ColorAttribute
from compas.scene.descriptors.colordict import ColorDictAttribute
from compas_ags.diagrams import FormDiagram
from compas_rui.scene import RUIMeshObject


class RhinoFormObject(RUIMeshObject):
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

    @property
    def diagram(self) -> FormDiagram:
        return self.mesh

    @diagram.setter
    def diagram(self, diagram: FormDiagram) -> None:
        self.mesh = diagram

    # =============================================================================
    # Draw
    # =============================================================================

    def draw_vertices(self):
        for vertex in self.diagram.vertices():
            if self.diagram.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.vertexcolor_fixed

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

    # =============================================================================
    # Redraw
    # =============================================================================

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

    def redraw(self):
        rs.EnableRedraw(False)
        self.clear_vertices()
        self.clear_edges()
        self.draw_vertices()
        self.draw_edges()
        rs.EnableRedraw(True)
        rs.Redraw()

    # =============================================================================
    # Select
    # =============================================================================

    def select_fixed_vertices(self):
        self.show_vertices = list(self.diagram.vertices())
        self.redraw_vertices()

        selected = self.select_vertices(message="Select ALL fixed vertices (others will be unfixed).")
        if selected:
            self.diagram.vertices_attribute(name="is_fixed", value=False)
            self.diagram.vertices_attribute(name="is_fixed", value=True, keys=selected)

        return selected

    def select_independent_edges(self):
        self.show_vertices = list(self.diagram.edges_where(_is_edge=True))
        self.redraw_vertices()

        selected = self.select_edges(message="Select ALL independent edges.")
        if selected:
            self.diagram.edges_attribute(name="is_ind", value=False)
            self.diagram.edges_attribute(name="is_ind", value=True, keys=selected)

        return selected
