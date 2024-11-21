from compas.geometry import Box
from compas.geometry import Point
from compas.geometry import bounding_box
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


def compute_force_drawinglocation(form: RhinoFormObject, force: RhinoForceObject, margin: float = 2) -> Point:
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

    bbox_form = Box.from_bounding_box(bounding_box(form.diagram.vertices_attributes("xyz")))
    bbox_force = Box.from_bounding_box(bounding_box(force.diagram.vertices_attributes("xyz")))

    y_form = bbox_form.ymin + 0.5 * (bbox_form.ymax - bbox_form.ymin)
    y_force = bbox_force.ymin + 0.5 * (bbox_force.ymax - bbox_force.ymin)

    dx = margin * (bbox_form.xmax - bbox_form.xmin) + (bbox_form.xmin - bbox_force.xmin)
    dy = y_form - y_force

    point[0] += dx + (point[0] - bbox_force.xmin)
    point[1] += dy + (point[1] - bbox_force.ymin)
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
