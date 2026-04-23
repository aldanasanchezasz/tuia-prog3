"""
Módulo de estrategias para el juego del Tateti

Este módulo contiene las estrategias para elegir la acción a realizar.
Los alumnos deben implementar la estrategia minimax.

Por defecto, se incluye una estrategia aleatoria como ejemplo base.
"""

import random
from typing import List, Tuple
from tateti import Tateti, JUGADOR_MAX, JUGADOR_MIN

def estrategia_aleatoria(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    """
    Estrategia aleatoria: elige una acción al azar entre las disponibles.
  
    Args:
        tateti: Instancia de la clase Tateti
        estado: Estado actual del tablero
        
    Returns:
        Tuple[int, int]: Acción elegida (fila, columna)

    Raises:
        ValueError: Si no hay acciones disponibles
    """
    acciones_disponibles = tateti.acciones(estado)
    if not acciones_disponibles:
        raise ValueError("No hay acciones disponibles")
    
    return random.choice(acciones_disponibles)

def estrategia_minimax(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    """
    Estrategia minimax: elige la mejor acción usando el algoritmo minimax.
    
    Args:
        tateti: Instancia de la clase Tateti
        estado: Estado actual del tablero
        
    Returns:
        Tuple[int, int]: Acción elegida (fila, columna)
        
    Raises:
        NotImplementedError: Hasta que el alumno implemente el algoritmo
    """

    # ---------------------------------------------------------------------

    def MINIMAX_MAX(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
       # Calcula recursivamente el valor minimax en un nodo MAX  

       # Caso base: si el estado es terminal, devuelve la utilidad
       if tateti.test_terminal(estado):
           return tateti.utilidad(estado, JUGADOR_MAX)
       
       # Como MAX busca el mayor valor posible, empezamos desde el peor caso.
       valor = float("-inf")

       # Probamos todas las jugadas posibles:
       for accion in tateti.acciones(estado):
           sucesor = tateti.resultado(estado, accion)
           # Comparamos con el mejor resultado que ya obtuvimos:
           valor = max(valor, MINIMAX_MIN(tateti, sucesor))  
           # se llama a minimax_min porque es el jugador que sigue

       # Retornamos el mejor resulatdo para el jugador MAX:
       return valor



    def MINIMAX_MIN(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
        # Calcula recursivamente el valor minimax en un nodo MIN

        # Caso base: si el estado es terminal, devuelve la utilidad
        if tateti.test_terminal(estado):
            return tateti.utilidad(estado, JUGADOR_MAX)
        
        # Como MIN busca el menor valor posible, empezamos desde el peor caso.
        valor = float("inf")

        # Probamos todas las jugadas posibles:
        for accion in tateti.acciones(estado):
            sucesor = tateti.resultado(estado, accion)
            # Comparamos con el mejor resultado que ya obtuvimos:
            valor = min(valor, MINIMAX_MAX(tateti, sucesor))  
            # se llama a minimax_max porque es el jugador que sigue

        # Retornamos el mejor resultado para el jugador MIN:
        return valor



    def MINIMAX(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
        # Toma un estado y devuelve la mejor acción a aplicar segun la estrategia minimax.

        # Caso base: se alcanzó el estado objetivo:
        if tateti.test_terminal(estado):
            return None

        ### Si juega MAX:
        if tateti.jugador(estado) == JUGADOR_MAX:

            # Creamos un diccionario donde guardaremos cada acción posible y su valor minimax
            sucesor = {}

            # Evaluamos cada acción posible:
            for accion in tateti.acciones(estado):
                nuevo_estado = tateti.resultado(estado, accion)
                # Guardamos ese resultado en el diccionario:
                sucesor[accion] = MINIMAX_MIN(tateti, nuevo_estado)

            # Busco el máximo valor del diccionario: la acción con el mayor valor minimax:
            accion_mejor = max(sucesor, key=sucesor.get)

            return accion_mejor
        

        ### Si juega MIN:
        else:

            # Creamos un diccionario donde guardaremos cada acción posible y su valor minimax
            sucesor = {}

            # Evaluamos cada acción posible:
            for accion in tateti.acciones(estado):
                nuevo_estado = tateti.resultado(estado, accion)
                # Guardamos ese resultado en el diccionario:
                sucesor[accion] = MINIMAX_MAX(tateti, nuevo_estado)

            # Busco el mínimo valor del diccionario: la acción con el menor valor minimax:
            accion_mejor = min(sucesor, key=sucesor.get)

            return accion_mejor
    accion = MINIMAX(tateti, estado)

    if accion is None:
        raise ValueError("No hay acciones disponibles")

    return accion