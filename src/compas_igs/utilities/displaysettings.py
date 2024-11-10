from compas.geometry import Point
from compas.geometry import bounding_box_xy
from compas.geometry import distance_point_point_xy
from compas_igs.scene import RhinoForceObject
from compas_igs.scene import RhinoFormObject


def compute_force_drawingscale(form: RhinoFormObject, force: RhinoForceObject) -> float:
    """Compute an appropriate scale factor to create the force diagram.

    Parameters
    ----------
    form : :class:`compas_igs.scene.RhinoFormObject`
    force : :class:`compas_igs.scene.RhinoForceObject`

    Returns
    -------
    float
        Appropriate scale factor to draw form and force diagram next to each other

    """
    form_bbox = bounding_box_xy(form.diagram.vertices_attributes("xyz"))
    force_bbox = bounding_box_xy(force.diagram.vertices_attributes("xyz"))
    form_diagonal = distance_point_point_xy(form_bbox[0], form_bbox[2])
    force_diagonal = distance_point_point_xy(force_bbox[0], force_bbox[2])
    return 0.75 * form_diagonal / force_diagonal


def compute_force_drawinglocation(form: RhinoFormObject, force: RhinoForceObject) -> Point:
    """Compute an appropriate location for the force diagram.

    Parameters
    ----------
    form : :class:`compas_igs.scene.RhinoFormObject`
    force : :class:`compas_igs.scene.RhinoForceObject`

    Returns
    -------
    :class:`compas.geometry.Point`

    """
    point = force.location.copy()

    form_xyz = list(form.diagram.vertices_attributes("xyz"))
    force_xyz = list(force.diagram.vertices_attributes("xyz"))
    form_xmax = max([xyz[0] for xyz in form_xyz])
    form_xmin = min([xyz[0] for xyz in form_xyz])
    form_ymin = min([xyz[1] for xyz in form_xyz])
    force_xmin = min([xyz[0] for xyz in force_xyz])
    force_ymin = min([xyz[1] for xyz in force_xyz])

    spacing = 0.5 * (form_xmax - form_xmin)

    point[0] += form_xmax + spacing - force_xmin
    point[1] += form_ymin - force_ymin
    return point


def compute_form_forcescale(form: RhinoFormObject) -> float:
    """Calculate an appropriate scale to the thickness of the forces in the form diagram.

    Parameters
    ----------
    form : :class:`compas_igs.scene.RhinoFormObject`

    Returns
    -------
    float
        Appropriate scale factor to thickness of form diagram lines.

    """
    q = [abs(form.diagram.edge_attribute(uv, "q")) for uv in form.diagram.edges_where({"is_external": False})]

    scale = 0.1 / max(q)
    return scale
