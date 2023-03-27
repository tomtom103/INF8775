import argparse
import time
from pathlib import Path
from typing import List

# try:
#     import matplotlib.pyplot as plt
#     plot = True
# except ModuleNotFoundError:
#     plot = False
#     pass

from algorithms.utils import read_cities, City
from algorithms.algorithms import greedy, dynamic, mst

# def _init_plot(cities: List[City], title: str) -> None:
#     plt.ion()
#     fig = plt.figure(0)
#     fig.suptitle(title)
#     x_lst, y_lst = [], []
#     for city in cities:
#         x_lst.append(city.x)
#         y_lst.append(city.y)
#     x_lst.append(cities[0].x)
#     y_lst.append(cities[0].y)

#     plt.plot(x_lst, y_lst, 'ro')
#     plt.show(block=False)

# def _plot_interactive(route: List[City], block: bool = False):
#     x1, y1, x2, y2 = route[-2].x, route[-2].y, route[-1].x, route[-1].y
#     plt.plot([x1, x2], [y1, y2], 'ro')
#     plt.plot([x1, x2], [y1, y2], 'g')
#     plt.draw()
#     plt.pause(0.05)
#     plt.show(block=block)

def _print_route(cities: List[City], route: List[City]):
    route.append(route[0])
    for city in route:
        print(cities.index(city))
    route.pop(-1)

# def plot_route(route: List[City]) -> None:
#     # Close the graph inside the animation
#     route.append(route[0])
#     for i in range(2, len(route)):
#         _plot_interactive(route[:i], block=False)
#     route.pop(-1)

if __name__ == "__main__":
    
    algorithms = {
        'glouton': greedy,
        'progdyn': dynamic,
        'approx': mst
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
    parser.add_argument("-c", action="store_true",
                        help="Affiche le cout")
    # parser.add_argument("-plot", action="store_true",
    #                     help="Afficher un plot dynamique du chemin emprunte")
    args = parser.parse_args()

    # Load file
    algorithm = args.a

    if algorithm not in algorithms:
        print(f"Algorithme inconnue, les algorithmes sont: {set(algorithms.keys())}")
        exit(1)

    num, cities = read_cities(Path(args.e))

    func = algorithms[algorithm]
    
    start = time.perf_counter_ns()

    route, cost = func(cities)

    duration = time.perf_counter_ns() - start

    # if bool(args.plot):
    #     if plot:
    #         _init_plot(cities, algorithm)
    #         plot_route(route)
    #         plt.show(block=True)
    #     else:
    #         print("Cannot plot the route, matplotlib is not installed...")
    
    if bool(args.t):
        print(duration / (10 ** 6))

    if bool(args.c):
        print(cost)

    if bool(args.p):
        _print_route(cities, route)
    else:
        print(len(route))
