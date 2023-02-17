import time
import argparse
from pathlib import Path

from algorithms.utils import parse_matrix, multiply
from algorithms.strassen import strassen_multiply
from algorithms.strassen_leaf import strassen_multiply as strassen_multiply_leaf

if __name__ == "__main__":

    algorithms = {
        "conv": multiply,
        "strassen": strassen_multiply,
        "strassenSeuil": strassen_multiply_leaf
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", required=True, type=str,
                        help="Algorithme à utiliser: \{conv, strassen, strassenSeuil\}")
    parser.add_argument("-e1", required=True, type=str,
                        help="Chemin vers la première matrice")
    parser.add_argument("-e2", required=True, type=str,
                        help="Chemin vers la deuxième matrice")
    parser.add_argument("-p", action="store_true",
                        help="Affiche la matrice résultat contenant uniquement les valeurs")
    parser.add_argument("-t", action="store_true",
                        help="Affiche le temps d'exécution en millisecondes")
    args = parser.parse_args()

    algorithm = args.a
    if algorithm not in algorithms:
        print(f"Algorithme inconnue, les algorithmes sont: {set(algorithms.keys())}")
        exit(1)

    display_matrix, display_time = bool(args.p), bool(args.t)

    A, B = parse_matrix(Path(args.e1)), parse_matrix(Path(args.e2))

    start = time.perf_counter_ns()
    result = algorithms[args.a](A, B)
    duration = time.perf_counter_ns() - start

    if display_matrix:
        print('\n'.join([' '.join([str(val) for val in row]) for row in result]))

    if display_time:
        print(duration / 1000)
