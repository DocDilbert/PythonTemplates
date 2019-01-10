

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton

class Dialog(QDialog):
    
    def __init__(self):
        super(QDialog, self).__init__()
        subDialog = QDialog()
        subDialog.setWindowTitle("Sub Dialog")
        #button = QPushButton("Push to open new dialog", this)
        #connect(button, SIGNAL(clicked()), subDialog, SLOT(show()))
    