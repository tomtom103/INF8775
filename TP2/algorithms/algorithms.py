import functools
from typing import List, Tuple, Dict

from .utils import (
    City, 
    path_cost, 
    distanceGraph,
)
    

def greedy(cities: List[City]):
    unvisited = set(cities[1:]) # O(n - 1)
    route = [cities[0]] # O(1)

    while unvisited: # O(n)
        city = min(
            unvisited,
            key=lambda x: x.distance(route[-1])
        )
        route.append(city) # O(1)
        unvisited.remove(city) # O(1) since it's a set

    return route, path_cost(route) # O(n)
 

def dynamic(cities: List[City]) -> Tuple[List[City], float]:
    """
    Function has n possible start vertices and 2 ^ n possible subgraphs.
    
    Function will be called on at most n * 2 ^ n distinct arguments

    Each call performs at most O(n) work

    Total work: O(n ^ 2 * 2 ^ n)
    """
    distance_matrix = distanceGraph(cities) # Not counted in complexity

    N = frozenset(range(1, len(distance_matrix))) # O(n)
    memo: Dict[Tuple, int] = {}

    @functools.lru_cache(maxsize=1024)
    def distance(ni: int, N: frozenset) -> float:
        if not N:
            return distance_matrix[ni][0] # O(1)
        
        costs = [
            (nj, distance_matrix[ni][nj] + distance(nj, N.difference({nj}))) for nj in N
        ]
        nmin, min_cost = min(costs, key=lambda x: x[1])
        memo[(ni, N)] = nmin

        return min_cost
    
    best_distance = distance(0, N)

    # Get path with the minimum distance
    ni = 0
    route = [cities[0]]

    while N:
        ni = memo[(ni, N)]
        route.append(cities[ni])
        N = N.difference({ni})
    return route, best_distance

    