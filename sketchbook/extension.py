import krita
from . import create
from . import next_page
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore

class SketchbookExtension(krita.Extension):
    def __init__(self, parent):
        super().__init__(parent)
    
    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("sketchbook", "Sketchbook", "tools")
        menu = QtWidgets.QMenu("sketchbook", window.qwindow())
        action.setMenu(menu)

        sketchbook_next_page = window.createAction("sketchbook_next_page", None, "tools/sketchbook")
        sketchbook_next_page.triggered.connect(next_page.open_next_page)

        sketchbook_create = window.createAction("sketchbook_create", None, "tools/sketchbook")
        sketchbook_create.triggered.connect(create.show_dialog)


app = krita.Krita.instance()
app.addExtension(SketchbookExtension(app))