import argparse
import os
from pathlib import Path

import numpy as np

def read_file(file: Path) -> ...:
    with open(file, 'r') as f:
        lines = f.readlines()
    n, m, k = list(map(lambda x: int(x), lines[0].split(" ")))
    print(f"n = {n}, m = {m}, k = {k}")
    
    liste_enclos = list(map(lambda x: int(x), lines[1].split(" ")))
    print(f"Liste des enclos: {liste_enclos}")

    tailles_enclos = []
    for i in range(2, n + 2):
        tailles_enclos.append(int(lines[i].strip()))

    print(f"Taille des enclos: {tailles_enclos}")

    # Remaining n lines
    # n lignes representent les poids de l'enclos i vers les n autre enclos
    # on a un poids de zero pour une distance avec soi-meme
    lines = lines[i + 1:]
    
    matrice_poids = []
    for line in lines:
        vec_ligne = []
        for val in line.split(" "):
            vec_ligne.append(int(val))

        matrice_poids.append(vec_ligne)

    print(f"Matrice de poids: \n{np.matrix(matrice_poids)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", required=True, type=str,
                        help="Chemin vers l'exemplaire")
    parser.add_argument("-p", action="store_true",
                        help="Affiche les indices des villes a visiter en commencant par 0 et finissant par 0")
    args = parser.parse_args()

    read_file(Path(str(args.e)))

    if bool(args.p):
        # A chaque fois qu'une meilleure solution est trouvée, affiche la nouvelle solution. Format décrit dans le rapport
        ...
    else:
        # Afficher seulement l'attrait total du zoo à chaque fois qu'une meilleure solution est trouvée.
        ...
