#!/usr/bin/env python3

# INF8775 - Analyse et conception d'algorithmes
#   TP3
#
#   AUTEURS :
#     DANSEREAU, Charles - 13 mars 2023
#
#   RÉSUMÉ DES CHANGEMENTS :
#     13/03/2023 - Disponibilité initiale.
#
#   USAGE :
#     Ce script génère les exemplaires requis pour le TP3.
#
#     $ ./inst_gen.py -n NB_ENCLOS -m TAILLE-S [-x PRÉFIXE]
#
#     où :
#       * NB_BATIMENTS est la taille du problème et 
#       * NB_EXEMPLAIRES est le nombre d'exemplaires différents requis (par défaut 1).
#
#     Il est nécessaire de rendre ce script exécutable en utilisant chmod +x
#     Python 3.5 ou ultérieur recommandé pour lancer ce script.

import random
import argparse
import numpy as np


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nb-enclos", \
                        help="Représente la taille du graphe à générer", \
                        action='store', required=True, metavar='NB_ENCLOS', type=int)
    parser.add_argument("-m", "--taille-s", \
                        help="Représente la taille du sous-ensemble d'enclos à placer à proximité", \
                        action='store', required=False, metavar='TAILLE_MAX', type=int)
    parser.add_argument("-x", "--prefixe", \
                        help="Ajouter le préfixe indiqué aux noms des fichiers", \
                        action='store', required=False, metavar='PREFIXE', type=str)

    args = parser.parse_args()
    if not args.prefixe:
        args.prefixe = 'ex'
    else:
        args.prefixe = args.prefixe + '_'
    if args.taille_s > args.nb_enclos:
        print(f"La taille du sous-ensemble donnée est supérieure au nombre d'enclos, elle a été fixée à {args.nb_enclos}")
        args.taille_s = args.nb_enclos

    # Parameters
    max_weight = 100

    #initialize
    tailles = []
    poids = []
    theme = []

    #generate data
    for i in range(args.nb_enclos):
        tailles.append(random.randint(2, 20))

        poids_i = []
        for j in range(args.nb_enclos):
            poids_i.append(random.randint(1, max_weight))
            if i == j:
                poids_i[j] = 0

        poids.append(poids_i)

    max_dist = np.ceil(np.sqrt(args.taille_s*11)*2)-10
    theme = random.sample(range(args.nb_enclos),k=args.taille_s)




    # Write
    with open(args.prefixe + '_n' + str(args.nb_enclos) + '_m' +  str(args.taille_s) + ".txt",'w') as inst:
        inst.write("%d %d %d\n" % (args.nb_enclos, args.taille_s, max_dist))

        for i in range(args.taille_s-1):
            inst.write("%d " % theme[i])
        inst.write("%d\n" % theme[-1])

        for i in range(args.nb_enclos):
            inst.write("%d\n" % tailles[i])

        for i in range(args.nb_enclos):
            for j in range(args.nb_enclos-1):
                inst.write("%d " % poids[i][j])
            inst.write("%d\n" % poids[i][-1])
