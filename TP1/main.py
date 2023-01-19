import argparse
import timeit
import numpy as np

from algorithms.utils import parse_matrix, multiply
from algorithms.strassen import strassen_multiply
from algorithms.strassen_np import strassen_multiply as strassen_multiply_np
from algorithms.strassen_leaf import strassen_multiply as strassen_multiply_leaf
from algorithms.strassen_np_leaf import strassen_multiply as strassen_multiply_np_leaf

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-A", required=True, type=str,
                        help="File pointing to the first matrix")
    parser.add_argument("-B", required=True, type=str,
                        help="File pointing to the second matrix")

    args = parser.parse_args()

    A = parse_matrix(args.A)
    B = parse_matrix(args.B)

    np_A, np_B = np.array(A), np.array(B)

    t = timeit.timeit('multiply(A, B)', globals=globals(), number=1)
    t1 = timeit.timeit('strassen_multiply(A, B)', globals=globals(), number=1)
    t2 = timeit.timeit('strassen_multiply_np(np_A, np_B)', globals=globals(), number=1)
    t3 = timeit.timeit('strassen_multiply_leaf(A, B)', globals=globals(), number=1)
    t4 = timeit.timeit('strassen_multiply_np_leaf(np_A, np_B)', globals=globals(), number=1)

    print("Regular multiply: ", t)
    print("Strassen multiply: ", t1)
    print("Strasseb multiply with np : ", t2)
    print("Strassen multiply with leaf: ", t3)
    print("Strassen multiply with np and leaf: ", t4)
