#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Dieses Modul enthält das eigentliche Template für Qt Tools.

.. note::

       BLA BLA

"""

import argparse
import sys
import time

#print(sys.path)
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from autocomment.mainwindow import MainWindow
from pycpp.lexer import Lexer
from pycpp.blockfactory import BlockFactory
from pycpp.blockcombine import BlockCombine
from pycpp.code import TokenNewLine

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
    start = time.time()
    lexer = Lexer()
    lexer.input(code)
    output = list(lexer.tokens())

    cb_factory = BlockFactory()
    output2 = cb_factory.tree(output)

    doxy_factory = BlockFactory(begin_token_type='DOXYGENCOMMENT', end_token_type='NL')
    output3 = doxy_factory.tree(output2)

    doxy_combine = BlockCombine(begin_token_type='DOXYGENCOMMENT', end_token_type='NL')
    output4 = doxy_combine.tree(output3)

    comment_factory = BlockFactory(begin_token_type='COMMENT', end_token_type='NL')
    output5 = comment_factory.tree(output4)

    comment_combine = BlockCombine(begin_token_type='COMMENT', end_token_type='NL')
    output6 = comment_combine.tree(output5)

    end = time.time()

    print("Elapsed Time "+str(end - start)+" seconds")
    with open("output", "w") as write_file:
        for t in output6:
            write_file.write(str(t))
            if isinstance(t,TokenNewLine):
                write_file.write('\n')
            
    #w = MainWindow(data)
    #w.setWindowTitle('Simple')
    #w.show()
    
    #app.exec_()
	

if __name__ == "__main__":
    main() 