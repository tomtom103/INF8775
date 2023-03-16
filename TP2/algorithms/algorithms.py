import sys
import itertools
from typing import List

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

def dynamic(cities: List[City]):
    distance_matrix = distanceGraph(cities) # Not counted in complexity

    n = len(distance_matrix) # O(1)
    # Set containing all nodes
    set_of_nodes = set(range(n)) # O(n)

    # dict containing all sub-problem solutions
    dp_dict = {(tuple([node]), node): tuple([0, None]) for node in set_of_nodes} # O(n)
    # dict access is worst case O(n) for bad hash algorithm
    # average access is O(1), performed n times

    # queue of subproblems to solve starting with first node
    queue = [((0,), 0)]

    while len(queue) > 0:
        visited, previous_node = queue.pop(0) # O(n) since whole list is shifted by 1

        # Get the previous best distance
        prev_dist, _ = dp_dict[(visited, previous_node)] # O(1) access

        # Create a set of nodes to visit
        to_visit = set_of_nodes.difference(set(visited)) # Difference s - t = O(len(s)) average case

        for node in to_visit:
            # Mark each node in to_visit as visited
            new_visited = tuple(sorted(list(visited) + [node]))

            new_dist = (prev_dist + distance_matrix[previous_node][node])

            if (new_visited, node) not in dp_dict:
                dp_dict[(new_visited, node)] = (new_dist, previous_node)
                queue += [(new_visited, node)]
            
            elif new_dist < dp_dict[(new_visited, node)][0]:
                dp_dict[(new_visited, node)] = (new_dist, previous_node)

    # Solve backward through stored solutions of subproblems
    # Find all prenultimate subproblem and store them in dict
    node_set = tuple(range(n))
    penultimate_path_dict = dict((_visited, previous) for _visited, previous in dp_dict.items() if _visited[0] == node_set)

    path_keys = list(penultimate_path_dict.keys())

    total_dist = [
        penultimate_path_dict[path][0] + distance_matrix[path[1]][0]
        for path in penultimate_path_dict
    ]
    idx, distance = min(enumerate(total_dist), key=lambda x: x[1])

    path_key = path_keys[idx]
    _, penultimate_node = path_key
    _, pre_penultimate_node = dp_dict[path_key]

    final_path = [penultimate_node]
    # Remove penultimate_node from set
    node_set = tuple(sorted(set(node_set).difference({penultimate_node})))

    while pre_penultimate_node is not None:
        penultimate_node = pre_penultimate_node
        path_key = (node_set, penultimate_node)
        _, pre_penultimate_node = dp_dict[path_key]

        final_path += [penultimate_node]
        # Remove node from set of remaining nodes
        node_set = tuple(sorted(set(node_set).difference({penultimate_node})))

    final_path.append(0)

    return [cities[i] for i in final_path], distance  

    

    