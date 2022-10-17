# PIIS
Lab1:
Лі Алгоритм:

python3 pacman.py -l bigMaze -p SearchAgent -z .8

АСтар:

python3  pacman.py -l bigMaze -z .8 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

Жадібний АСтар:

python3  pacman.py -l bigMaze -z .8 -p SearchAgent -a fn=gass,heuristic=manhattanHeuristic

Шлях по кутам:

python3 pacman.py -l bigCorners -z .5 -p SearchAgent -a fn=astar,prob=CornersProblem

Зібрати всі монети:

python3 pacman.py -l trickySearch -p AStarFoodSearchAgent

Lab2:
Мінімакс: 

python3 pacman.py -p MinimaxAgent -l smallClassic -a depth=4

Альфа-Бетта відсікання: 

python3 pacman.py -p AlphaBetaAgent  -l smallClassic -a depth=3

експектімакс: 

python3 pacman.py -p ExpectimaxAgent -l smallClassic -a depth=4
