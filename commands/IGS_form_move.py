#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino.conversions
from compas_ags.diagrams import Diagram
from compas_igs.session import IGSSession


def move(diagram: Diagram):
    start = rs.GetPoint("Start point")
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

    vector = compas_rhino.conversions.point_to_compas(end) - compas_rhino.conversions.point_to_compas(start)

    for vertex in diagram.vertices():
        point = diagram.vertex_point(vertex) + vector
        diagram.vertex_attributes(vertex, "xy", point[:2])


# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    form = session.find_formdiagram(warn=True)
    if not form:
        return

    # =============================================================================
    # Command
    # =============================================================================

    move(form.diagram)

    # =============================================================================
    # Update Scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Form Move")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
