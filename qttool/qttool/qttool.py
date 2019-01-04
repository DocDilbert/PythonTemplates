#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Dieses Modul enthält das eigentliche Template für Qt Tools.

.. note::

       BLA BLA

"""

import argparse

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
    print("main() finished")

if __name__ == "__main__":
    main() 