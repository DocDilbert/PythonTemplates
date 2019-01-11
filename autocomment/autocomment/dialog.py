

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from autocomment.ui.ui_dialog import Ui_Dialog
import pprint
class Dialog(QDialog, Ui_Dialog):
    
    def __init__(self, method):
        super().__init__()

         # Set up the user interface from Designer.
        self.setupUi(self)
        sub_dialog = QDialog()
        sub_dialog.setWindowTitle("Suggested Comment")
 
        code = ""
        if len(method.arguments)>0:
            code = "/// Arguments:\n"
            for arg in method.arguments:

                code+='///     %s\n' % (arg.name)
            code += "///\n"
        code += "/// Returns:\n"
        code += '///     [%s]\n' % (method.returns)
        self.textEdit.setText(code)