import numpy as np

LEAF_SIZE = 8

def strassen_multiply(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    if A.size <= LEAF_SIZE or B.size <= LEAF_SIZE:
        return A @ B
    
    n = A.shape[0]

    m  = n // 2

    # Split matrix A
    a = A[: m, : m]
    b = A[: m, m :]
    c = A[m :, : m]
    d = A[m :, m :]

    # Split matrix y
    e = B[: m, : m]
    f = B[: m, m :]
    g = B[m :, : m]
    h = B[m :, m :]

    m1 = strassen_multiply(a, f - h)
    m2 = strassen_multiply(a + b, h)
    m3 = strassen_multiply(c + d, e)
    m4 = strassen_multiply(d, g - e)
    m5 = strassen_multiply(a + d, e + h)
    m6 = strassen_multiply(b - d, g + h)
    m7 = strassen_multiply(a - c, e + f)

    result = np.zeros((2 * m, 2 * m), dtype=np.int32)

    result[: m, : m] = m5 + m4 - m2 + m6
    result[: m, m :] = m1 + m2
    result[m :, : m] = m3 + m4
    result[m :, m :] = m1 + m5 - m3 - m7

    return result[: n, : n]
