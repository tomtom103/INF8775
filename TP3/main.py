import numpy as np
import argparse
import math
import itertools
from pathlib import Path
from typing import List, Tuple, Dict, Iterator, Any
from dataclasses import dataclass, field


@dataclass
class Enclosure:
    id: int
    size: int
    shape: List[Tuple[int, int]] # [(x, y), (x, y)]
    neighbors: List[Tuple["Enclosure", int]] # Enclosure + weight to that enclosure

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

    while True: # TODO: Replace with time constraints instead
        bbox = [[0 for _ in range(width)] for _ in range(height)]

        for enclosure in enclosures:
            # TODO: Logic to place an enclosure within the box
            ...

            # assert len(enclosure.shape) == enclosure.size
            for x, y in enclosure.shape:
                bbox[y][x] = enclosure.id

        # TODO: Instead of yielding every time, only yield when we found a solution that is better than the previous one
        yield bbox

def populate_most_valuable_neighbors(enclosures: List[Enclosure], bonus_enclosures: List[Enclosure], weights: List[List[int]]) -> List[Enclosure]:
    # TODO: Do shit here

    for enclosure in enclosures:
        # TODO: Figure out how to populate the neighbors according to weights and bonus enclosures that need to be together
        # We could probably want some kind of heuristic here that tells us which enclosures absolutely need to be next to eachother
        # If we have a score of like 30 vs 300, the 300 one obviously takes priority
        enclosure.neighbors = []

    # Return all enclosures with a populated list of neighbors (IMPORTANT)
    return enclosures


def read_file(file_path: Path, p: bool):
    with open(file_path, 'r') as file:
        n, m, k = map(int, file.readline().split())
        print(f"n = {n}, m = {m}, k = {k}")

        bonus_enclosures = list(map(int, file.readline().split()))
        print(f"Liste des enclos a placer pour bonus: {bonus_enclosures}")

        enclosure_sizes = [int(file.readline()) for _ in range(n)]
        print(f"Taille des enclos: {enclosure_sizes}")

        enclosure_weights = [list(map(int, file.readline().split())) for _ in range(n)]
        print(f"Matrice de poids: \n{np.matrix(enclosure_weights)}")

    return n, m, k, bonus_enclosures, enclosure_sizes, enclosure_weights

if __name__ == "__main__":
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

    for bbox in pack_enclosures(enclosures, bonus_enclosures, enclosure_weights):
        # TODO: Find a way to properly print the bbox on each iteration
        ...
