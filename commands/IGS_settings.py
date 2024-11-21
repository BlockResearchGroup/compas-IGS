#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.2

import rhinoscriptsyntax as rs  # type: ignore
from pydantic import BaseModel

from compas_igs.session import IGSSession
from compas_rui.forms import NamedValuesForm


def update_settings(model, title):
    names = []
    values = []
    for name, info in model.model_fields.items():
        if issubclass(info.annotation, BaseModel):
            continue
        names.append(name)
        values.append(getattr(model, name))
    form = NamedValuesForm(names, values, title=title)
    if form.show():
        for name, value in form.attributes.items():
            setattr(model, name, value)


# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = IGSSession()

    options = ["General", "Solver", "FormDiagram", "ForceDiagram"]

    while True:
        option = rs.GetString(message="Settings Section", strings=options)
        if not option:
            break

        if option == "General":
            update_settings(session.settings, title="General")

        elif option == "Solver":
            update_settings(session.settings.solver, title="Solver")

        elif option == "FormDiagram":
            update_settings(session.settings.form, title="FormDiagram")

        elif option == "ForceDiagram":
            update_settings(session.settings.force, title="ForceDiagram")

        session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Update settings")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
