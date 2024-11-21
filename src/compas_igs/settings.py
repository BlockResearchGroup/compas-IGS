from pydantic import BaseModel
from pydantic import Field

from compas_session.settings import Settings


class SolverSettings(BaseModel):
    maxiter: int = 20  # maximum number of diagram updates
    kmax: int = 20  # maximum number of parallelisation iterations
    max_angle: float = Field(default=0.5, description="Maximum angle between parallel edges.")
    min_force: float = Field(default=0.05, description="Minimum length of force edges to be considered nonzero.")
    max_ldiff: float = Field(default=0.05, description="Maximum deviation of edges from their target length/force.")


class FormDiagramSettings(BaseModel):
    pass


class ForceDiagramSettings(BaseModel):
    pass


class IGSSettings(Settings):
    autoupdate: bool = False
    solver: SolverSettings = SolverSettings()
    form: FormDiagramSettings = FormDiagramSettings()
    force: ForceDiagramSettings = ForceDiagramSettings()
