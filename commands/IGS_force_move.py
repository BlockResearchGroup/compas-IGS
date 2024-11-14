#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

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

    if force.move():
        # move to update_location_from_current_anchorpoint
        vertex_guid = {v: k for k, v in force._guid_vertex.items()}
        guid = vertex_guid[force.anchor]
        rpoint = compas_rhino.objects.get_point_coordinates([guid])[0]
        point = compas_rhino.conversions.point_to_compas(rpoint)
        force.location = point

        force.redraw()

        if session.settings.autosave:
            session.record(name="Force Move")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
