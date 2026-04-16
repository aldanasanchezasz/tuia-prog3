from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = True

        # ------------------------------------------------------------------

        # El nodo raíz, ¿tiene estado objetivo?
        if grid.objective_test(root.state):
            return Solution(root, reached)

        # Initialize frontier with the root node
        frontier = QueueFrontier()
        frontier.add(root)

        # Bucle principal:
        while True:

            # Si la frontera queda vacía, no hay solución:
            if frontier.is_empty():
                return NoSolution(reached)
            
            # Si aún hay nodos en la frontera, vamos por el primero:
            node = frontier.remove()

            # Acciones que puedo realizar con dicho nodo:
            for action in grid.actions(node.state):

                # Resultado que da aplicar cada acción al nodo:
                result = grid.result(node.state, action)

                # Para evitar ciclos:
                if result not in reached:
                    reached[result] = True # “ya visité este estado”

                    # Creo un nuevo nodo (hijo) con el resultado:
                    new_node = Node('', result, node.cost + 1, node, action)

                    # Verifico si este nuevo nodo hijo llegó al objetivo:
                    if grid.objective_test(new_node.state):
                        return Solution(new_node, reached)
                    
                    # En caso de que no lo sea, lo agrego a la frontera:
                    frontier.add(new_node)

        # ------------------------------------------------------------------

        return NoSolution(reached)