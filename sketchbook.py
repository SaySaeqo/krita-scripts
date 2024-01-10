from krita import Krita, InfoObject
from os import path

SKETCHBOOK_DOCUMENT_NAME = "Kartka szkicownika"
SAVED_SKETCHBOOK_LAST_PAGE_NAME = "last.kra"
PATH_TO_SKETCHBOOK = "/home/saysaeqo/Dropbox/HomePictures/sketchbook/"

def export_page() -> (int, int):
    doc = Krita.instance().activeDocument()
    info = InfoObject()
    info.setProperty("alpha", False)
    info.setProperty("compression", 9)
    info.setProperty("forceSRGB", False)
    info.setProperty("indexed", True)
    info.setProperty("interlaced", False)
    info.setProperty("saveSRGBProfile", False)
    info.setProperty("transparencyFillcolor", [255,255,255])
    # Get the next consecutive number for the file name
    i = 1
    while path.exists(PATH_TO_SKETCHBOOK + str(i) + ".png"):
        i += 1
    # export and close
    filepath = PATH_TO_SKETCHBOOK + str(i) + ".png"
    doc.exportImage(filepath, info)
    return filepath

def create_new_page(width, height):
    app = Krita.instance()
    doc = app.createDocument(width, height, SKETCHBOOK_DOCUMENT_NAME, "RGBA", "U8", "", 300.0)
    app.activeWindow().addView(doc)
    app.setActiveDocument(doc)
    # add empty layer
    app.action('add_new_paint_layer').trigger()
    # save new page
    doc.saveAs(PATH_TO_SKETCHBOOK + SAVED_SKETCHBOOK_LAST_PAGE_NAME)

doc = Krita.instance().activeDocument()
if doc and doc.name() == SKETCHBOOK_DOCUMENT_NAME:
    w, h = doc.width(), doc.height()
    filepath = export_page()
    if path.exists(filepath):
        doc.save()
        doc.close()
        create_new_page(w, h)
        print("Sketchbook page was saved")
    else: 
        print("Skechbook page was not saved - declined by user")
else:
    print("Skechbook page was not saved - wrong document")
