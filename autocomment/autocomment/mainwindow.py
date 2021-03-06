""" Dieses Modul definiert die Klasse MainWindow. 
"""

from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from autocomment.ui.ui_mainwindow import Ui_MainWindow
from PyQt5.QtCore import Qt
from autocomment.dialog import Dialog

class MainWindow(QMainWindow, Ui_MainWindow):
    """ Die Klasse MainWindow ist eine Ableitung aus den Klasse QMainWindow sowie Ui_MainWindow. 
        
        Die erstere ist die Qt Standard Klasse für ein Hauptfenster. Die zweite kommt
        aus dem Qt Code Generator. Das Benutzerinterface welches durch diese Klasse aufgebaut wird
        kann durch das Tool Designer, welches Teil von Qt5 ist, erstellt werden.
    

    """


    def __init__(self, methods):
        super().__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        model = QStandardItemModel(self.listView)
        self.listView.setModel(model)
        self.listView.doubleClicked.connect(self.doubleClicked)
        self.methods = methods
        for idx, method in enumerate(methods):
            label = ""
            label += method.name

            qitem = QStandardItem(label)
            qitem.setCheckable(False)
            qitem.setEditable(False)
    
            # Add the item to the model
            model.appendRow(qitem)

            # Ändere die Hintergrundfarbe jedes zweiten Items um diese besser zu unterscheiden
            glitter = QColor("#E6E8FA")
            if idx % 2 == 0:
                model.setData(model.index(idx, 0), QBrush(glitter), Qt.BackgroundRole)

            # Setze die Schriftfarbe jedes items auf rot welches das mark Attribut aufweist.
            #if "mark" in method and method["mark"]:
            #        model.setData(model.index(idx, 0), QBrush(Qt.red), Qt.ForegroundRole)

    
        # Connect up the buttons.
        self.exitButton.clicked.connect(self.close)

    def doubleClicked(self, index):
        row = index.row()
        method = self.methods[row]
        dialog = Dialog(method)
        dialog.setWindowTitle("Dialog")
        out = dialog.exec()
