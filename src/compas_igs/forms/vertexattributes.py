#! python3
# venv: brg-csd

import ast
from typing import Any
from typing import Type

import Eto.Drawing  # type: ignore
import Eto.Forms  # type: ignore
import Rhino  # type: ignore
import Rhino.UI  # type: ignore
from pydantic import BaseModel


class Attribute(BaseModel):
    name: str
    value: Type
    text: str
    editable: bool = False
    expand: bool = False
    width: int = 0


class VertexAttributesForm(Eto.Forms.Dialog[bool]):
    """"""

    def __init__(
        self,
        attributes: list[Attribute],
        vertices: dict[tuple[int, int], Any],
        title: str = "Vertex Attributes",
        width: int = 500,
        height: int = 500,
    ) -> None:
        super().__init__()

        def on_cell_formatting(sender, e):
            if not e.Column.Editable:
                e.ForegroundColor = Eto.Drawing.Colors.Gray

        self.attributes = attributes

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        self.table = Eto.Forms.GridView()
        self.table.ShowHeader = True
        self.table.CellFormatting += on_cell_formatting

        # index column
        column = Eto.Forms.GridColumn()
        column.HeaderText = "Index"
        column.Editable = False
        column.Expand = False
        column.Width = 48
        column.DataCell = Eto.Forms.TextBoxCell(0)
        self.table.Columns.Add(column)

        # vertex column
        column = Eto.Forms.GridColumn()
        column.HeaderText = "Vertex"
        column.Editable = False
        column.Expand = True
        column.Width = 48
        column.DataCell = Eto.Forms.TextBoxCell(1)
        self.table.Columns.Add(column)

        # attribute columns
        for index, model in enumerate(self.attributes):
            column = Eto.Forms.GridColumn()
            column.HeaderText = model.text
            column.Editable = model.editable
            column.Expand = model.expand
            if model.width != 0:
                column.Width = model.width
            column.DataCell = Eto.Forms.TextBoxCell(index + 2)
            self.table.Columns.Add(column)

        # vertex data rows
        rows = []
        for index, vertex in enumerate(vertices):
            values = [repr(index), repr(vertex)]
            for model in self.attributes:
                values.append(repr(vertices[vertex][model.name]))
            row = Eto.Forms.GridItem()
            row.Values = values
            rows.append(row)
        self.table.DataStore = rows

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(Eto.Drawing.Padding(0, 0, 0, 0), Eto.Drawing.Size(0, 0), True, True)
        layout.AddRow(self.table)
        layout.EndVertical()
        layout.BeginVertical(Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(6, 0), False, False)
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndVertical()

        self.Content = layout

    @property
    def ok(self):
        self.DefaultButton = Eto.Forms.Button()
        self.DefaultButton.Text = "OK"
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button()
        self.AbortButton.Text = "Cancel"
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    @property
    def vertexdata(self):
        vertices = {}
        for row in self.table.DataStore:
            vertex = ast.literal_eval(row.getValue(1))
            vertices[vertex] = {}
            for i, model in enumerate(self.attributes):
                vertices[vertex][model.name] = ast.literal_eval(row.GetValue(2 + i))
        return vertices

    def on_ok(self, sender, event):
        self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    from compas.datastructures import Mesh

    mesh = Mesh.from_meshgrid(10, 10)
    mesh.update_default_vertex_attributes({"a": 1.0, "b": 10, "c": False})

    attributes = [
        Attribute(name="a", text="A", value=float, width=48),
        Attribute(name="b", text="B", value=float, width=48),
        Attribute(name="c", text="C", value=float, width=48),
    ]

    vertices = {}
    for vertex in mesh.vertices():
        vertices[vertex] = {}
        for attr in attributes:
            vertices[vertex][attr.name] = mesh.vertex_attribute(vertex, name=attr.name)

    form = VertexAttributesForm(attributes, vertices)

    if form.show():
        for vertex, data in form.vertexdata.items():
            for attr, value in zip(attributes, data):
                print(attr.name, value)
