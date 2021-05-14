# PI2C_abalone
- Nom: Lancelot Neirinckx
- Matricule: 18206
## But
Réaliser une intelligence artificielle pour le jeu Abalone qui devra intéragir avec un [gestionnaire de partie](https://github.com/qlurkin/PI2CChampionshipRunner).

## Utilisation
```
$ python server.py -h       
usage: server.py [-h] name port

Abalone AI

positional arguments:
  name        choose a name, leave blank for default (default)
  port        choose a port, leave blank for default (8026)

optional arguments:
  -h, --help  show this help message and exit
```

## Stratégie
Le code calculera d'abord tous les moves possibles qu'un pion peut jouer et essayera de créer un "train" de pions si possible.

Les moves sont ensuite triés dans l'ordre suivant:
- Sortir un pion adverse du plateau
- Pousser les pions adverses vers les bords
- Rassembler les pions vers le milieu

Les moves sont ensuite envoyés vers un algorithme negamax avec alpha beta pruning et une profondeur de 4. 
## Librairies utilisées
- `socket`: interaction avec [PI2CChampionshipRunner](https://github.com/qlurkin/PI2CChampionshipRunner)
- `json`: sérialiser / déserialiser des requêtes en json
- `sys`: récupérer les arguments (nom et port) dans la commande de ligne
- `argparse`: interface de commande de ligne
- `time`: calculer le temps que prends la recherche d'un move
- `copy`: copier l'état du jeu
