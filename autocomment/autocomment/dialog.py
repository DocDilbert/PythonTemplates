

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
        sub_dialog.setWindowTitle("Sub Dialog")
 
        code = ""
        if len(method['args'])>0:
            code = "/// Arguments:\n"
            for arg in method['args']:
                code+='///     %s\n' % (arg['name'].val)
            code += "///\n"
        code += "/// Returns:\n"
        code += '///     [%s]\n' % (method['returns'].val)
        self.textEdit.setText(code)