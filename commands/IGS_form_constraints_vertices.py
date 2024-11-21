#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino.conversions
from compas.geometry import Line
from compas_igs.session import IGSSession
from compas_igs.utilities import check_equilibrium


def get_constraint():
    start = rs.GetPoint("Start of line constraint")
    if not start:
        return

    def OnDynamicDraw(sender, e):
        end = e.CurrentPoint
        e.Display.DrawDottedLine(start, end, color)

    color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor

    gp = Rhino.Input.Custom.GetPoint()
    gp.DynamicDraw += OnDynamicDraw
    gp.SetCommandPrompt("End of line constraint")
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success:
        return

    end = gp.Point()

    return Line(compas_rhino.conversions.point_to_compas(start), compas_rhino.conversions.point_to_compas(end))


# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    return session.warn("Constraints are not available yet.")

    form = session.find_formdiagram(warn=True)
    if not form:
        return

    force = session.find_forcediagram(warn=True)
    if not force:
        return

    # =============================================================================
    # Apply constraints
    # =============================================================================

    selected = form.select_vertices()
    if not selected:
        return

    line = get_constraint()
    if not line:
        return

    for vertex in selected:
        point = form.diagram.vertex_point(vertex)
        point = line.closest_point(point)
        form.diagram.vertex_attribute(vertex, "line_constraint", line)
        form.diagram.vertex_attributes(vertex, "xyz", point)

    # =============================================================================
    # Check equilibrium
    # =============================================================================

    max_angle = session.settings.solver.max_angle
    min_force = session.settings.solver.min_force
    max_ldiff = session.settings.solver.max_ldiff

    result = check_equilibrium(
        form.diagram,
        force.diagram,
        tol_angle=max_angle,
        tol_force=min_force,
        tol_ldiff=max_ldiff,
    )

    if result:
        session.settings.form.show_internal_force_pipes = True
        session.settings.form.show_external_force_labels = True
    else:
        print("The diagrams ARE NOT in equilibrium.")

        session.settings.form.show_internal_force_pipes = False
        session.settings.form.show_external_force_labels = False
        session.settings.form.show_independent_edge_labels = True

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Update Form Vertex Constraints")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
