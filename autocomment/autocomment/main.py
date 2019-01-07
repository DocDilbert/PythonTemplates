#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Dieses Modul enthält das eigentliche Template für Qt Tools.

.. note::

       BLA BLA

"""

import argparse
import sys

#print(sys.path)
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from autocomment.mainwindow import MainWindow
from pycpp.lexer import Lexer
from pycpp.closurefinder import ClosureFinder


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

    code = ""

    with open("LibRteDriver.h", "r") as read_file:
        code = read_file.read()

    lexer = Lexer()
    lexer.input(code)
    output = list(lexer.tokens())

    closurefinder = ClosureFinder()
    closurefinder.input(output)

    output2 = closurefinder.tree()
    with open("output", "w") as write_file:
        for t in output2:
            write_file.write(str(t))
            write_file.write('\n')
            
    #w = MainWindow(data)
    #w.setWindowTitle('Simple')
    #w.show()
    
    #app.exec_()
	

if __name__ == "__main__":
    main() 