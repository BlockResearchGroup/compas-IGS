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


class EdgeAttributesForm(Eto.Forms.Dialog[bool]):
    """"""

    def __init__(
        self,
        attributes: list[Attribute],
        edges: dict[tuple[int, int], Any],
        title: str = "Edge Attributes",
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

        # edge column
        column = Eto.Forms.GridColumn()
        column.HeaderText = "Edge"
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

        # edge data rows
        rows = []
        for index, edge in enumerate(edges):
            values = [repr(index), repr(edge)]
            for model in self.attributes:
                values.append(repr(edges[edge][model.name]))
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
        self.DefaultButton.Text = "OK1"
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button()
        self.AbortButton.Text = "Cancel"
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    @property
    def temp(self):
        edges = {}
        for row in self.table.DataStore:
            edge = ast.literal_eval(row.getValue(1))
            edges[edge] = {}
            for i, model in enumerate(self.attributes):
                edges[edge][model.name] = ast.literal_eval(row.GetValue(2 + i))
        return edges

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
    mesh.update_default_edge_attributes({"q": 1.0, "f": 10, "is_ind": False})

    attributes = [
        Attribute(name="l", text="L", value=float, width=48),
        Attribute(name="q", text="Q", value=float, width=48),
        Attribute(name="f", text="F", value=float, width=48),
        Attribute(name="is_ind", text="IND", value=bool, width=48),
    ]

    edges = {}
    for edge in mesh.edges():
        edges[edge] = {}
        for attr in attributes:
            edges[edge][attr.name] = mesh.edge_attribute(edge, name=attr.name)

    form = EdgeAttributesForm(attributes, edges)

    if form.show():
        for edge, data in form.temp.items():
            for attr, value in zip(attributes, data):
                print(attr.name, value)
