#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

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

    form.assign_forces()

    rs.UnselectAllObjects()

    if session.settings.autosave:
        session.record(name="Form Assign Forces")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
