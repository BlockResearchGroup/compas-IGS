import os

from compas_rui.rui import Rui

HERE = os.path.dirname(__file__)
UI = os.path.join(HERE, "ui.json")
RUI = os.path.join(HERE, "IGS.rui")

rui = Rui.from_json(UI, RUI)

rui.write()
