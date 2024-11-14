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
    text: str
    editable: bool = False
    expand: bool = False
    width: int = 0
    value: Type


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

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        self.table = Eto.Forms.GridView()
        self.table.ShowHeader = True
        self.table.CellFormatting += on_cell_formatting

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Index"
        column.Editable = False
        column.Expand = False
        column.Width = 48
        column.DataCell = Eto.Forms.TextBoxCell(0)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Edge"
        column.Editable = False
        column.Expand = True
        column.DataCell = Eto.Forms.TextBoxCell(1)
        self.table.Columns.Add(column)

        for index, attribute in enumerate(attributes):
            column = Eto.Forms.GridColumn()
            column.HeaderText = attribute.text
            column.Editable = attribute.editable
            column.Expand = attribute.expand
            if attribute.width != 0:
                column.Width = attribute.width
            column.DataCell = Eto.Forms.TextBoxCell(index + 2)
            self.table.Columns.Add(column)

        collection = []
        for index, edge in enumerate(edges):
            values = [repr(index), repr(edge)]
            for attr in attributes:
                values.append(repr(edges[edge][attr.name]))
            item = Eto.Forms.GridItem()
            item.Values = values
            collection.append(item)
        self.table.DataStore = collection

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
    def rows(self):
        rows = []
        for row in form.table.DataStore:
            index = ast.literal_eval(row.GetValue(0))
            edge = ast.literal_eval(row.GetValue(1))
            force = ast.literal_eval(row.GetValue(2))
            rows.append([index, edge, force])
        return rows

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
    mesh.update_default_edge_attributes({"q": 1.0, "f": 10})

    attributes = [
        Attribute(name="l", text="L", value=float, width=48),
        Attribute(name="q", text="Q", value=float, width=48),
        Attribute(name="f", text="F", value=float, width=48),
        Attribute(name="is_ind", text="IND", value=bool, width=48),
    ]

    edges = {}
    for edge in mesh.edges():
        edges[edge] = {
            "q": mesh.edge_attribute(edge, "q"),
            "l": mesh.edge_length(edge),
            "f": mesh.edge_attribute(edge, "f"),
            "is_ind": mesh.edge_attribute(edge, "is_ind"),
        }

    form = EdgeAttributesForm(attributes, edges)

    if form.show():
        pass
