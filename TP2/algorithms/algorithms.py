import itertools
from typing import List, Tuple

import matplotlib.pyplot as plt

from .utils import City, path_cost, distanceGraph

def _init_plot(cities: List[City]) -> None:
    fig = plt.figure(0)
    fig.suptitle("Greedy algorithm")
    x_lst, y_lst = [], []
    for city in cities:
        x_lst.append(city.x)
        y_lst.append(city.y)
    x_lst.append(cities[0].x)
    y_lst.append(cities[0].y)

    plt.plot(x_lst, y_lst, 'ro')
    plt.show(block=False)

def plot_interactive(route: List[City], block: bool = False):
    x1, y1, x2, y2 = route[-2].x, route[-2].y, route[-1].x, route[-1].y
    plt.plot([x1, x2], [y1, y2], 'ro')
    plt.plot([x1, x2], [y1, y2], 'g')
    plt.draw()
    plt.pause(0.07)
    plt.show(block=block)
    

def greedy(cities: List[City], plot: bool = False):
    unvisited = cities[1:]
    route = [cities[0]]

    if plot:
        plt.ion()
        plt.show(block=False)
        _init_plot([*route, *unvisited])

    while len(unvisited):
        index, city = min(
            enumerate(unvisited),
            key=lambda x: x[1].distance(route[-1])
        )
        route.append(city)
        del unvisited[index]
        if plot:
            plot_interactive(route, block=False)

    # This is only done to close the graph
    if plot:
        route.append(route[0])
        plot_interactive(route, block=False)
        route.pop()

    return route, path_cost(route)
