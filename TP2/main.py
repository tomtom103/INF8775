import argparse
import time

from pathlib import Path

import matplotlib.pyplot as plt

from algorithms.utils import read_cities
from algorithms.algorithms import greedy

if __name__ == "__main__":
    
    algorithms = {
        'glouton': greedy,
        'progdyn': ...,
        'approx': ...,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", required=True, type=str,
                        help=f"Algorithme à utiliser: {set(algorithms.keys())}")
    parser.add_argument("-e", required=True, type=str,
                        help="Chemin vers l'exemplaire")
    parser.add_argument("-p", action="store_true",
                        help="Affiche les indices des villes a visiter en commencant par 0 et finissant par 0")
    parser.add_argument("-t", action="store_true",
                        help="Affiche le temps d'execution en millisecondes")
    parser.add_argument("-plot", action="store_true",
                        help="Afficher un plot dynamique du chemain emprunte")
    args = parser.parse_args()

    # Load file
    algorithm = args.a

    if algorithm not in algorithms:
        print(f"Algorithme inconnue, les algorithmes sont: {set(algorithms.keys())}")
        exit(1)

    num, cities = read_cities(Path(args.e))

    start = time.perf_counter_ns()

    route, cost = algorithms[algorithm](cities, plot=bool(args.plot))

    duration = time.perf_counter_ns() - start

    if bool(args.plot):
        plt.show(block=True)
    elif bool(args.t):
        print(int(duration / 1000))

    if bool(args.p):
        # TODO
        ...
        print(cost)
        print(route)
