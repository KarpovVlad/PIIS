from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):

    def getAction(self, gameState):

        legalMoves = gameState.getLegalActions()

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        # Визначити найменьшу відстань до привидів
        # Знайти найменьшу відстань до привидів, яка загрожує пакману найбільше

        nearestGhost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])

        if nearestGhost:
            distanceToGhost = -10/nearestGhost
        else:
            distanceToGhost = -1000

        foodList = newFood.asList()
        if foodList:
            nearestFood = min([manhattanDistance(newPos, food) for food in foodList])
        else:
            nearestFood = 0

        # Найбільша вага для залишившоїся їжі
        return (-2 * nearestFood) + distanceToGhost - (100*len(foodList))

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        def minimax_search(state, agentIndex, depth):
            # якщо в мінімальному шарі і останній привид
            if agentIndex == state.getNumAgents():
                # якщо досягнуто максимальної глибини, оцінюємо стан
                if depth == self.depth:
                    return self.evaluationFunction(state)
                # починаємо новий максимальний шар із більшою глибиною
                else:
                    return minimax_search(state, 0, depth + 1)
            # якщо не мінімальний шар і останній привид
            else:
                moves = state.getLegalActions(agentIndex)
                # якщо немає що робити, оцінюємо стан
                if len(moves) == 0:
                    return self.evaluationFunction(state)
                # отримати всі мінімаксні значення для наступного шару, причому кожен вузол є можливим станом після переміщення
                next = (minimax_search(state.generateSuccessor(agentIndex, m), agentIndex + 1, depth) for m in moves)

                # якщо максимальний шар, повертає максимальний шар нижче
                if agentIndex == 0:
                    return max(next)
                # якщо мінімальний шар, повернути мінімальний шар нижче нього
                else:
                    return min(next)
        # вибрати дію з найбільшим мінімаксним значенням
        result = max(gameState.getLegalActions(0), key=lambda x: minimax_search(gameState.generateSuccessor(0, x), 1, 1))

        return result

class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        Infinity = float('inf')

        def minValue(state, agentIndex, depth, a, b):
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)

            v = Infinity
            for action in legalActions:
                newState = state.generateSuccessor(agentIndex, action)

                # Перевіряємо чи це останній привид
                if agentIndex == state.getNumAgents() - 1:
                    newV = maxValue(newState, depth, a, b)
                else:
                    newV = minValue(newState, agentIndex + 1, depth, a, b)

                v = min(v, newV)
                if v < a:
                    return v
                b = min(b, v)
            return v

        def maxValue(state, depth, a, b):
            legalActions = state.getLegalActions(0)
            if not legalActions or depth == self.depth:
                return self.evaluationFunction(state)

            v = -Infinity
            # для увімкнення другого відсікання
            if depth == 0:
                bestAction = legalActions[0]
            for action in legalActions:
                newState = state.generateSuccessor(0, action)
                newV = minValue(newState, 0 + 1, depth + 1, a, b)
                if newV > v:
                    v = newV
                    if depth == 0:
                        bestAction = action
                if v > b:
                    return v
                a = max(a, v)

            if depth == 0:
                return bestAction
            return v

        bestAction = maxValue(gameState, 0, -Infinity, Infinity)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        def expectimax_search(state, agentIndex, depth):
            # якщо в мінімальному шарі, та останній привид
            if agentIndex == state.getNumAgents():
                # якщо досягнуто максимальної глибини, оцінює стан
                if depth == self.depth:
                    return self.evaluationFunction(state)
                # почати новий максимальний шар з більшою глибиною на 1
                else:
                    return expectimax_search(state, 0, depth + 1)
            # якщо не в мінімальному шарі, та останній привид
            else:
                moves = state.getLegalActions(agentIndex)
                # Якщо нічого не можемо зробити, оцінюємо стан
                if len(moves) == 0:
                    return self.evaluationFunction(state)
                # отримати всі мінімаксні значення для наступного шару, причому кожен вузол є можливим станом після переміщення
                next = (expectimax_search(state.generateSuccessor(agentIndex, m), agentIndex + 1, depth) for m in moves)

                # якщо максимальний шар, повертає максимальний шар нижче
                if agentIndex == 0:
                    return max(next)
                # якщо найнижчий шар, повертає експктімакс
                else:
                    l = list(next)
                    return sum(l) / len(l)
        # Обирає дію з найбільшою цінністю
        result = max(gameState.getLegalActions(0), key=lambda x: expectimax_search(gameState.generateSuccessor(0, x), 1, 1))

        return result

def betterEvaluationFunction(currentGameState):
    util.raiseNotDefined()
