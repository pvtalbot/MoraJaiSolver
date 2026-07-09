![CI Status](https://github.com/pvtalbot/MoraJaiSolver/actions/workflows/ci.yaml/badge.svg)

# Mora Jai Box Solver

Interface graphique et solveur pour le jeu de plateau Mora Jai de Blue Prince, développé par Tonda Ros (développeur Dogubomb, éditeur Raw Fury).

L'application comprend une interface utilisateur interactive développée avec CustomTkinter et un algorithme de recherche en largeur (BFS) utilisant des masques de bits pour l'exploration des états de la grille.

## Fonctionnalités et fonctionnement

* Interface graphique : En mode `Config`, renseignement de la grille de jeu. Il est également possible de créer une grille aléatoire. En mode `Play`, les tuiles effectuent leur action respective au clic. Un solveur est également disponible et affiche une solution, si elle existe.

* En coulisses, deux modélisations sont utilisées : le mode play utilise un dictionnaire de tuiles, mais le solveur modélise le plateau par un entier et calcule avec du bitmasking.

* Le solveur utilise une stratégie BFS pour trouver un des plus courts chemins en stockant chaque état de la grille 3x3 sur un entier de 36 bits, optimisant l'empreinte mémoire et la vitesse de comparaison.

* Quelques tests unitaires sont disponibles.

## Installation et lancement

Le projet est géré avec l'outil d'empaquetage et de gestion d'environnement `uv`.
1. Cloner le dépôt
```bash
git clone git@github.com:pvtalbot/MoraJaiSolver.git
cd MoraJaiSolver
```
2. Synchroniser l'environnement et les dépendances
```bash
uv sync
```
3. Exécuter l'application
```bash
uv run morajai-solver
```
Arguments optionnels :

* `[-v|--verbose]` : Active les logs de niveau DEBUG.

* `[-q|--quiet]` : Restreint les logs au niveau WARNING et supérieurs.

## Tests

Pour exécuter la suite complète de tests unitaires et d'intégration :
```bash
uv run pytest
```

## Structure du projet
```
MoraJaiSolver/
├── src/
│   └── morajai_solver/
│       ├── components/          # Composants graphiques UI (Boutons, Palettes)
│       ├── core/                # Moteur logique (GameEngine, Stratégies, Solver BFS)
│       ├── models/              # Modèles de données (MoraBoard Abstrait/Dict/Bitmask, Enums)
│       ├── views/               # Vues principales de l'application (Grille, Console, Solution)
│       └── main.py              # Point d'entrée de l'application
├── tests/
│   ├── strategies/              # Tests isolés pour les 10 règles de mouvements
│   ├── test_boards.py           # Cohérence entre l'implémentation Dict et Bitmask
│   ├── test_event_dispatcher.py # Validation du bus d'événements (Singleton)
│   └── test_victory.py          # Validation du calcul des conditions de victoire
├── pyproject.toml               # Définition du projet et des dépendances
└── uv.lock                      # Verrouillage des versions de l'environnement
```

## Règles et stratégies de couleur

L'objectif est d'aligner les couleurs de la grille interne (3x3) avec les objectifs situés aux 4 coins extérieurs (positions virtuelles 0 et 4). Chaque case déclenche un effet spécifique :

* Yellow : Échange sa position avec la case supérieure, si elle existe.
* Purple : Échange sa position avec la case inférieure, si elle existe
* Black : Effectue un décalage circulaire de sa ligne vers la droite.
* Green : Échange sa position avec sa case symétrique opposée par rapport à la tuile centrale.
* Pink : Effectue une rotation horaire de l'ensemble de ses voisins valides.
* Blue : Exécute la stratégie correspondant à la couleur située sur la tuile centrale.
* Red : Transforme les tuiles noires en tuiles rouges, et les tuiles blanches en tuiles noires.
* Orange : Remplace sa couleur par la couleur strictement majoritaire de ses voisins orthogonaux, si elle existe.
* White : Alterne entre les couleurs blanche et grise pour elle-même et ses voisins orthogonaux.
* Grey : Case neutre, aucune action associée.