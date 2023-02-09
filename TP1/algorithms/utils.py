import os
from typing import List, Union, Any
from tabulate import tabulate

MatrixT = List[List[int]]
_PathLike = Union[str, bytes, os.PathLike]

class InvalidMatrixSize(Exception):
    ...


def _is_valid_dimensions(matrix: MatrixT, N: int) -> bool:
    """
    Check whether the final matrix size corresponds to 
    The first provided N value (matrix must be 2 ** N x 2 ** N)
    """
    return (
        all(len(row) == 2 ** N for row in matrix)
        and len(matrix) == 2 ** N 
    )


def alloc_square_matrix(size: int) -> MatrixT:
    return [[0 for _ in range(size)] for _ in range(size)]


def parse_matrix(file_path: _PathLike) -> MatrixT:
    result = []
    with open(file_path, "r") as f:
        N = int(f.readline().strip())
        for line in f.readlines():
            result.append(list(map(int, line.replace('\n', '').split(' '))))
    
    # Verification
    if not _is_valid_dimensions(result, N):
        raise InvalidMatrixSize("Final matrix size does not match the one specified in the file")

    return result


def multiply(A: MatrixT, B: MatrixT) -> MatrixT:
    """
    Simple matrix multiplication
    """
    C = [[0 for _ in range(len(A))] for _ in range(len(A))] # Memory allocation
    for i in range(len(A)):
        for j in range(len(A)):
            for k in range(len(A)):
                C[i][j] += A[i][k] * B[k][j]
    return C


def add(A: MatrixT, B: MatrixT) -> MatrixT:
    """
    Simple matrix addition
    """
    C = [[0 for _ in range(len(A))] for _ in range(len(A))] # Memory allocation
    for i in range(len(A)):
        for j in range(len(A)):
            C[i][j] = A[i][j] + B[i][j]
    return C


def sub(A: MatrixT, B: MatrixT) -> MatrixT:
    """
    Simple matrix substraction
    """
    C = [[0 for _ in range(len(A))] for _ in range(len(A))] # Memory allocation
    for i in range(len(A)):
        for j in range(len(A)):
            C[i][j] = A[i][j] - B[i][j]
    return C

def print_results(table: List[List[Any]], headers: List[str]) -> None:
    print(tabulate(table, headers=headers))