#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Dieses Modul enthält das eigentliche Template für Qt Tools.

.. note::

       BLA BLA

"""

import argparse
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from mainWindow import MainWindow

def main():
    """Die Main Funktion
    """

    parser = argparse.ArgumentParser(description='Qt Tool Template.')


    # optional arguments:
    parser.add_argument(
        "-v", 
        "--verbose", 
        help="increase output verbosity",
        action="store_true"
    )

    args = parser.parse_args()
    print(args)
    app = QApplication(sys.argv)

    w = MainWindow()
    #w.resize(250, 150)
    #w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    app.exec_()
	

if __name__ == "__main__":
    main() 