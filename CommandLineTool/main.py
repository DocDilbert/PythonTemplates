import argparse

def main():
    print("HELLO WORLD")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Command line tool template.')

    # positional arguments:
    parser.add_argument(
        'integers', 
        metavar='N', 
        type=int, 
        nargs='+',
        help='an integer for the accumulator'
    )

    # optional arguments:
    parser.add_argument(
        '--sum', 
        dest='accumulate', 
        action='store_const',
        const=sum, # use built-in function sum
        default=max, # use built-in function max as default
        help='sum the integers (default: find the max)'
    )

    args = parser.parse_args()
    print(args)
    print(args.accumulate(args.integers))
    main() 