import util
from util import Queue
from util import PriorityQueue

class SearchProblem:

    def getStartState(self):
        util.raiseNotDefined()

    def isGoalState(self, state):
        util.raiseNotDefined()

    def getSuccessors(self, state):
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def lee(problem: SearchProblem):

    set = Queue()
    set.push(problem.getStartState())
    trace = []
    previous_nodes = []
    trace_to_current_position = Queue()
    current_position = set.pop()
    while not problem.isGoalState(current_position):

        if current_position not in previous_nodes:
            previous_nodes.append(current_position)
            successors = problem.getSuccessors(current_position)

            for child, action, cost in successors:
                set.push(child)
                trace_to_current_position.push(trace + [action])

        current_position = set.pop()
        trace = trace_to_current_position.pop()

    return trace

def nullHeuristic(state, problem=None):
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):

    set = PriorityQueue()
    set.push(problem.getStartState(), 0)
    trace = []
    previous_nodes = []
    trace_to_current_position = PriorityQueue()
    current_position = set.pop()

    while not problem.isGoalState(current_position):
        if current_position not in previous_nodes:
            previous_nodes.append(current_position)
            successors = problem.getSuccessors(current_position)
            for child, action, cost in successors:
                current_cost = problem.getCostOfActions(trace + [action]) + heuristic(child, problem)
                set.push(child, current_cost)
                trace_to_current_position.push(trace + [action], current_cost)
        current_position = set.pop()
        trace = trace_to_current_position.pop()

    return trace
    # util.raiseNotDefined()
def greedAStarSearch(problem: SearchProblem, heuristic=nullHeuristic):

    set = PriorityQueue()
    set.push(problem.getStartState(), 0)
    trace = []
    previous_nodes = []
    trace_to_current_position = PriorityQueue()
    current_position = set.pop()

    while not problem.isGoalState(current_position):
        if current_position not in previous_nodes:
            previous_nodes.append(current_position)
            successors = problem.getSuccessors(current_position)
            for child, action, cost in successors:
                current_cost = heuristic(child, problem)
                set.push(child, current_cost)
                trace_to_current_position.push(trace + [action], current_cost)
        current_position = set.pop()
        trace = trace_to_current_position.pop()

    return trace
    # util.raiseNotDefined()
# Abbreviations
bfs = lee
astar = aStarSearch
gass = greedAStarSearch
