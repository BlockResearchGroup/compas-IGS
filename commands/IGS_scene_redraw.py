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

    session.scene.redraw()
    rs.Redraw()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
