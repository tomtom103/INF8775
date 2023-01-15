import argparse

from algorithms.utils import parse_matrix
from algorithms.classic import classic_multiply

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-A", required=True, type=str,
                        help="File pointing to the first matrix")
    parser.add_argument("-B", required=True, type=str,
                        help="File pointing to the second matrix")

    args = parser.parse_args()

    A = parse_matrix(args.A)
    B = parse_matrix(args.B)

    result = classic_multiply(A, B)
    print(result)