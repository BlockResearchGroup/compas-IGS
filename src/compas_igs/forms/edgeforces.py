import ast
from typing import Any

import Eto.Drawing  # type: ignore
import Eto.Forms  # type: ignore
import Rhino  # type: ignore
import Rhino.UI  # type: ignore
from pydantic import BaseModel


class Header(BaseModel):
    text: str
    editable: bool = False
    expand: bool = True
    width: int = 0


class EdgeForcesForm(Eto.Forms.Dialog[bool]):
    """"""

    def __init__(
        self,
        rows: list[list[Any]],
        title: str = "Edge Forces",
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

        headers = [
            Header(text="Index", editable=False, expand=False, width=48),
            Header(text="Edge (Vertex Pair)", editable=False, expand=True),
            Header(text="Force", editable=True, expand=False, width=96),
        ]

        for index, header in enumerate(headers):
            column = Eto.Forms.GridColumn()
            column.HeaderText = header.text
            column.Editable = header.editable
            column.Expand = header.expand
            if header.width != 0:
                column.Width = header.width
            column.DataCell = Eto.Forms.TextBoxCell(index)
            self.table.Columns.Add(column)

        data = []
        for index, row in enumerate(rows):
            item = Eto.Forms.GridItem()
            item.Values = [repr(value) for value in row]
            data.append(item)
        self.table.DataStore = data

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
        for row in self.table.DataStore:
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
    form = EdgeForcesForm(
        rows=[
            [0, (0, 1), 3],
            [1, (0, 2), 5],
        ],
    )
    if form.show():
        for row in form.rows:
            print(row)
