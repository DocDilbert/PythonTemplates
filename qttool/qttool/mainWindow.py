""" Dieses Modul definiert die Klasse MainWindow. 
"""

from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush
from ui.ui_mainwindow import Ui_MainWindow
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow, Ui_MainWindow):
    """ Die Klasse MainWindow ist eine Ableitung aus den Klasse QMainWindow sowie Ui_MainWindow. 
        
        Die erstere ist die Qt Standard Klasse für ein Hauptfenster. Die zweite kommt
        aus dem Qt Code Generator. Das Benutzerinterface welches durch diese Klasse aufgebaut wird
        kann durch das Tool Designer, welches Teil von Qt5 ist, erstellt werden.
    

    """


    def __init__(self, data):
        super(QMainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        model = QStandardItemModel(self.listView)
        self.listView.setModel(model)

        for idx, item in enumerate(data):
            qitem = QStandardItem(item["name"])
            qitem.setCheckable(False)
            qitem.setEditable(False)
    
            # Add the item to the model
            model.appendRow(qitem)

            if "red" in item:
                if item["red"] == True:
                    model.setData(model.index(idx, 0), QBrush(Qt.red), Qt.BackgroundRole)
    
        # Connect up the buttons.
        self.exitButton.clicked.connect(self.close)
