#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

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
    # Command
    # =============================================================================

    form.assign_forces()

    # =============================================================================
    # Update Scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.set("equilibrium", False)
    session.settings.form.show_external_force_labels = False
    session.settings.form.show_independent_edge_labels = True

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Form Assign Forces")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
