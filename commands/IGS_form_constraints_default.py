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

    return session.warn("Constraints are not available yet.")

    form = session.find_formdiagram(warn=True)
    if not form:
        return

    force = session.find_forcediagram(warn=True)
    if not force:
        return

    # =============================================================================
    # Command
    # =============================================================================

    form.diagram.identify_constraints()
    force.diagram.constraints_from_dual()

    # =============================================================================
    # Update Scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Form Default Constraints")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
