#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore  # noqa: F401

import compas_rhino.conversions
import compas_rhino.objects
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

    # =============================================================================
    # Command
    # =============================================================================

    vertex = force.select_anchor()
    if vertex is None:
        return

    force.anchor = vertex

    vertex_guid = {v: k for k, v in force._guid_vertex.items()}
    force.location = compas_rhino.conversions.pointobject_to_compas(vertex_guid[vertex])

    # =============================================================================
    # Update Scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Force Select Anchor")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
