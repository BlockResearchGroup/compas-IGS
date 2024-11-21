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

    if force.select_fixed_vertices():
        rs.UnselectAllObjects()

        force.redraw_vertices()

        if session.settings.autosave:
            session.record(name="Force Select Fixed Vertices")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
