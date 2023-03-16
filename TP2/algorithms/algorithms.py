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
    

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insert(node, city, origin):
    if node is None:
        return Node(city)
    if city.distance(origin) < node.data.distance(origin):
        node.left = insert(node.left, city, origin)
    else:
        node.right = insert(node.right, city, origin)
    return node

def prim(cities: List[City]) -> Tuple[List[Tuple[int, int, float]], List[City]]:
    # Initialize the distances matrix
    n = len(cities)
    distances = [[math.inf for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            distance = cities[i].distance(cities[j])
            distances[i][j] = distance
            distances[j][i] = distance
    
    # Initialize the set of unvisited vertices
    unvisited = set(range(n))
    
    # Start with vertex 0
    visited = set([0])
    unvisited.remove(0)
    
    # Initialize the minimum spanning tree
    mst = []
    edge_count = 0
    
    # Loop until all vertices have been visited
    while unvisited:
        # Find the edge with minimum weight
        min_distance = math.inf
        for i in visited:
            for j in unvisited:
                if distances[i][j] < min_distance:
                    min_distance = distances[i][j]
                    u = i
                    v = j
        
        # Add the new edge to the minimum spanning tree
        mst.append((u, v, min_distance))
        edge_count += 1
        
        # Mark the new vertex as visited
        visited.add(v)
        unvisited.remove(v)
    
    # Extract the cities from the minimum spanning tree
    tree_cities = [cities[mst[i][0]] for i in range(len(mst))] + [cities[mst[i][1]] for i in range(len(mst))]
    unique_cities = list(set(tree_cities))
    
    # Compute the path by following the edges in the minimum spanning tree
    path = []
    current_city = unique_cities[0]
    path.append(current_city)
    while len(path) < n:
        for u, v, distance in mst:
            if current_city in (cities[u], cities[v]):
                if cities[u] == current_city:
                    current_city = cities[v]
                else:
                    current_city = cities[u]
                if current_city not in path:
                    path.append(current_city)
    
    return mst, path


def preorder_traversal(node):
    if node is None:
        return []
    result = [node]
    result += preorder_traversal(node.left)
    result += preorder_traversal(node.right)

    cnt = []
    for node in result : 
        cnt.append(node.data)
    
    return result

def mst(cities: List[City]) -> Tuple[List[City], float]:

    arr, cost = greedy(cities)
    mst, path = prim(cities)

    # Build a binary search tree from the unique cities
    root = None
    for city in path:
        if root is None:
            root = Node(city)
        else:
            insert(root, city, path[0])

    preorder_traversal(root)
    print(path_cost(path))
    return path, path_cost(path)