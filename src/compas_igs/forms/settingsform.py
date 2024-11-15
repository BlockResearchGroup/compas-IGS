# import ast
# from typing import Any
# from typing import Type

import Eto.Drawing  # type: ignore
import Eto.Forms  # type: ignore
import Rhino  # type: ignore
import Rhino.UI  # type: ignore
from pydantic import BaseModel


class SettingsForm(Eto.Forms.Dialog[bool]):
    def __init__(self, model: BaseModel):
        super().__init__()
        self.model = model

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
