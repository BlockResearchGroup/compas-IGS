#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas_ags.ags import form_update_from_force
from compas_igs.session import IGSSession
from compas_igs.utilities import check_equilibrium
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

    # =============================================================================
    # Command
    # =============================================================================

    # include in while loop

    selected = force.select_vertices_manual()
    if not selected:
        return

    if force.move_vertices(selected):
        force.redraw()

        if session.settings.autoupdate:
            form_update_from_force(form.diagram, force.diagram)
            form.redraw()

    # =============================================================================
    # Check equilibrium
    # =============================================================================

    # max_angle = session.settings.solver.max_angle
    # min_force = session.settings.solver.min_force

    # compute_angle_deviations(form.diagram, force.diagram, tol_force=min_force)
    # check = check_equilibrium(form.diagram, force.diagram, tol_angle=max_angle, tol_force=min_force)
    # deviation = max(form.diagram.edges_attribute("a"))

    # if check:
    #     message = f"Diagrams are parallel!\nMax. angle deviation: {deviation:.2g} deg\nThreshold assumed: {max_angle:.2g} deg."
    # else:
    #     message = f"Diagrams are not parallel!\nMax. angle deviation: {deviation:.2g} deg\nThreshold assumed: {max_angle:.2g} deg."

    # rs.MessageBox(message, title="Info")

    # =============================================================================
    # Update scene
    # =============================================================================

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Force Move Nodes")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
