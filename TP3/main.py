import argparse
import math
import atexit
import time
import signal

from pathlib import Path
from typing import List, Tuple, Iterator, Dict
from dataclasses import dataclass, field

from timeout import timeout

@dataclass
class Enclosure:
    id: int
    size: int
    shape: List[Tuple[int, int]] = field(default_factory=list, hash=False, compare=False) # [(x, y), (x, y)]
    neighbors: List[Tuple["Enclosure", int]] = field(default_factory=list, hash=False, compare=False) # Enclosure + weight to that enclosure

    def distance_to(self, other: "Enclosure") -> int:
        """
        Returns the manhattan distance between the closest points
        of this and another enclosure

        This function runs in O(n log n) instead of O(n^2)
        """
        # Sort the points by x-coordinates
        shape1 = sorted(self.shape, key=lambda point: point[0])
        shape2 = sorted(other.shape, key=lambda point: point[0])

        closest_1 = shape1[0]
        closest_2 = shape2[0]
        min_distance = abs(closest_1[0] - closest_2[0]) + abs(closest_1[1]  - closest_2[1])

        # Iterate through the points in both shapes in parallel
        i, j = 0, 0
        while i < len(shape1) and j < len(shape2):
            distance = abs(shape1[i][0] - shape2[j][0]) + abs(shape1[i][1], shape2[j][1])

            if distance < min_distance:
                closest_1 = shape1[i]
                closest_2 = shape2[j]
                min_distance = distance

            if shape1[i][0] < shape2[j][0]:
                i += 1
            else:
                j += 1

        return min_distance


def pack_enclosures(enclosures: List[Enclosure], bonus_enclosures: List[Enclosure], weights: List[List[int]]) -> Iterator[List[List[int]]]:
    total_area = sum([enclosure.size for enclosure in enclosures])

    # Calculate the width and height of the bounding box
    width = int(math.sqrt(total_area))
    height = int(math.ceil(total_area / width))

    current_score = - math.inf

    while True:
        bbox = [[0 for _ in range(width)] for _ in range(height)]

        estimated_score = 0

        for enclosure in enclosures:
            # TODO: Logic to place an enclosure within the box
            ...

            # assert len(enclosure.shape) == enclosure.size
            for x, y in enclosure.shape:
                bbox[y][x] = enclosure.id

        if estimated_score > current_score:
            yield bbox


# def populate_most_valuable_neighbors(enclosures: List[Enclosure], bonus_enclosures: List[Enclosure], weights: List[List[int]]) -> List[Enclosure]:
#     # TODO: Do shit here

#     for enclosure in enclosures:
#         # TODO: Figure out how to populate the neighbors according to weights and bonus enclosures that need to be together
#         # We could probably want some kind of heuristic here that tells us which enclosures absolutely need to be next to eachother
#         # If we have a score of like 30 vs 300, the 300 one obviously takes priority
#         enclosure.neighbors = []

#     # Return all enclosures with a populated list of neighbors (IMPORTANT)
#     return enclosures

def populate_most_valuable_neighbors(enclosures: List[Enclosure], bonus_enclosures: List[Enclosure], weights: List[List[int]], num_neighbors: int = 3) -> List[Enclosure]:
    
    def get_bonus_attraction(e1: Enclosure, e2: Enclosure, k: int) -> int:
        # Check if both enclosures are in the bonus list
        # If so we get kˆ2 as the bonus, otherwise no bonus
        if e1 in bonus_enclosures and e2 in bonus_enclosures:
            return k**2
        return 0

    for enclosure in enclosures:
        # This is to keep a list of all the possible neighbors 
        neighbor_values = []
        
        for neighbor in enclosures:
            # Skip current enclosure as a neighbor 
            if enclosure == neighbor:
                continue
                
            # Weight between current enclosure and its neighbor
            weight = weights[enclosure.id][neighbor.id] + weights[neighbor.id][enclosure.id]
            
            # Bonus for current enclosure and neighbor
            bonus_attraction = get_bonus_attraction(enclosure, neighbor, k)
            
            # Calculate sum(weight, attraction)
            total_value = weight + bonus_attraction
            
            # Add neighbor and its total value to the neighbor_values list
            neighbor_values.append((neighbor, total_value))

        # Sort the neighbor_values list by the total value in descending order (higher value first)
        neighbor_values.sort(key=lambda x: x[1], reverse=True)

        # Assign the top num_neighbors most valuable neighbors to the current enclosure
        enclosure.neighbors = [neighbor for neighbor, _ in neighbor_values[:num_neighbors]]

    # Return the list of enclosures with their neighbors assigned
    return enclosures



def read_file(file_path: Path, p: bool):
    with open(file_path, 'r') as file:
        n, m, k = map(int, file.readline().split())
        bonus_enclosures = list(map(int, file.readline().split()))
        enclosure_sizes = [int(file.readline()) for _ in range(n)]
        enclosure_weights = [list(map(int, file.readline().split())) for _ in range(n)]

    return n, m, k, bonus_enclosures, enclosure_sizes, enclosure_weights


def print_filled_bbox(bbox: List[List[int]]) -> None:
    data: Dict[int, List[Tuple[int, int]]] = {}

    for i in range(len(bbox)):
        for j in range(len(bbox[i])):
            value = bbox[i][j]

            if value in data:
                data[value].append((i, j))
            else:
                data[value] = [(i, j)]

    for _, coordinates in sorted(data.items()):
        for x, y in coordinates:
            print(f"{x} {y} ", end="")

    print()


class RanOutOfTimeException(Exception):
    """
    Exception thrown once we've ran out of time (execution time took too long)
    """


_bbox = None


def handle_exit(*args):
    global _bbox

    if _bbox is not None:
        print("I'm printing one last time before exiting")
        print_filled_bbox(_bbox)


atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)


try:
    with timeout(120, exception=RanOutOfTimeException):
        parser = argparse.ArgumentParser()
        parser.add_argument("-e", required=True, type=str,
                            help="Chemin vers l'exemplaire")
        parser.add_argument("-p", action="store_true",
                            help="Affiche les indices des villes a visiter en commencant par 0 et finissant par 0")
        args = parser.parse_args()
        p = bool(args.p)

        n, m, k, bonus_enclosures, enclosure_sizes, enclosure_weights = read_file(Path(str(args.e)), p)
        


        enclosures = [Enclosure(id=i, size=enclosure_sizes[i]) for i in range(n)]
        bonus_enclosures = [enclosures[i] for i in bonus_enclosures]
        enclosures = populate_most_valuable_neighbors(enclosures, bonus_enclosures, enclosure_weights)

        # gen = pack_enclosures(enclosures, bonus_enclosures, enclosure_weights)

        # while _bbox := next(gen):
        #     print_filled_bbox(_bbox)
        
except RanOutOfTimeException:
    print("I ran out of time!!!")
    pass
