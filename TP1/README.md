# TP1

# Mise en situation

Ce travail pratique se répartit sur deux séances de laboratoire et porte sur l’analyse empirique et hybride des algorithmes. Dans les capsules vidéo de la semaine 3, trois approches d’analyse de l’implantation d’un algorithme sont décrites. Vous les mettrez en pratique pour des algorithmes de résolution d’un problème connu.

# Implantation

Vous implanterez les algorithmes de multiplication de matrices conventionnel et diviser-pour-régner (algorithme de Strassen). Vous ferez deux versions de ce dernier, avec et sans un seuil de récursivité déterminé expérimentalement par essai-erreur. Pour la version avec seuil de récursivité, les (sous-)exemplaires dont la taille est en deçà de ce seuil ne seront plus résolus récursivement mais plutôt directement avec l’algorithme conventionnel. Assurez-vous que vos implantations sont correctes en comparant les résultats des trois algorithmes.

# Jeu de données

Vous travaillerez avec des matrices de taille 2N × 2N. Pour chaque valeur de N, vous devrez générer cinq matrices que vous pourrez multiplier deux à deux, ce qui vous donnera dix exemplaires. Utilisez au moins cinq valeurs consécutives de N pour votre analyse, ce choix pourra varier d’une équipe à l’autre selon la qualité de vos implémentations.

Vous trouverez dans l’archive du TP un script python inst_gen.py servant à générer les exemplaires. Ce script s’exécute de la manière suivante :

```bash
inst_gen.py  -S TAILLE_MIN [-t NB_TAILLES] [-n NB_EXEMPLAIRES] [-r RANDOM_SEED]
```

- `TAILLE_MIN` correspond à la plus petite valeur de N que vous voudrez utiliser
- `NB_TAILLES` correspond au nombre de tailles consécutives que vous voulez générer (par exemple si `TAILLE_MIN = 2` et `NB_TAILLES = 3`, alors le script génèrera des matrices pour N = 2, N = 3 et N = 4.
- `NB_EXEMPLAIRES` correspond au nombre de matrices que vous voulez générer pour chaque taille
- `RANDOM_SEED` correspond à la seed utilisée pour la génération aléatoire des matrices


Les fichiers générés débutent avec la valeur de N sur la première ligne et les lignes suivantes correspondent aux lignes de la matrice où chaque nombre est séparé par une tabulation. Voici un exemple pour N = 2 :

```
1	3	2	1
0	1	2	2
3	3	3	1
3	0	1	1
```

**Pour chacun des trois algorithmes, mesurez le temps d’exécution des exemplaires et rapportez dans un tableau le temps moyen pour chaque taille d’exemplaire.**
