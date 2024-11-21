from compas.geometry import Box
from compas.geometry import Point
from compas.geometry import bounding_box
from compas.geometry import bounding_box_xy
from compas.geometry import distance_point_point_xy
from compas.geometry import transform_points
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


def compute_force_drawinglocation(form: RhinoFormObject, force: RhinoForceObject, margin: float = 1.3) -> Point:
    """Compute an appropriate location for the force diagram.

    Parameters
    ----------
    form : :class:`compas_igs.scene.RhinoFormObject`
    force : :class:`compas_igs.scene.RhinoForceObject`

    Returns
    -------
    :class:`compas.geometry.Point`

    """
    location = force.location.copy()
    transformation = force.transformation

    points_form = form.diagram.vertices_attributes("xyz")
    points_force = transform_points(force.diagram.vertices_attributes("xyz"), transformation)

    bbox_form = Box.from_bounding_box(bounding_box(points_form))
    bbox_force = Box.from_bounding_box(bounding_box(points_force))

    y_form = bbox_form.ymin + 0.5 * (bbox_form.ymax - bbox_form.ymin)
    y_force = bbox_force.ymin + 0.5 * (bbox_force.ymax - bbox_force.ymin)

    dx = margin * (bbox_form.xmax - bbox_form.xmin) + (bbox_form.xmin - bbox_force.xmin)
    dy = y_form - y_force

    location[0] += dx
    location[1] += dy
    return location


def compute_form_forcescale(form: RhinoFormObject) -> float:
    """Calculate an appropriate scale to the thickness of the force pipes in the form diagram.
    This IS NOT the scale of the force diagram.

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
