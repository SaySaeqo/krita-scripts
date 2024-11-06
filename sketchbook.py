import krita
import os
import logging

SKETCHBOOK_DOCUMENT_NAME = "Kartka szkicownika"
LOGGER_NAME = "sketchbook-script"

def _export_page(sketchbook_path, page_prefix = "") -> (int, int):
    doc = krita.Krita.instance().activeDocument()
    info = krita.InfoObject()
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

def _create_new_page(width, height, current_page_path):
    app = krita.Krita.instance()
    doc = app.createDocument(width, height, SKETCHBOOK_DOCUMENT_NAME, "RGBA", "U8", "", 300.0)
    app.activeWindow().addView(doc)
    app.setActiveDocument(doc)
    # add empty layer
    app.action('add_new_paint_layer').trigger()
    # save new page
    doc.saveAs(current_page_path)

def _create_new_page_from_template(template_path: str, current_page_path):
    app = krita.Krita.instance()
    doc = app.openDocument(template_path)
    app.activeWindow().addView(doc)
    app.setActiveDocument(doc)
    # save new page
    doc.saveAs(current_page_path)

def open_next_page():
    log = logging.getLogger(LOGGER_NAME)
    doc = krita.Krita.instance().activeDocument()
    if not doc:
        log.warning("Skechbook page was not saved - no active document")
        return
    
    last_path = doc.fileName()
    if not last_path or not last_path.endswith("last.kra"):
        log.warning("Skechbook page was not saved - that is not a sketchbook page")
        return
    
    sketchbook_path = os.path.dirname(last_path) + "/"
    sketchbook_prefix = os.path.basename(last_path).removesuffix("last.kra")
    template_path = sketchbook_path + sketchbook_prefix + "template.kra"

    
    w, h = doc.width(), doc.height()
    filepath = _export_page(sketchbook_path, sketchbook_prefix)
    if not os.path.exists(filepath):
        log.warning("Skechbook page was not saved - declined by user")
        return
    
    doc.save()
    doc.close()
    if os.path.exists(template_path):
        _create_new_page_from_template(template_path, last_path)
    else:
        _create_new_page(w, h, last_path)
    log.info("Sketchbook page was saved")


open_next_page()