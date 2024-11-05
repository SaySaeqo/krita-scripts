### copied from sketchbook.py

from krita import Krita, InfoObject
import os
import logging

SKETCHBOOK_DOCUMENT_NAME = "Kartka szkicownika"
LOGGER_NAME = "sketchbook-script"

def _export_page(sketchbook_path, page_prefix = "") -> (int, int):
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
    while os.path.exists(sketchbook_path + page_prefix + str(i) + ".png"):
        i += 1
    # export and close
    filepath = sketchbook_path + page_prefix + str(i) + ".png"
    doc.exportImage(filepath, info)
    return filepath

def _create_new_page(width, height, sketchbook_path, current_page_filename):
    app = Krita.instance()
    doc = app.createDocument(width, height, SKETCHBOOK_DOCUMENT_NAME, "RGBA", "U8", "", 300.0)
    app.activeWindow().addView(doc)
    app.setActiveDocument(doc)
    # add empty layer
    app.action('add_new_paint_layer').trigger()
    # save new page
    doc.saveAs(sketchbook_path + current_page_filename + ".kra")

def _create_new_page_from_template(template_path: str, sketchbook_path: str, current_page_filename = "last"):
    app = Krita.instance()
    doc = app.openDocument(template_path)
    app.activeWindow().addView(doc)
    app.setActiveDocument(doc)
    # save new page
    doc.saveAs(sketchbook_path + current_page_filename + ".kra")

def open_next_page(sketchbook_path: str, current_page_filename = "last", template_path = None, exported_page_prefix = ""):
    """
    :sketchbook_path: path to chosen sketchbook folder ended with '/'
    :current_page_filename: name for .kra file with last, not exported yet, page (without extension)
    """
    log = logging.getLogger(LOGGER_NAME)
    doc = Krita.instance().activeDocument()
    if not doc:
        log.warning("Skechbook page was not saved - no active document")
        return
    
    last = doc.fileName()
    if not last or last != sketchbook_path + current_page_filename + ".kra":
        log.warning("You are trying to save page from different sketchbook")
        return
    
    w, h = doc.width(), doc.height()
    filepath = _export_page(sketchbook_path, exported_page_prefix)
    if not os.path.exists(filepath):
        log.warning("Skechbook page was not saved - declined by user")
        return
    
    doc.save()
    doc.close()
    if template_path:
        _create_new_page_from_template(template_path, sketchbook_path, current_page_filename)
    else:
        _create_new_page(w, h, sketchbook_path, current_page_filename)
    log.info("Sketchbook page was saved")

### end of copied from sketchbook.py


open_next_page("/home/saysaeqo/Dropbox/HomePictures/manga/", 
                          current_page_filename="manga_last",
                          template_path="/home/saysaeqo/Dropbox/HomePictures/komiks_s.kra",
                          exported_page_prefix="manga_")