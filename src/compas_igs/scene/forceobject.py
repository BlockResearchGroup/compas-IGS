from typing import Optional

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import transform_points
from compas.geometry import transform_vectors
from compas.scene.descriptors.color import ColorAttribute
from compas.scene.descriptors.colordict import ColorDictAttribute
from compas_ags.diagrams import ForceDiagram
from compas_rui.scene import RUIMeshObject


class RhinoForceObject(RUIMeshObject):
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

        self._anchor = None
        self._location = None
        self._scale = None

        self.show_faces = False
        self.show_edges = True
        self.show_vertices = True

    @property
    def diagram(self) -> ForceDiagram:
        return self.mesh

    @diagram.setter
    def diagram(self, diagram: ForceDiagram) -> None:
        self.mesh = diagram

    @property
    def anchor(self) -> int:
        if self._anchor is None:
            return 0
        return self._anchor

    @anchor.setter
    def anchor(self, vertex: int) -> None:
        self._anchor = vertex

    @property
    def location(self) -> Point:
        if self._location is None:
            return self.diagram.vertex_point(self.anchor)
        return self._location

    @location.setter
    def location(self, point: Point) -> None:
        self._location = point

    @property
    def scale(self) -> float:
        if self._scale is None:
            return 1.0
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        self._scale = value

    @property
    def transformation(self):
        # move from anchor coordinates to origin
        # apply scale
        # move from origin to location
        origin = Point(0, 0, 0)
        anchorpoint = self.diagram.vertex_point(self.anchor)
        vector = origin - anchorpoint
        T0 = Translation.from_vector(vector)
        S = Scale.from_factors([self.scale, self.scale, 1])
        T1 = Translation.from_vector(self.location)
        return T1 * S * T0

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

    def select_anchor(self):
        self.show_vertices = list(self.diagram.vertices())
        self.redraw_vertices()

        selected = self.select_vertices(message="Select the force diagram anchor.")
        if not selected:
            return

        if len(selected) > 1:
            return rs.MessageBox("You can only select one anchor vertex.", title="Warning")

        return selected[0]

    def select_fixed_vertices(self):
        self.show_vertices = list(self.diagram.vertices())
        self.redraw_vertices()

        selected = self.select_vertices(message="Select ALL fixed vertices (others will be unfixed).")

        if selected:
            self.diagram.vertices_attribute(name="is_fixed", value=False)
            self.diagram.vertices_attribute(name="is_fixed", value=True, keys=selected)

        return selected

    # =============================================================================
    # Move
    # =============================================================================

    def move(self) -> bool:
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor

        vertex_p0 = {v: Rhino.Geometry.Point3d(*self.mesh.vertex_coordinates(v)) for v in self.mesh.vertices()}
        vertex_p1 = {v: Rhino.Geometry.Point3d(*self.mesh.vertex_coordinates(v)) for v in self.mesh.vertices()}

        edges = list(self.mesh.edges())

        def OnDynamicDraw(sender, e):
            current = e.CurrentPoint
            vector = current - start
            for vertex in vertex_p1:
                vertex_p1[vertex] = vertex_p0[vertex] + vector
            for u, v in iter(edges):
                sp = vertex[u]
                ep = vertex[v]
                e.Display.DrawDottedLine(sp, ep, color)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move from?")
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Point to move to?")
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = compas_rhino.conversions.vector_to_compas(end - start)

        for _, attr in self.mesh.vertices(True):
            attr["x"] += vector[0]
            attr["y"] += vector[1]
            attr["z"] += vector[2]

        return True

    def move_vertex(
        self,
        vertex: int,
        constraint: Optional[Rhino.Geometry.GeometryBase] = None,
        allow_off: bool = True,
    ) -> bool:
        def OnDynamicDraw(sender, e):
            for ep in nbrs:
                sp = e.CurrentPoint
                e.Display.DrawDottedLine(sp, ep, color)

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs = [self.mesh.vertex_coordinates(nbr) for nbr in self.mesh.vertex_neighbors(vertex)]
        nbrs = [Rhino.Geometry.Point3d(*xyz) for xyz in nbrs]

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move to?")
        gp.DynamicDraw += OnDynamicDraw
        if constraint:
            gp.Constrain(constraint, allow_off)

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        self.mesh.vertex_attributes(vertex, "xyz", list(gp.Point()))
        return True

    def move_vertices(self, vertices: list[int]) -> bool:
        def OnDynamicDraw(sender, e):
            end = e.CurrentPoint
            vector = end - start
            for a, b in lines:
                a = a + vector
                b = b + vector
                e.Display.DrawDottedLine(a, b, color)
            for a, b in connectors:
                a = a + vector
                e.Display.DrawDottedLine(a, b, color)

        X = self.worldtransformation

        vertex_xyz = dict(zip(self.diagram.vertices(), transform_points(self.diagram.vertices_attributes("xyz"), X)))

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for vertex in vertices:
            a = vertex_xyz[vertex]
            nbrs = self.mesh.vertex_neighbors(vertex)
            for nbr in nbrs:
                b = vertex_xyz[nbr]
                line = [Rhino.Geometry.Point3d(*a), Rhino.Geometry.Point3d(*b)]
                if nbr in vertices:
                    lines.append(line)
                else:
                    connectors.append(line)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move from?")
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = compas_rhino.conversions.vector_to_compas(end - start)
        vector = transform_vectors([vector], X.inverted())[0]

        for vertex in vertices:
            point = Point(*self.mesh.vertex_attributes(vertex, "xyz"))
            self.mesh.vertex_attributes(vertex, "xyz", point + vector)

        return True

    def move_vertices_direction(self, vertices: list[int], direction: str) -> bool:
        def OnDynamicDraw(sender, e):
            draw = e.Display.DrawDottedLine
            end = e.CurrentPoint
            vector = end - start
            for a, b in lines:
                a = a + vector
                b = b + vector
                draw(a, b, color)
            for a, b in connectors:
                a = a + vector
                draw(a, b, color)

        direction = direction.lower()
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for vertex in vertices:
            a = Rhino.Geometry.Point3d(*self.mesh.vertex_coordinates(vertex))
            nbrs = self.mesh.vertex_neighbors(vertex)
            for nbr in nbrs:
                b = Rhino.Geometry.Point3d(*self.mesh.vertex_coordinates(nbr))
                if nbr in vertices:
                    lines.append((a, b))
                else:
                    connectors.append((a, b))

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Point to move from?")
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        if direction == "x":
            geometry = Rhino.Geometry.Line(start, start + Rhino.Geometry.Vector3d(1, 0, 0))
        elif direction == "y":
            geometry = Rhino.Geometry.Line(start, start + Rhino.Geometry.Vector3d(0, 1, 0))
        elif direction == "z":
            geometry = Rhino.Geometry.Line(start, start + Rhino.Geometry.Vector3d(0, 0, 1))
        elif direction == "xy":
            geometry = Rhino.Geometry.Plane(start, Rhino.Geometry.Vector3d(0, 0, 1))
        elif direction == "yz":
            geometry = Rhino.Geometry.Plane(start, Rhino.Geometry.Vector3d(1, 0, 0))
        elif direction == "zx":
            geometry = Rhino.Geometry.Plane(start, Rhino.Geometry.Vector3d(0, 1, 0))

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw

        if direction in ("x", "y", "z"):
            gp.Constrain(geometry)
        else:
            gp.Constrain(geometry, False)

        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = compas_rhino.conversions.vector_to_compas(end - start)

        for vertex in vertices:
            point = self.mesh.vertex_point(vertex)
            self.mesh.vertex_attributes(vertex, "xyz", point + vector)

        return True
