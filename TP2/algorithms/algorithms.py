from typing import List

from .utils import City, path_cost, init_plot, plot_interactive
    

def greedy(cities: List[City], plot: bool = False):
    unvisited = cities[1:]
    route = [cities[0]]

    if plot:
        init_plot([*route, *unvisited], "Greedy Algorithm")

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
