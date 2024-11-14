#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas_ags.ags import compute_loadpath
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

    lp = compute_loadpath(form.diagram, force.diagram)

    rs.MessageBox(f"The total load-path of the structure is {lp:.2f} kNm.", title="Info")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
