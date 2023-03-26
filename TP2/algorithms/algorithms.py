import sys
import functools
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field

from .utils import (
    City, 
    path_cost, 
    distanceGraph,
)
    

def greedy(cities: List[City]):
    unvisited = set(cities[1:]) # O(n - 1)
    route = [cities[0]] # O(1)

    while unvisited: # O(n)
        # min prend O(n)
        city = min(
            unvisited,
            key=lambda x: x.distance(route[-1]) # O(1)
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

    @functools.lru_cache(maxsize=None)
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


@dataclass(eq=False, frozen=True)
class Node:
    data: Any
    children: List["Node"] = field(default_factory=lambda: list())


def preorder_traversal(root: Node) -> List[int]:
    if not root:
        return []
    
    # Add root node to traversal array
    traversal = [root.data]
    
    # Traverse all child nodes recursively
    for child in root.children:
        traversal += preorder_traversal(child)
    
    return traversal


def mst(cities : List[City]) -> Tuple[List[City], float]:
    distance_matrix = distanceGraph(cities)

    traversal = preorder_traversal(prim(distance_matrix))

    path = [cities[i] for i in traversal]
    return path, path_cost(path)


def prim(G: List[List[float]]) -> Node:
    # Accept an arbitrary N by N matrix
    N = len(G)

    selected_node = [False] * N
    tree = []

    selected_node[0] = True

    while len(tree) < N - 1:
        minimum = sys.maxsize
        a, b = 0, 0
        for m in range(N):
            if selected_node[m]:
                for n in range(N):
                    if not selected_node[n] and G[m][n]:  
                        # not in selected and there is an edge
                        if minimum > G[m][n]:
                            minimum = G[m][n]
                            a = m
                            b = n
        selected_node[b] = True
        tree.append((a, b))

    # Create a dictionary to store nodes with their data as key
    nodes_dict: Dict[Any, Node] = {}
    
    edges = tree
    # Create all the nodes without their children
    for edge in edges:
        parent_data, child_data = edge
        if parent_data not in nodes_dict:
            parent_node = Node(parent_data)
            nodes_dict[parent_data] = parent_node
        else:
            parent_node = nodes_dict[parent_data]
        
        if child_data not in nodes_dict:
            child_node = Node(child_data)
            nodes_dict[child_data] = child_node
        else:
            child_node = nodes_dict[child_data]
            
        # Add child node to parent's child nodes
        parent_node.children.append(child_node)
    
    # Return the root node
    return nodes_dict[edges[0][0]]
