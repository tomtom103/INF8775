from .utils import MatrixT, add, sub, multiply, alloc_square_matrix

LEAF_SIZE: int = 64

def strassen_multiply(A: MatrixT, B: MatrixT) -> MatrixT:
    """
    Basé sur l'algorithme décrite sur:
    https://en.wikipedia.org/wiki/Strassen_algorithm 
    """
    n = len(A) # common

    if n <= LEAF_SIZE:
        return multiply(A, B)

    div_size = n // 2 # floor division

    a11 = alloc_square_matrix(div_size)
    a12 = alloc_square_matrix(div_size)
    a21 = alloc_square_matrix(div_size)
    a22 = alloc_square_matrix(div_size)

    b11 = alloc_square_matrix(div_size)
    b12 = alloc_square_matrix(div_size)
    b21 = alloc_square_matrix(div_size)
    b22 = alloc_square_matrix(div_size)

    for i in range(div_size):
        for j in range(div_size):
            a11[i][j] = A[i][j] # top left
            a12[i][j] = A[i][j+div_size] # top right
            a21[i][j] = A[i+div_size][j] # bottom left
            a22[i][j] = A[i+div_size][j+div_size] # bottom right

            b11[i][j] = B[i][j] # top left
            b12[i][j] = B[i][j+div_size] # top right
            b21[i][j] = B[i+div_size][j] # bottom left
            b22[i][j] = B[i+div_size][j+div_size] # bottom right

    m1 = strassen_multiply(add(a11, a22), add(b11, b22)) # (a11 + a22) * (b11 + b22)
    m2 = strassen_multiply(add(a21, a22), b11) # (a21 + a22) * b11
    m3 = strassen_multiply(a11, sub(b12, b22)) # a11 * (b12 - b22)
    m4 = strassen_multiply(a22, sub(b21, b11)) # a22 * (b21 - b11)

    m5 = strassen_multiply(add(a11, a12), b22) # (a11 + a12) * b22
    m6 = strassen_multiply(sub(a21, a11), add(b11, b12)) # (a21 + a11) * (b11 + b12)
    m7 = strassen_multiply(sub(a12, a22), add(b21, b22)) # (a12 + a22) * (b21 + b22)

    c12 = add(m3, m5) # m3 + m5
    c21 = add(m2, m4) # m2 + m4
    c11 = sub(add(m1, m4), add(m5, m7)) # m1 + m4 - m5 + m7
    c22 = sub(add(add(m1, m3), m6), m2) # m1 + m3 + m6 - m2
    
    C = alloc_square_matrix(n)

    for i in range(0, div_size):
        for j in range(0, div_size):
            C[i][j] = c11[i][j]
            C[i][j + div_size] = c12[i][j]
            C[i + div_size][j] = c21[i][j]
            C[i + div_size][j + div_size] = c22[i][j]
    return C
