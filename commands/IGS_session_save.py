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

    filepath = FileForm.save(session.basedir, "compas-IGS.json")
    if not filepath:
        return

    session.dump(filepath)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
