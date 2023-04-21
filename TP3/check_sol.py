  ################################################################################
#
# Auteur: CHARLES DANSEREAU
# dernière modification: 2023-03-16 //disponibilité initiale
#
# Ce script vérifie si votre solution est valide. C'est le script qui sera
# utilisé pour la correction, donc assurez-vous que la sortie de votre
# script tp.sh est compatible avec ce script-ci.
#
# Argument 1 : Path vers l'exemplaire
# Argument 2 : Path vers la solution de cet exemplaire
#
# Exemple d'utilisation :
#
#   1. Vous exécutez votre algorithme avec tp.sh et vous envoyez son résultat
#      vers un fichier texte :
#
#      ./tp.sh -e ./exemplaires/10_3_25_0.txt -p > sol_10_3_25_0.txt
#
#   2. Vous vérifiez si votre solution est valide avec ce script-ci (où k=3 ici):
#
#      python3 check_sol.py ./exemplaires/10_3_25_0.txt sol_10_3_25_0.txt
#
################################################################################

import numpy as np
import pathlib
import sys
from itertools import combinations
from collections import defaultdict

# Initial sanity checks
if (len(sys.argv) != 3):
    exit("ERREUR : Ce script de vérification de solution prend 2 " + \
         "arguments en entrée.")
if (not pathlib.Path(sys.argv[1]).is_file()):
    exit("ERREUR : Fichier " + sys.argv[1] + " inexistant.")
if (not pathlib.Path(sys.argv[2]).is_file()):
    exit("ERREUR : Fichier " + sys.argv[2] + " inexistant.")


def validPath(n: int, d: defaultdict(set), start: int, end: int) -> bool:
    stack = []
    visited = set()

    visited.add(start)
    stack.append(start)

    while stack:
        node = stack.pop(0)
        if node == end: return True

        for x in d[node]:
            if x not in visited:
                visited.add(x)
                stack.append(x)
    return False

def distance(x1, y1, x2, y2):
    return abs(x2-x1)+abs(y2-y1)


# Chargement de la solution
with open(sys.argv[2], 'r') as file:
    sol = []
    duplicates = {}
    full_sol = file.read().split('\n\n')
    # Parse seulement la dernière solution proposée
    for line in full_sol[-1].strip().split('\n'):
        coords =  line.strip().split(' ')
        enclos = []
        for i in range(round(len(coords)/2)):
            if (coords[2*i] + ' ' + coords[2*i+1]) in duplicates:
                exit(f"ERREUR : une ou plusieurs cases ont les mêmes coordonnées.")
            else:
                duplicates[coords[2*i] + ' ' + coords[2*i+1]] = 0

            enclos.append([int(coords[2*i]), int(coords[2*i+1])])
        sol.append(enclos)


# Chargement du graphe et des paramètres
with open(sys.argv[1], 'r') as file:
    #lecture
    tailles =[]
    poids = []
    for num_line, lines in enumerate(file.readlines()):
        if num_line == 0:
            [n, m, k] = lines.strip().split(' ')
            n, m, k = int(n), int(m), int(k)
        elif num_line == 1:
            theme = lines.strip().split(' ')
        elif num_line > 1 and num_line <= n+1:
            tailles.append(lines.strip('\n'))
        else:
            poids.append(lines.strip().split(' '))

    theme = [eval(i) for i in theme]
    tailles = [eval(i) for i in tailles]
    poids = [[eval(i) for i in enclos] for enclos in poids]




#création de la representation de la solution
tailles_sol = []
for enclos in sol:
    tailles_sol.append(len(enclos))


# Vérification de la validité de la solution
#nombre de voisins de chaque case
#pas de répétitions dans les coordonnées

try:
    theme[m-1]
    tailles[n-1]
    poids[n-1][n-1]
except:
    exit("ERREUR : Problème avec le format de la solution.")

if not tailles_sol == tailles:
    exit(f"ERREUR : un ou des enclos n'a pas la taille correspondant au fichier d'entrée.")


for enclos in sol:
    voisins = defaultdict(set)
    combs = combinations(range(len(enclos)),2)
    for paire in combs:
        x1 = enclos[paire[0]][0]
        y1 = enclos[paire[0]][1]

        x2 = enclos[paire[1]][0]
        y2 = enclos[paire[1]][1]

        if ((x1 == x2 and y1 == y2 + 1) or (x1 == x2 and y1 == y2 - 1)): #voisin vertical
            voisins[paire[0]].add(paire[1])
            voisins[paire[1]].add(paire[0])
        elif ((x1 == x2 +1 and y1 == y2) or (x1 == x2 - 1 and y1 == y2)): #voisin horizontal
            voisins[paire[0]].add(paire[1])
            voisins[paire[1]].add(paire[0])

    for i in range(len(enclos)):
        if not validPath(len(enclos), voisins, 0, i):
            exit(f"ERREUR : un ou des enclos n'est pas contigu.")






# Évaluation de la solution

#somme de tous les poids
distances = [[99999 for _ in sol] for _ in sol]
combs_enclos = combinations(range(len(sol)),2)
for paire in combs_enclos:
    for start in sol[paire[0]]:
        for end in sol[paire[1]]:
            length = distance(start[0], start[1], end[0], end[1])
            if length < distances[paire[0]][paire[1]]:
                distances[paire[0]][paire[1]] = length
                distances[paire[1]][paire[0]] = length

somme = 0
for i, _ in enumerate(sol):
    for j, _ in enumerate(sol):
        somme += poids[i][j]*distances[i][j]

#vérifier la contrainte de distance
combs_theme = combinations(theme,2)
bonus = m**2
for paire in combs_theme:
    if distances[paire[0]][paire[1]] > k:
        bonus = 0
        break
print("Votre solution est valide et a une valeur de", bonus - somme)



