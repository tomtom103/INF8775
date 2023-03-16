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


from typing import Tuple 
import math

def mst(cities: List[City]) -> Tuple[List[City], float]:

    arr, cost = greedy(cities)
    graph = array_to_tree(arr)
    preorder = preorder_traversal(graph)

    # for i, val in enumerate(arr):
    #     if a[i] != val:
    #         print(f"Greedy value: {val}, preorder value: {a[i]}")


    return preorder, path_cost(preorder)
    

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def array_to_tree(arr):
    if not arr:
        return None
    mid = len(arr) // 2
    node = Node(arr[mid])
    node.left = array_to_tree(arr[:mid])
    node.right = array_to_tree(arr[mid+1:])
    return node

def preorder_traversal(root: Node):
    if not root:
        return []

    stack = [root]
    result = []

    while stack:
        node = stack.pop()
        result.append(node.data)

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result







