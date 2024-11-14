import json
import os
import zipfile

from compas_rui.rui import Rui

HERE = os.path.dirname(__file__)
UI = os.path.abspath(os.path.join(HERE, "ui.json"))
RHPROJ = os.path.abspath(os.path.join(HERE, "../plugin/IGS.rhproj"))
RUI = os.path.abspath(os.path.join(HERE, "../plugin/build/rh8/COMPAS-IGS.rui"))
YAK = os.path.abspath(os.path.join(HERE, "../plugin/build/rh8/compas-igs-0.2.9.9085-rh8-any.yak"))

with open(RHPROJ, mode="rt") as f:
    rhproj = json.load(f)
    guid = rhproj["id"]

rui = Rui.from_json(UI, RUI, guid=guid)
rui.write()

with zipfile.ZipFile(YAK, mode="a", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.write(RUI, "COMPAS-IGS.rui")


# copy the existing archive
# create a new archive and add the contents of the build folder + the generated rui
