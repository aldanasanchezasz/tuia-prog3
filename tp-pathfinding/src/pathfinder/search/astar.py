from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # La cola de prioridad a la frontera
        frontier = PriorityQueueFrontier()
        # Encolar en la frontera
        frontier.add(root, root.cost + heuristic(root.state, grid.end))

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

        # Heurística
        def heuristic(state, goal):
            x, y = state
            x_objetivo, y_objetivo = goal
            return abs(x - x_objetivo) + abs(y - y_objetivo)

        # Bucle principal
        while True:
            if frontier.is_empty():
                return NoSolution(reached)
            
            # Desencolar
            node = frontier.pop()
            
            # Test objetivo
            if grid.objective_test(node.state):
                return Solution(node, reached)
            
            for action in grid.actions(node.state):

                # Resultado
                result = grid.result(node.state, action)
                
                # Costo acumulado
                new_cost = node.cost + grid.individual_cost(node.state, action)
                
                # Condicional
                if result not in reached or new_cost < reached[result]:

                    new_node = Node("", result, new_cost, node, action)
                    reached[result] = new_cost
                    priority = new_node.cost + heuristic(new_node.state, grid.end)
                    frontier.add(new_node, priority)

        return NoSolution(reached)