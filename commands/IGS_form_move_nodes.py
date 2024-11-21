#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas_ags.ags import force_update_from_form
from compas_ags.ags import form_update_q_from_qind
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
    # Command
    # =============================================================================

    # include in while loop

    # selectable = set(form.diagram.vertices_where(is_fixed=False))
    # temp = set(form.select_vertices())
    # selected = list(selectable & temp)

    selected = form.select_vertices_manual()

    if not selected:
        return

    if form.move_vertices(selected):
        form.redraw()

        if session.settings.autoupdate:
            form_update_q_from_qind(form.diagram)
            force_update_from_form(form.diagram)
            force.redraw()

    # =============================================================================
    # Update scene
    # =============================================================================

    # check equilibrium
    # turn of forces if no equilibrium
    # turn off external labels if no equilibrium

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Form Move Nodes")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
