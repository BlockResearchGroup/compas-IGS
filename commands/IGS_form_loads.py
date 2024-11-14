#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

import rhinoscriptsyntax as rs  # type: ignore

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
    # Loads
    # =============================================================================

    if not form.select_independent_edges():
        return

    rs.UnselectAllObjects()
    form.assign_forces()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Form Loads")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
