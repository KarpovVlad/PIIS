# PIIS
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
