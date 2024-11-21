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

    force = session.find_forcediagram(warn=True)
    if not force:
        return

    # =============================================================================
    # Apply constraints
    # =============================================================================

    option = rs.GetString("Constraint Type", strings=["Direction", "Force"])
    if not option:
        return

    if option == "Direction":
        pass

    elif option == "Force":
        pass

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Update Form Edge Constraints")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
