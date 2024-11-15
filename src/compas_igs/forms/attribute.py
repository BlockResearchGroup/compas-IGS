from typing import Type

from pydantic import BaseModel


class Attribute(BaseModel):
    name: str
    value: Type
    text: str
    editable: bool = False
    expand: bool = False
    width: int = 0
