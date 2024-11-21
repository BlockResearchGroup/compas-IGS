#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

from compas_ags.ags import form_count_dof
from compas_igs.session import IGSSession

# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    form = session.find_formdiagram(warn=True)
    if not form:
        return

    # =============================================================================
    # Command
    # =============================================================================

    k, m = form_count_dof(form.diagram)
    inds = len(list(form.diagram.edges_where(is_ind=True)))

    if k == inds:
        message = "Success: You have identified the correct number of externally applied loads."
    elif k > inds:
        message = f"Warning: You have not yet identified all external loads. ({k} required and {inds} selected)"
    else:
        message = f"Warning: You have identified too many external forces as loads. ({k} required and {inds} selected)"

    rs.MessageBox(message, title="Info")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
