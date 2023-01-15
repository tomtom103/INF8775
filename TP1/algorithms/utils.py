import os
from typing import List, Union

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
