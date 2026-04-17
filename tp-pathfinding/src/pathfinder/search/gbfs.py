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
            row, col = state
            end_row, end_col = goal
            return abs(row - end_row) + abs(col - end_col)

       # Frontera como cola de prioridad 
        frontier = PriorityQueueFrontier()
        frontier.add(root, heuristic(root.state, grid.end))

         # Alcanzados guarda el costo (aunque GBFS no lo usa mucho)
        reached = {}
        reached[root.state] = root.cost

        # ¿El inicial ya es objetivo?
        if grid.objective_test(root.state):
            return Solution(root, reached)

        # Bucle principal
        while True:

            if frontier.is_empty():
                return NoSolution(reached)

            node = frontier.pop()

            # Expandimos
            for action in grid.actions(node.state):

                result = grid.result(node.state, action)
                new_cost = node.cost + 1  # como en BFS

                # Condición del pseudocódigo
                if result not in reached or new_cost < reached[result]:

                    new_node = Node("", result, new_cost, node, action)
                    reached[result] = new_cost

                    # ¿Llegamos?
                    if grid.objective_test(new_node.state):
                        return Solution(new_node, reached)

                    # PRIORIDAD = heurística
                    priority = heuristic(new_node.state, grid.end)
                    frontier.add(new_node, priority)

        return NoSolution(reached)
