from krita import *

app = Krita.instance()
doc = app.activeDocument()

# get the current selected layer, called a 'node'
node = doc.activeNode()
if node.animated():
    for i in range(doc.animationLength()):
        if node.hasKeyframeAtTime(2*i):
            doc.setCurrentTime(2*i)
            doc.refreshProjection()
            app.action('insert_keyframe_right').trigger()
doc.refreshProjection()
