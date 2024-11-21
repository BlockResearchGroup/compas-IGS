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

            is_external = False
            is_ind = False
            is_compression = False
            is_tension = False

            for index, model in enumerate(self.attributes):
                value = e.Item.GetValue(index + 2)
                value = ast.literal_eval(value)

                if model.name == "f":
                    is_compression = value < 0
                    is_tension = value > 0

                elif model.name == "is_external":
                    is_external = value

                elif model.name == "is_ind":
                    is_ind = value

            if is_ind:
                e.BackgroundColor = Eto.Drawing.Colors.Cyan
                e.ForegroundColor = Eto.Drawing.Colors.White
            elif is_external:
                e.BackgroundColor = Eto.Drawing.Colors.Green
                e.ForegroundColor = Eto.Drawing.Colors.White
            elif is_compression:
                e.BackgroundColor = Eto.Drawing.Colors.Blue
                e.ForegroundColor = Eto.Drawing.Colors.White
            elif is_tension:
                e.BackgroundColor = Eto.Drawing.Colors.Red
                e.ForegroundColor = Eto.Drawing.Colors.White

        self.attributes = attributes
        self.edges = edges

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
        for index, edge in enumerate(self.edges):
            values = [repr(index), repr(edge)]
            for model in self.attributes:
                value = self.edges[edge][model.name]
                if not model.editable and model.value is float:
                    value = round(value, 3)
                values.append(repr(value))
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
                if model.editable:
                    edges[edge][model.name] = ast.literal_eval(row.GetValue(2 + i))
                else:
                    edges[edge][model.name] = self.edges[edge][model.name]
        return edges

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
