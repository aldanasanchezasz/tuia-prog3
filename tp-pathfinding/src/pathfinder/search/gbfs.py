from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

        def heuristic(state, goal):
            x, y = state
            x_objetivo, y_objetivo = goal
            return abs(x - x_objetivo) + abs(y - y_objetivo)

        # Frontera como cola de prioridad 
        frontier = PriorityQueueFrontier()
        frontier.add(root, heuristic(root.state, grid.end))

        # Bucle principal
        while True:

            if frontier.is_empty():
                return NoSolution(reached)

            node = frontier.pop()

            # Ver si es el objetivo
            if grid.objective_test(node.state):
                return Solution(node, reached)

            # Expandimos
            for action in grid.actions(node.state):

                result = grid.result(node.state, action)

                costo = node.cost + grid.cost(node.state, action)

                # Condicional
                if result not in reached or costo < reached[result]:

                    new_node = Node("", result, costo, node, action)
                    reached[result] = costo

                    # Prioridad = heurística (seleccionamos el nodo con menor heurística)
                    priority = heuristic(new_node.state, grid.end)
                    # Lo agregamos a la cola de prioridad 
                    frontier.add(new_node, priority)

        return NoSolution(reached)