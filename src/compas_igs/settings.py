from pydantic import BaseModel
from pydantic import Field

from compas_session.settings import Settings


class SolverSettings(BaseModel):
    kmax: int = 100
    max_angle: float = Field(default=0.5, description="Maximum angle between parallel edges.")
    min_force: float = Field(default=0.05, description="Minimum length of force edges.")

    tol_length: float = Field(default=0.05, description="Tolerance for devation from force length.")


class FormDiagramSettings(BaseModel):
    show_labels: bool = True


class ForceDiagramSettings(BaseModel):
    show_labels: bool = True


class IGSSettings(Settings):
    autoupdate: bool = False

    solver: SolverSettings = SolverSettings()
    form: FormDiagramSettings = FormDiagramSettings()
    force: ForceDiagramSettings = ForceDiagramSettings()
