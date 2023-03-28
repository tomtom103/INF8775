import argparse
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", required=True, type=str,
                        help="Chemin vers l'exemplaire")
    parser.add_argument("-p", action="store_true",
                        help="Affiche les indices des villes a visiter en commencant par 0 et finissant par 0")
    args = parser.parse_args()

    fichier = Path(str(args.e))

    if bool(args.p):
        # A chaque fois qu'une meilleure solution est trouvée, affiche la nouvelle solution. Format décrit dans le rapport
        ...
    else:
        # Afficher seulement l'attrait total du zoo à chaque fois qu'une meilleure solution est trouvée.
        ...
