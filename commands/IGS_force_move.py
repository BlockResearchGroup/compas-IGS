#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino.conversions
import compas_rhino.objects
from compas_igs.scene import RhinoForceObject
from compas_igs.session import IGSSession


def move(force: RhinoForceObject):
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

    force.location = force.location + vector


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
    # Command
    # =============================================================================

    move(force)

    # =============================================================================
    # Update Scene
    # =============================================================================

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Force Move")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
