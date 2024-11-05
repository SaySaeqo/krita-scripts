from krita import *

app = Krita.instance()
doc = app.activeDocument()

# get the current selected layer, called a 'node'
node = doc.activeNode()
op = node.opacity()
if op < 241:
    op = op+15
else:
    op = 255
node.setOpacity(op)


doc.refreshProjection()