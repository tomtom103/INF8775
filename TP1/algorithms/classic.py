from .utils import MatrixT

def classic_multiply(A: MatrixT, B: MatrixT) -> MatrixT:
    result = [[] for _ in range(len(A))] # Memory allocation
    for i in range(len(A)):
        for j in range(len(A)):
            _sum = 0
            for k in range(len(A)):
                _sum += A[i][k] * B[k][j]
            result[i].append(_sum)

    return result
