#! python3
# venv: brg-csd
# r: compas_session>=0.4.5, compas_ags>=1.3.1

import pathlib

import Eto.Drawing  # type: ignore
import Eto.Forms  # type: ignore
import Rhino  # type: ignore
import Rhino.UI  # type: ignore
import System  # type: ignore

pluginfile = Rhino.PlugIns.PlugIn.PathFromId(System.Guid("ea785b43-c1c1-43da-b896-69df6c0e4b19"))
shared = pathlib.Path(str(pluginfile)).parent / "shared"


class SplashForm(Eto.Forms.Dialog[bool]):
    def __init__(self, title, url, width=800, height=400):
        super().__init__()

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = False
        self.ClientSize = Eto.Drawing.Size(width, height)
        # self.WindowStyle = Eto.Forms.WindowStyle.NONE  # type: ignore

        webview = Eto.Forms.WebView()
        webview.Size = Eto.Drawing.Size(width, height)
        webview.Url = System.Uri(url)
        webview.BrowserContextMenuEnabled = False
        webview.DocumentLoading += self.action

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical()
        layout.AddRow(webview)
        layout.EndVertical()
        self.Content = layout

    def action(self, sender, e):
        if e.Uri.Scheme == "action" and e.Uri.Host == "close":
            self.Close()

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


def RunCommand():
    form = SplashForm(title="COMPAS IGS", url=str(shared / "index.html"))
    form.show()


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
