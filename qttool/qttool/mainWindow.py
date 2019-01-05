from PyQt5.QtWidgets import QMainWindow
from ui.ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)


        # Make some local modifications.
        self.listWidget.addItem("TEST");


        # Connect up the buttons.
        #self.okButton.clicked.connect(self.accept)
        self.exitButton.clicked.connect(self.close)
