#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

from compas_igs.session import IGSSession

# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    if not session.confirm("This will clear all objects from the scene. Proceed?"):
        return

    session.scene.clear()

    if session.settings.autosave:
        session.record(name="Clear Scene")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
