#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

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
    # Command
    # =============================================================================

    if not form.select_fixed_vertices():
        return

    # =============================================================================
    # Update Scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Form Select Fixed Vertices")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
