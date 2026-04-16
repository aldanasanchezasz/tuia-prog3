from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

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
        
        # ------------------------------------------------------------------
           
        # Initialize frontier with the root node
        frontier = PriorityQueueFrontier()
        frontier.add(root)

        # Agrego al diccionario de alcanzados el estado inicial con su costo:
        reached[root.state] = root.cost

        # Bucle principal:
        while True:

            # Si la frontera queda vacía, no hay solución:
            if frontier.is_empty():
                return NoSolution(reached)
            
            # Si aún hay nodos en la frontera, vamos por el de menor prioridad:
            node = frontier.pop()

            # Si el nodo que saqué de la frontera es el objetivo, retorno:
            if grid.objective_test(node.state):
                return Solution(node, reached)

            # Acciones que puedo realizar con dicho nodo:
            for action in grid.actions(node.state):

                # Resultado que da aplicar cada acción al nodo:
                result = grid.result(node.state, action)

                # Obtengo el costo de seguir ese camino:
                cost = node.cost + grid.individual_cost(node.state, action)

                # Evalúo si conviene usar ese camino:
                if result not in reached or cost < reached[result]:
                    
                    # Creo un nuevo nodo (hijo) con el resultado:
                    new_node = Node('', result, cost, node, action)

                    # Lo agrego a alcanzados:
                    reached[result] = cost

                    # Lo agrego a la frontera:
                    frontier.add(new_node, cost)
        
        # ------------------------------------------------------------------

        return NoSolution(reached)
