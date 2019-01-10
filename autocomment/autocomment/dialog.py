

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from autocomment.ui.ui_dialog import Ui_Dialog
import pprint
class Dialog(QDialog, Ui_Dialog):
    
    def __init__(self, method):
        super(Dialog, self).__init__()

         # Set up the user interface from Designer.
        self.setupUi(self)
        sub_dialog = QDialog()
        sub_dialog.setWindowTitle("Sub Dialog")
 

        pp = pprint.PrettyPrinter(indent=4)
        self.textEdit.setText(pp.pformat(method))