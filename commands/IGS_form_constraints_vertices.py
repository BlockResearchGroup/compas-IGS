#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino.conversions
from compas.geometry import Line
from compas_igs.session import IGSSession


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
        form.diagram.vertex_attribute(vertex, "line_constraint", line)

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
