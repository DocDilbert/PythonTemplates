"""
Dieses Skript erzeugt binär Dateien beliebiger Länge. Die Datei
wird mit zufälligen Daten gefüllt. 
"""

import argparse
import random

def generate_random_byte_array(seed, size):
    """Diese Methode generiert ein byte array welches mit pseudo zufälligen Daten gefüllt wird.
    
    Arguments:
        seed -- Der seed mit dem der Zufallsgenerator initialisiert wird.
        size -- Die Größe des zu generiernden byte arrays.
    """

    random.seed(seed)
    content = bytearray([random.randint(0, 255) for _ in range(0, size)])
    return content

def create_random_file(seed, size, filename):
    """Diese Funktion erzeugt eine pseudo zufällige Binärdatei
    
    Arguments:
        seed -- Der seed mit dem der Zufallsgenerator initialisiert wird.
        size -- Die Größe der zu generierenden Datei.
        filename -- Der Name der zu generierenden Datei.
    """

    with open(filename,"wb") as file:
        file.write(generate_random_byte_array(seed, size))


def main():
    """
    Die Main Funktion des Skriptes.
    """

    parser = argparse.ArgumentParser(description='Random binary file generator.')

    # Dateigröße als Argument
    parser.add_argument(
        'seed', 
        metavar='seed', 
        type=int, 
        help='The random seed used for file generation.'
    )

    # Dateigröße als Argument
    parser.add_argument(
        'size', 
        metavar='size', 
        type=int, 
        help='The size in bytes of the random binary file.'
    )

    # Dateiname als Argument
    parser.add_argument(
        'filename', 
        metavar='filename', 
        type=str, 
        help='The name of the random binary file.'
    )

    args = parser.parse_args()
    print("Creating binary file ...")
    
    create_random_file(args.seed, args.size, args.filename)
    
    print("Done!")

if __name__ == "__main__":
    main() 
