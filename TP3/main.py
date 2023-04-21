import argparse
import math
import os
import random
import itertools
import dataclasses
import multiprocessing
import atexit
import signal
from multiprocessing.connection import Connection
from threading import Timer

from pathlib import Path
from typing import List, Tuple

import itertools
from typing import List, Tuple

@dataclasses.dataclass
class Enclosure:
    id: int
    size: int
    shape: List[Tuple[int, int]] = dataclasses.field(default_factory=list, hash=False, compare=False) # [(x, y), (x, y)]

    def __hash__(self) -> int:
        return hash((self.id, self.size))
    
    def __eq__(self, other: "Enclosure") -> bool:
        if not isinstance(other, self.__class__):
            return False
        
        return all((
            self.id == other.id,
            self.size == other.size,
            set(self.shape) == set(other.shape)
        ))
    
    def __str__(self) -> str:
        return f"<Enclosure id={self.id}, size={self.size}, shape={str(self.shape)}>"


def generate_spiral_grid(enclosures: List[Enclosure]) -> List[List[Tuple[int, int]]]:
    sizes = [(enclosure.id, enclosure.size) for enclosure in enclosures]
    unrolled_enclosures = []
    for id, size in sizes:
        unrolled_enclosures.extend([id] * size)

    n = len(unrolled_enclosures)
    # Calculate dimensions of the _bbox
    rows = cols = math.ceil(math.sqrt(n))

    visited = set()

    # Initialize the _bbox
    solution = [[] for _ in range(len(enclosures))]

    # Start from the center
    row, col = rows // 2, cols // 2

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    direction_index = 0
    steps_in_current_direction = 1
    steps_taken = 0

    for id in unrolled_enclosures:
        solution[id].append((row, col))
        visited.add((row, col))

        if steps_taken == steps_in_current_direction:
            direction_index = (direction_index + 1) % 4
            steps_taken = 0
            if direction_index in (0, 2):
                steps_in_current_direction += 1

        next_row, next_col = row + directions[direction_index][0], col + directions[direction_index][1]
        
        while not (0 <= next_row < rows and 0 <= next_col < cols) or (next_row, next_col) in visited:
            direction_index = (direction_index + 1) % 4
            next_row, next_col = row + directions[direction_index][0], col + directions[direction_index][1]
            if direction_index in (0, 2):
                steps_in_current_direction += 1
                
        row, col = next_row, next_col
        steps_taken += 1

    return solution


def swap_random_enclosures(enclosures: List[Enclosure]) -> List[Enclosure]:
    operation = random.choice(["swap", "rotate"])

    if operation == "swap":
        idx1, idx2 = random.sample(range(len(enclosures)), 2)
        enclosures[idx1], enclosures[idx2] = enclosures[idx2], enclosures[idx1]

    elif operation == "rotate":
        rotate_left = random.choice([True, False])
        if rotate_left:
            enclosures.insert(0, enclosures.pop())
        else:
            enclosures.append(enclosures.pop(0))

    return enclosures


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def total_score(
    solution: List[List[Tuple[int, int]]], 
    weights: List[List[int]],
    bonus_enclosures: List[int],
    k: int,
) -> int:
    distances = [[99999 for _ in solution] for _  in solution]
    for zero, one in itertools.combinations(range(len(solution)), 2):
        for x_start, y_start in solution[zero]:
            for x_end, y_end in solution[one]:
                length = distance(x_start, y_start, x_end, y_end)
                if length < distances[zero][one]:
                    distances[zero][one] = length
                    distances[one][zero] = length

    somme = 0
    for i in range(len(solution)):
        for j in range(len(solution)):
            somme += weights[i][j] * distances[i][j]

    bonus = len(bonus_enclosures) ** 2
    for paire in itertools.combinations(bonus_enclosures, 2):
        if distances[paire[0]][paire[1]] > k:
            bonus = 0
            break

    return bonus - somme

def late_acceptance_hill_climbing(
    enclosures: List[Enclosure],
    bonus_enclosures: List[int],
    weights: List[List[int]],
    k: int,
    look_back_steps: int,
    max_iterations: int,
    send_end: Connection
) -> List[Enclosure]:
    best_order = enclosures[:]
    best_score = total_score(generate_spiral_grid(enclosures), weights, bonus_enclosures, k)

    current_solution = enclosures[:]
    current_score = best_score

    scores_history = [current_score] * look_back_steps

    for iteration in range(max_iterations):
        new_solution = swap_random_enclosures(current_solution[:])
        new_score = total_score(generate_spiral_grid(new_solution), weights, bonus_enclosures, k)

        history_index = iteration % look_back_steps
        if new_score >= scores_history[history_index]:
            current_solution = new_solution
            current_score = new_score
            scores_history[history_index] = new_score

        if current_score > best_score:
            best_order = current_solution[:]
            best_score = current_score

    send_end.send((best_order, best_score))

# def simulated_annealing(
#     enclosures: List[Enclosure],
#     bonus_enclosures: List[int],
#     weights: List[List[int]],
#     k: int,
#     initial_temperature: float,
#     cooling_rate: float,
#     send_end: Connection
# ) -> None:
#     best_order = enclosures[:]
#     best_score = total_score(generate_spiral_grid(enclosures), weights, bonus_enclosures, k)

#     current_temperature = initial_temperature

#     while current_temperature > 1:
#         new_order = enclosures[:]
#         new_order = swap_random_enclosures(new_order)


#         current_score = total_score(generate_spiral_grid(enclosures), weights, bonus_enclosures, k)
#         new_score = total_score(generate_spiral_grid(new_order), weights, bonus_enclosures, k)
#         score_diff = new_score - current_score

#         if score_diff < 0 or math.exp(-score_diff / current_temperature) > random.random():
#             enclosures = new_order
#             current_score = new_score
        
#         if current_score > best_score:
#             best_order = enclosures[:]
#             best_score = current_score

#         current_temperature *= cooling_rate
    
#     send_end.send((best_order, best_score))

def late_acceptance_hill_climbing_parallel(
    enclosures: List[Enclosure],
    bonus_enclosures: List[int],
    weights: List[List[int]],
    k: int,
    lookback_steps: int,
    max_iterations: int,
    num_processes: int,
) -> Tuple[List[Enclosure], int]:
    processes: List[multiprocessing.Process] = []
    pipe_list: List[Connection] = []
    for _ in range(num_processes):
        recv_end, send_end = multiprocessing.Pipe(False)
        p = multiprocessing.Process(
            target=late_acceptance_hill_climbing,
            args=(
                enclosures, 
                bonus_enclosures, 
                weights, 
                k, 
                lookback_steps,
                max_iterations,
                send_end
            )
        )
        processes.append(p)
        pipe_list.append(recv_end)
        p.daemon = True
        p.start()

    for p in processes:
        p.join()

    results_list = [x.recv() for x in pipe_list]
    best_result = max(results_list, key=lambda x: x[1])

    return best_result


def read_file(file_path: Path):
    with open(file_path, 'r') as file:
        n, m, k = map(int, file.readline().split())
        bonus_enclosures = list(map(int, file.readline().split()))
        enclosure_sizes = [int(file.readline()) for _ in range(n)]
        enclosure_weights = [list(map(int, file.readline().split())) for _ in range(n)]

    return n, m, k, bonus_enclosures, enclosure_sizes, enclosure_weights


def print_solution(solution: List[List[Tuple[int, int]]]):
    for coordinates in solution:
        for x, y in coordinates:
            print(f"{x} {y} ", end="")
        print()
    print()


def handle_exit(*args):
    global best_order

    if best_order:
        solution = generate_spiral_grid(best_order)
        print_solution(solution)
        os._exit(0)


atexit.register(handle_exit)
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


if __name__ == "__main__":
    # Start 120 second timer
    Timer(120, os.kill, [os.getpid(), signal.SIGTERM]).start()

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", required=True, type=str,
                        help="Chemin vers l'exemplaire")
    parser.add_argument("-p", action="store_true",
                        help="Affiche les indices des villes a visiter en commencant par 0 et finissant par 0")
    args = parser.parse_args()
    p = bool(args.p)

    n, m, k, bonus_enclosures, enclosure_sizes, enclosure_weights = read_file(Path(str(args.e)))

    enclosures = [Enclosure(id=i, size=enclosure_sizes[i]) for i in range(n)]

    best_order = enclosures[:]
    solution = generate_spiral_grid(best_order)
    best_score = total_score(solution, enclosure_weights, bonus_enclosures, k)
    if p:
        print_solution(solution)

    while True:
        new_order, new_score = late_acceptance_hill_climbing_parallel(
            best_order,
            bonus_enclosures,
            enclosure_weights,
            k,
            lookback_steps=1000,
            max_iterations=10000,
            num_processes=multiprocessing.cpu_count(),
        )
        if new_score > best_score:
            best_order = new_order
            best_score = new_score
            if p:
                solution = generate_spiral_grid(best_order)
                print_solution(solution)
