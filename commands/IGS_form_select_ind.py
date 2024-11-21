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

    if form.select_independent_edges():
        rs.UnselectAllObjects()

        form.redraw_edges()

        if session.settings.autosave:
            session.record(name="Form Select Independent Edges")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
