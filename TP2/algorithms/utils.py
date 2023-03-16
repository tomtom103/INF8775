import math
import os
from typing import List, Tuple, Union
from dataclasses import dataclass

_PathLike = Union[str, bytes, os.PathLike]


@dataclass(frozen=True, eq=True)
class City:
    x: int
    y: int

    def distance(self, city: "City") -> float:
        return math.hypot(city.x - self.x, city.y - self.y)
    
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
