#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

from compas_igs.session import IGSSession

# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    oldscene = session.scene

    if not session.redo():
        return

    oldscene.clear()

    form = session.find_formdiagram(warn=False)
    force = session.find_forcediagram(warn=False)

    if form and force:
        form.diagram.dual = force.diagram
        force.diagram.dual = form.diagram

    session.scene.draw()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
