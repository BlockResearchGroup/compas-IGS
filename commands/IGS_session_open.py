#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

from compas_igs.session import IGSSession
from compas_rui.forms import FileForm

# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    filepath = FileForm.open(session.basedir)
    if not filepath:
        return

    session.scene.clear()
    session.load(filepath)

    form = session.find_formdiagram(warn=False)
    force = session.find_forcediagram(warn=False)

    if form and force:
        form.diagram.dual = force.diagram
        force.diagram.dual = form.diagram

    session.scene.draw()

    if session.settings.autosave:
        session.record(name="Open Session")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
