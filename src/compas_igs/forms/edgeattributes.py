import ast
from typing import Any

import Eto.Drawing  # type: ignore
import Eto.Forms  # type: ignore
import Rhino  # type: ignore
import Rhino.UI  # type: ignore

from .attribute import Attribute


class EdgeAttributesForm(Eto.Forms.Dialog[bool]):
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
        self.table.GridLines = Eto.Forms.GridLines.Horizontal
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
        self.DefaultButton.Text = "OK"
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    def on_ok(self, sender, event):
        self.Close(True)

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button()
        self.AbortButton.Text = "Cancel"
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    def on_cancel(self, sender, event):
        self.Close(False)

    @property
    def edgedata(self):
        edges = {}
        for row in self.table.DataStore:
            edge = ast.literal_eval(row.getValue(1))
            edges[edge] = {}
            for i, model in enumerate(self.attributes):
                edges[edge][model.name] = ast.literal_eval(row.GetValue(2 + i))
        return edges

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
