#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas_ags.ags import force_update_from_form
from compas_ags.ags import form_count_dof
from compas_ags.ags import form_update_q_from_qind
from compas_ags.diagrams import ForceDiagram
from compas_igs.scene import RhinoForceObject
from compas_igs.session import IGSSession
from compas_igs.utilities import compute_force_drawinglocation
from compas_igs.utilities import compute_force_drawingscale
from compas_igs.utilities import compute_form_forcescale

# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    form = session.find_formdiagram(warn=True)
    if not form:
        return

    force = session.find_forcediagram(warn=False)
    if force:
        if not session.confirm("This will replace the existing ForceDiagram. Do you want to proceed?"):
            return

        force.clear()
        session.scene.remove(force)

    # =============================================================================
    # <COMMAND>
    # =============================================================================

    edges = list(form.diagram.edges_where(is_ind=True))

    if not len(edges):
        return session.warn(
            message="""You have not yet assigned force values to the form diagram.
            Please assign forces first."""
        )

    k, m = form_count_dof(form.diagram)

    if k != len(edges):
        return session.warn(
            message="""You have not assigned the correct number of force values.
            Please, check the degrees of freedom of the form diagram and update the assigned forces accordingly."""
        )

    formdiagram = form.diagram
    forcediagram = ForceDiagram.from_formdiagram(formdiagram)

    form_update_q_from_qind(formdiagram)
    force_update_from_form(forcediagram, formdiagram)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    force: RhinoForceObject = session.scene.add(forcediagram)

    drawingscale = compute_force_drawingscale(form, force)  # scale factor for the diagram
    drawinglocation = compute_force_drawinglocation(form, force)  # translation of the diagram
    forcescale = compute_form_forcescale(form)  # thickness

    force.scale = drawingscale
    force.location = drawinglocation
    form.scale_internal_forcepipes = forcescale

    form.show_internal_forcepipes = True

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Force From Form")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
