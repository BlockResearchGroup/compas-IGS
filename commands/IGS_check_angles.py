#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas_igs.session import IGSSession
from compas_igs.utilities import compute_angle_deviations

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

    max_angle = session.settings.solver.max_angle
    min_force = session.settings.solver.min_force

    compute_angle_deviations(form.diagram, force.diagram, tol_force=min_force)

    max_dev = max(form.diagram.edges_attribute("a"))
    result = max_dev <= max_angle

    if not result:
        message = f"Diagrams ARE NOT parallel: {max_dev} > {max_angle}"
    else:
        message = f"Diagrams ARE parallel: {max_dev} <= {max_angle}"

    rs.MessageBox(message)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
