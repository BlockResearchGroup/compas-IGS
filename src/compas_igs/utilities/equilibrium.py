from compas.geometry import angle_vectors_xy
from compas.geometry import distance_point_point_xy
from compas.geometry import subtract_vectors
from compas_ags.diagrams import ForceDiagram
from compas_ags.diagrams import FormDiagram


def compute_angle_deviations(form: FormDiagram, force: ForceDiagram, tol_force: float = 0.05) -> None:
    """Compute angle deviations based on the current position of the form and force diagram.

    Parameters
    ----------
    form : :class:`FormDiagram`
        The form diagram to check deviations.
    force : :class:`ForceDiagram`
        The force diagram to check deviations
    tol_force : float
        Distance tolerance to consider the null edges.
        The default value is ``0.05``.

    Returns
    -------
    None
        The form diagram is updated in place and the deviations are added as attributes.

    """

    edges_form = list(form.edges())
    edges_force = force.ordered_edges(form)

    for i in range(len(edges_form)):
        pt0, pt1 = form.edge_coordinates(edges_form[i][0], edges_form[i][1])
        _pt0, _pt1 = force.edge_coordinates(edges_force[i][0], edges_force[i][1])

        a = angle_vectors_xy(subtract_vectors(pt1, pt0), subtract_vectors(_pt1, _pt0), deg=True)
        a = min(a, 180 - a)

        if distance_point_point_xy(_pt0, _pt1) < tol_force:
            a = 0.0  # exclude edges with zero-force

        form.edge_attribute(edges_form[i], "a", a)


def check_form_angle_deviations(form: FormDiagram, tol_angle: float = 0.5) -> bool:
    """Checks whether the tolerances stored in the form force diagrams are indeed below the threshold.

    Note: the form diagram should have the angle deviations updated and stored in the attributes.

    Parameters
    ----------
    form : :class:`FormDiagram`
        The form diagram to check deviations.
    tol_angle : float, optional
        Stopping criteria tolerance for angle deviations.
        The default value is ``0.5``.

    Returns
    -------
    checked : bool
        Return whether of not the diagram passes the check with no deviations greater than the tolerance.

    """

    checked = True

    deviations = form.edges_attribute("a")
    max_deviation = max(deviations)
    if max_deviation > tol_angle:
        checked = False

    return checked


def check_force_length_constraints(force: ForceDiagram, tol_force: float = 0.05) -> bool:
    """Checks whether target length constraints applied to the force diagrams are respected, i.e. are below the tolerance criteria.

    Parameters
    ----------
    force : :class:`ForceDiagram`
        The force diagram to check deviations.
    tol_forces : float, optional
        Stopping criteria tolerance for the edge lengths (i.e. force magnitude) in the force diagram.
        The default value is ``0.05``.

    Returns
    -------
    checked : bool
        Return whether of not the diagram passes the check with no deviations greater than the tolerance.

    """
    checked = True

    for u, v in force.edges():
        target_constraint = force.dual_edge_targetforce((u, v))
        if target_constraint:
            length = force.edge_length(u, v)
            diff = abs(length - target_constraint)
            if diff > tol_force:
                checked = False
                break

    return checked


def check_equilibrium(form: FormDiagram, force: ForceDiagram, tol_angle: float = 0.5, tol_force: float = 0.05) -> bool:
    """Checks if maximum deviations and constraints exceed is below the tolerance.

    Parameters
    ----------
    form : :class:`FormDiagram`
        The form diagram to check equilibrium.
    force : :class:`ForceDiagram`
        The force diagram to check equilibrium.
    tol_angle : float, optional
        Stopping criteria tolerance for angle deviations.
        The default value is ``0.5``.
    tol_force : float, optional
        Stopping criteria tolerance for the constraints on the length.
        The default value is ``0.05``.

    Returns
    -------
    checked : bool
        Return whether of not the diagram passes the check.

    """

    compute_angle_deviations(form, force, tol_force=tol_force)
    check_form = check_form_angle_deviations(form, tol_angle=tol_angle)
    check_force = check_force_length_constraints(force, tol_force=tol_force)
    checked = check_form and check_force

    return checked
