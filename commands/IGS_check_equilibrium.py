#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

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

    force = session.find_forcediagram(warn=True)
    if not force:
        return

    # =============================================================================
    # Command
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

    if not result:
        message = "Diagrams ARE NOT in equilibrium."
    else:
        message = "Diagrams ARE in equilibrium."

    rs.MessageBox(message)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
