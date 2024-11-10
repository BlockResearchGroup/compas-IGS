import rhinoscriptsyntax as rs  # type: ignore

from compas_igs.settings import IGSSettings
from compas_session.session import Session


class IGSSession(Session):
    settings: IGSSettings

    def __new__(cls, **kwargs):
        if "name" in kwargs:
            del kwargs["name"]
        return super().__new__(cls, name="compas-IGS")

    def __init__(self, **kwargs):
        if "name" in kwargs:
            del kwargs["name"]
        super().__init__(name="compas-IGS", settings=IGSSettings(), **kwargs)

    def clear(self, clear_scene=True, clear_context=True):
        for sceneobject in self.scene.objects:
            if hasattr(sceneobject, "clear_conduits"):
                sceneobject.clear_conduits()
        self.scene.clear(clear_scene=clear_scene, clear_context=clear_context)

    def clear_conduits(self):
        for sceneobject in self.scene.objects:
            if hasattr(sceneobject, "clear_conduits"):
                sceneobject.clear_conduits()

    def find_formdiagram(self, warn=True):
        from compas_ags.diagrams import FormDiagram
        from compas_igs.scene import RhinoFormObject

        obj: RhinoFormObject = self.scene.find_by_itemtype(FormDiagram)
        if obj:
            return obj
        if warn:
            rs.MessageBox(
                message="There is no FormDiagram.",
                title="Warning",
            )

    def find_forcediagram(self, warn=True):
        from compas_ags.diagrams import ForceDiagram
        from compas_igs.scene import RhinoForceObject

        obj: RhinoForceObject = self.scene.find_by_itemtype(ForceDiagram)
        if obj:
            return obj
        if warn:
            rs.MessageBox(
                message="There is no ForceDiagram.",
                title="Warning",
            )

    def clear_all_formdiagrams(self, redraw=True):
        pass

    def clear_all_forcediagrams(self, redraw=True):
        pass

    def clear_all_diagrams(self, redraw=True):
        pass

    def confirm(self, message):
        result = rs.MessageBox(message, buttons=4 | 32 | 256 | 0, title="Confirmation")
        return result == 6

    def warn(self, message):
        return rs.MessageBox(message, title="Warning")
