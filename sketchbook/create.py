import krita
import os
import PyQt5.QtWidgets as QtWidgets
import shutil
from . import next_page

A4_WIDTH = 2480
A4_HEIGHT = 3508

def _create_sketchbook(sketchbook_path: str, template_path: str, page_prefix: str):
    app = krita.Krita.instance()

    # create sketchbook directory
    sketchbook_path = sketchbook_path + page_prefix + "sketchbook/"
    os.makedirs(sketchbook_path)

    # copy template to directory
    if template_path:
        template_copy_path = os.path.join(sketchbook_path, page_prefix + "template.kra")
        shutil.copy(template_path, template_copy_path)

    # create last.kra file
    last_path = sketchbook_path + page_prefix + "last.kra"
    if os.path.exists(template_path):
        next_page._create_new_page_from_template(template_path, last_path)
    else:
        next_page._create_new_page(A4_WIDTH, A4_HEIGHT, last_path)

def _path_input_layout(search_dir = False):
    layout = QtWidgets.QHBoxLayout()
    path_input = QtWidgets.QLineEdit()
    path_button = QtWidgets.QPushButton("Browse")
    layout.addWidget(path_input)
    layout.addWidget(path_button)
    if search_dir:
        path_button.clicked.connect(lambda: path_input.setText(QtWidgets.QFileDialog.getExistingDirectory() + "/"))
    else:
        path_button.clicked.connect(lambda: path_input.setText(QtWidgets.QFileDialog.getOpenFileName()[0]))
    return layout, path_input

def show_dialog():
    # opens new window with 2 file inputs, 1 text input and 2 buttons
    main_window: QtWidgets.QMainWindow = krita.Krita.instance().activeWindow().qwindow()

    dialog = QtWidgets.QDialog(main_window)
    dialog.resize(600, 0)
    dialog.setWindowTitle("Open new sketchbook")

    layout = QtWidgets.QVBoxLayout(dialog)

    form = QtWidgets.QFormLayout()
    layout.addLayout(form)

    l1, sketchbook_path_input = _path_input_layout(search_dir=True)
    label1 = QtWidgets.QLabel("Sketchbook path")
    label1.setToolTip("Path where the sketchbook folder will be created")
    form.addRow(label1, l1)

    l2, template_path_input = _path_input_layout()
    label2 = QtWidgets.QLabel("Template (krita file)")
    label2.setToolTip("Optional template file to use for new page creation")
    form.addRow(label2, l2)

    page_prefix_input = QtWidgets.QLineEdit()
    label3 = QtWidgets.QLabel("Page prefix")
    label3.setToolTip("Optional prefix for all sketchbook related files (adds _ to the end if not present)")
    form.addRow(label3, page_prefix_input)

    # buttons
    buttons_layout = QtWidgets.QHBoxLayout()
    layout.addLayout(buttons_layout)

    cancel_button = QtWidgets.QPushButton("Cancel")
    cancel_button.clicked.connect(dialog.reject)
    buttons_layout.addWidget(cancel_button)

    def check_inputs():
        if not sketchbook_path_input.text() or not os.path.isdir(sketchbook_path_input.text()):
            QtWidgets.QMessageBox.warning(dialog, "Invalid sketchbook path", "Invalid sketchbook path")
            return
        if template_path_input.text():
            if not os.path.isfile(template_path_input.text()):
                QtWidgets.QMessageBox.warning(dialog, "Invalid template", "Invalid template")
                return
            if not template_path_input.text().endswith(".kra"):
                QtWidgets.QMessageBox.warning(dialog, "Invalid template", "Template must be a .kra file")
                return

        if page_prefix_input.text() and not page_prefix_input.text().endswith("_"):
            page_prefix_input.setText(page_prefix_input.text() + "_")

        if os.path.exists(sketchbook_path_input.text() + page_prefix_input.text() + "sketchbook"):
            QtWidgets.QMessageBox.warning(dialog, "Sketchbook already exists", "Sketchbook already exists")
            return
    
        dialog.accept()
    open_sketchbook_button = QtWidgets.QPushButton("Create")
    open_sketchbook_button.clicked.connect(check_inputs)
    buttons_layout.addWidget(open_sketchbook_button)

    dialog.accepted.connect(lambda: _create_sketchbook(sketchbook_path_input.text(), template_path_input.text(), page_prefix_input.text()))
    dialog.show()

    

