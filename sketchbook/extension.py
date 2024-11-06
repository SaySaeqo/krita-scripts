import krita
from . import create
from . import next_page
import PyQt5.QtWidgets as QtWidgets
import os
import subprocess
import platform

class SketchbookExtension(krita.Extension):
    def __init__(self, parent):
        super().__init__(parent)
    
    def setup(self):
        pass

    def open_folder(self):
        doc = krita.Krita.instance().activeDocument()
        path = os.path.dirname(doc.fileName())
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])

    def createActions(self, window):
        action = window.createAction("sketchbook", "Sketchbook", "tools")
        menu = QtWidgets.QMenu("sketchbook", window.qwindow())
        action.setMenu(menu)

        sketchbook_next_page = window.createAction("sketchbook_next_page", None, "tools/sketchbook")
        sketchbook_next_page.triggered.connect(next_page.open_next_page)

        sketchbook_create = window.createAction("sketchbook_create", None, "tools/sketchbook")
        sketchbook_create.triggered.connect(create.show_dialog)

        sketchbook_folder = window.createAction("sketchbook_folder", None, "tools/sketchbook")
        sketchbook_folder.triggered.connect(self.open_folder)


app = krita.Krita.instance()
app.addExtension(SketchbookExtension(app))