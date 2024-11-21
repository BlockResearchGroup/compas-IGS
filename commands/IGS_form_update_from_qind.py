#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas_ags.ags import form_update_q_from_qind
from compas_igs.session import IGSSession
from compas_igs.utilities import check_equilibrium

# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    form = session.find_formdiagram(warn=True)
    if not form:
        return

    force = session.find_forcediagram(warn=False)

    # =============================================================================
    # Command
    # =============================================================================

    form_update_q_from_qind(form.diagram)

    # =============================================================================
    # Check equilibrium
    # =============================================================================

    if force:
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
            session.set("equilibrium", True)
            session.settings.form.show_external_force_labels = True

        else:
            print("The diagrams ARE NOT in equilibrium.")

            session.set("equilibrium", False)
            session.settings.form.show_external_force_labels = False
            session.settings.form.show_independent_edge_labels = True

    # =============================================================================
    # Update scene
    # =============================================================================

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Form Update From Qind")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
