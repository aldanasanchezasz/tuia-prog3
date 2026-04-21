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

         # Alcanzados guarda el costo 
        reached = {}
        reached[root.state] = True #root.cost #CAMBIOOOOOOOOOOOOOOOOOOOOOOOO

        # Ver si el inicial es el objetivo
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

                # Condicional
                if result not in reached:

                    new_node = Node("", result, 0, node, action)
                    reached[result] = True

                    # Test objetivo
                    if grid.objective_test(new_node.state):
                        return Solution(new_node, reached)

                    # Prioridad = heurística
                    priority = heuristic(new_node.state, grid.end)
                    frontier.add(new_node, priority)

        return NoSolution(reached)
