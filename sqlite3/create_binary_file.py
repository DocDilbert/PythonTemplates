"""Dieses Skript erzeugt binär Dateien beliebiger Länge. Die Datei
wird gefüllt mit fortlaufenden Bytes von 0 bis 255.
"""

import argparse

def main():
    """Die Main Funktion des Skriptes.
    """

    parser = argparse.ArgumentParser(description='Random binary file generator.')

    # Dateigröße als Argument
    parser.add_argument(
        'filesize', 
        metavar='filesize', 
        type=int, 
        help='The size in bytes of the binary file.'
    )

    # Dateiname als Argument
    parser.add_argument(
        'filename', 
        metavar='filename', 
        type=str, 
        help='The name of the binary file.'
    )

    args = parser.parse_args()
    print("Creating binary file ...")
    with open(args.filename,"wb") as file:
        one_byte = bytearray(1)
        for i in range(0,args.filesize):
            one_byte[0] = i % 256
            file.write(one_byte)

    print("Done!")

if __name__ == "__main__":
    main() 
