import math
import os
from typing import List, Tuple, Union
from dataclasses import dataclass

import matplotlib.pyplot as plt


_PathLike = Union[str, bytes, os.PathLike]


@dataclass
class City:
    x: int
    y: int

    def distance(self, city: "City") -> float:
        return math.hypot(self.x - city.x, self.y - city.y)
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


def read_cities(file: _PathLike) -> Tuple[int, List[City]]:
    cities: List[City] = []

    with open(file, 'r') as f:
        lines = f.readlines()
        num_cities = int(lines[0])
        for line in lines[1:]:
            x, y = map(float, line.split())
            cities.append(City(x, y))
    
    return num_cities, cities


def distanceGraph(cities: List[City]) -> List[List[float]]:
    return [[x.distance(y) for y in cities] for x in cities]


def path_cost(route: List[City]) -> float:
    return sum([city.distance(route[idx - 1]) for idx, city in enumerate(route)])


def init_plot(cities: List[City], title: str) -> None:
    plt.ion()
    plt.show(block=False)
    fig = plt.figure(0)
    fig.suptitle(title)
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
