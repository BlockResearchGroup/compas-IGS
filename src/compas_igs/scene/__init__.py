from compas.plugins import plugin
from compas.scene.context import register

from compas_ags.diagrams import ForceDiagram
from compas_ags.diagrams import FormDiagram

from .forceobject import RhinoForceObject
from .formobject import RhinoFormObject


@plugin(category="factories", pluggable_name="register_scene_objects", requires=["Rhino"])
def register_scene_objects_rhino():
    register(FormDiagram, RhinoFormObject, context="Rhino")
    register(ForceDiagram, RhinoForceObject, context="Rhino")
