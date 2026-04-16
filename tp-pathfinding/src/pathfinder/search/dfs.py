from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize expanded with the empty dictionary
        expanded = dict()

        #--------------------------------------------------------------------

        # El nodo raíz, ¿tiene estado objetivo?
        if grid.objective_test(root.state):
            return Solution(root, expanded)

        # Initialize frontier with the root node
        frontier = StackFrontier()
        frontier.add(root)

        # Bucle principal:
        while True:

            # Si la frontera queda vacía, no hay solución:
            if frontier.is_empty():
                return NoSolution(expanded)
            
            # Tomamos el último nodo agregado:
            node = frontier.remove()

            # Acciones que puedo realizar con dicho nodo:
            for action in grid.actions(node.state):

                # Resultado que da aplicar cada acción al nodo:
                result = grid.result(node.state, action)

                # Creo un nuevo nodo (hijo) con el resultado:
                new_node = Node('', result, node.cost + 1, node, action) 
                
                # Para evitar ciclos (reviso antes de crear hijo):
                if result not in expanded:
                    expanded[result] = True # “ya visité este estado”
                
                    # Verifico si este nuevo nodo hijo llegó al objetivo:
                    if grid.objective_test(new_node.state):
                        return Solution(new_node, expanded)
                
                    # En caso de que no lo sea, lo agrego a la frontera:
                    frontier.add(new_node)

        return NoSolution(expanded)