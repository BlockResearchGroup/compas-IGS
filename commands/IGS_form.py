#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

import rhinoscriptsyntax as rs  # type: ignore

from compas_igs.commands.form import create_from_lines
from compas_igs.commands.form import create_from_meshgrid
from compas_igs.commands.form import create_from_obj
from compas_igs.session import IGSSession

# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    form = session.find_formdiagram(warn=False)
    if form:
        if not session.confirm("This will remove the existing digrams. Do you want to procced?"):
            return
        session.clear()

    # =============================================================================
    # Create form diagram
    # =============================================================================

    option = rs.GetString(message="FormDiagram From", strings=["RhinoLines", "MeshGrid", "OBJ"])
    if not option:
        return

    if option == "RhinoLines":
        formdiagram = create_from_lines()

    elif option == "MeshGrid":
        formdiagram = create_from_meshgrid()

    elif option == "OBJ":
        formdiagram = create_from_obj(session.basedir)

    else:
        raise NotImplementedError

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    if not formdiagram:
        return

    session.scene.add(formdiagram)
    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Create FormDiagram")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
