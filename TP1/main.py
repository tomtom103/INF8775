import timeit

from tqdm import tqdm
from algorithms.utils import parse_matrix, multiply, print_results
from algorithms.strassen import strassen_multiply
from algorithms.strassen_leaf import strassen_multiply as strassen_multiply_leaf

if __name__ == "__main__":

    headers = ["Algorithm", "Matrix Size", "Leaf Size", "Execution Time", "Complexity"]
    results = [headers]

    for i in tqdm(range(4, 11)):
        if i >= 9:
            num_exec = 1
        else:
            num_exec = 5

        A = parse_matrix(f"data/ex{i}_0")
        B = parse_matrix(f"data/ex{i}_1")

        multiply_t = timeit.timeit('multiply(A, B)', globals=globals(), number=num_exec) / num_exec
        strassen_t = timeit.timeit('strassen_multiply(A, B)', globals=globals(), number=num_exec) / num_exec
        strassen_leaf_t = timeit.timeit('strassen_multiply_leaf(A, B, 64)', globals=globals(), number=num_exec) / num_exec

        results.extend([
            ['Classic', i, 0, multiply_t, "n^3"],
            ['Strassen', i, 0, strassen_t, "n^3"],
            ['Strassen with Leaf', i, 64, strassen_leaf_t, "n^3"],
        ])

        # seuils = [2 ** i for i in range(4, 11)]

        # for seuil in tqdm(seuils):
        #     strassen_leaf_t = timeit.timeit(f'strassen_multiply_leaf(A, B, {seuil})', globals=globals(), number=num_exec)

        #     results.extend([
        #         ['Strassen with Leaf', i, seuil, strassen_leaf_t, "n^3"],
        #     ])

    print_results(results[1:], headers)
