#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas_ags.ags import form_update_from_force
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

    form_update_from_force(form.diagram, force.diagram)

    # feedback on equilibrium

    form.redraw()

    if session.settings.autosave:
        session.record(name="Form Update From Force")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
