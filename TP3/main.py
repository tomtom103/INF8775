import argparse
from pathlib import Path

import numpy as np

from utils import Graph

def read_file(file: Path) -> Graph:
    g = Graph()

    with open(file, 'r') as f:
        lines = f.readlines()
    
    # n: nombre d'enclos
    # m: nombre d'enclos dans le sous-ensemble S
    # k: la distance maximale a respecter pour les enclos du sous-ensemble
    n, m, k = list(map(lambda x: int(x), lines[0].split(" ")))
    print(f"n = {n}, m = {m}, k = {k}")
    
    # Liste d'enclos a placer a une distance de k pour obtenir
    # le bonus V = m^2
    bonus_enclosures = list(map(lambda x: int(x), lines[1].split(" ")))
    print(f"Liste des enclos a placer pour bonus: {bonus_enclosures}")

    # Tailles des enclos i pour i allant de 0 a n-1
    enclosure_size = [int(lines[i].strip()) for i in range(2, n + 2)]

    for i in range(n):
        g.add_vertex(i, enclosure_size[i])

    assert len(enclosure_size) == n

    print(f"Taille des enclos: {enclosure_size}")

    # n lignes representent les poids de l'enclos i vers les n autre enclos
    # on a un poids de zero pour une distance avec soi-meme    
    weight_matrix = [[int(val) for val in line.split(" ")] for line in lines[n + 2:]]

    for i in range(n):
        for j in range(n):
            if weight_matrix[i][j] != 0: # if [i][j] == 0 then [j][i] == 0 because diagonal
                g.add_edge(i, j, weight_matrix[i][j])
                g.add_edge(j, i, weight_matrix[j][i])

    print(f"Matrice de poids: \n{np.matrix(weight_matrix)}")

    return g


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", required=True, type=str,
                        help="Chemin vers l'exemplaire")
    parser.add_argument("-p", action="store_true",
                        help="Affiche les indices des villes a visiter en commencant par 0 et finissant par 0")
    args = parser.parse_args()

    g = read_file(Path(str(args.e)))

    p = bool(args.p)

    if p:
        # A chaque fois qu'une meilleure solution est trouvée, affiche la nouvelle solution. Format décrit dans le rapport
        ...
    else:
        # Afficher seulement l'attrait total du zoo à chaque fois qu'une meilleure solution est trouvée.
        ...
