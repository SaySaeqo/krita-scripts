from krita import *

app = Krita.instance()
doc = app.activeDocument()

node = doc.activeNode()
name = node.name()

# opacity to 30% and new layer
node.setOpacity(80)
name = name.replace("malowania","szkicu")
node.setName(name)
app.action('add_new_paint_layer').trigger()


doc.refreshProjection()