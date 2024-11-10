from pydantic import BaseModel
from pydantic import Field

from compas_session.settings import Settings


class AgsSettings(BaseModel):
    kmax: int = 100
    max_angle: float = Field(default=0.5, description="Maximum angle between parallel edges.")
    min_force: float = Field(default=0.05, description="Minimum length of force edges.")

    tol_length: float = Field(default=0.05, description="Tolerance for devation from force length.")


class DrawingSettings(BaseModel):
    show_reactions: bool = True
    show_forces: bool = True
    show_residuals: bool = False
    show_loads: bool = False

    scale_reactions: float = 1e-1
    scale_residuals: float = 1.0
    scale_loads: float = 1.0

    tol_reactions: float = 1e-3
    tol_residuals: float = 1e-3
    tol_loads: float = 1e-3


class IGSSettings(Settings):
    ags: AgsSettings = AgsSettings()
    drawing: DrawingSettings = DrawingSettings()
    autoupdate: bool = False
