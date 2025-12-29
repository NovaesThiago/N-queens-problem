"""
algorithms.py
Implementação dos algoritmos de busca A* e Busca Gulosa.
"""

import heapq
import time
from typing import Dict, List, Tuple, Optional, Callable
from state import NQueensState

class SearchResult:
    """Armazena os resultados de uma busca."""
    
    def __init__(self, algorithm: str, n: int):
        self.algorithm = algorithm
        self.n = n
        self.solution = None
        self.solution_found = False
        self.states_explored = 0
        self.solution_depth = 0
        self.execution_time = 0.0
        self.solution_path = []
    
    def __str__(self) -> str:
        """Representação string dos resultados."""
        status = "SOLUÇÃO ENCONTRADA" if self.solution_found else "SEM SOLUÇÃO"
        return (
            f"Algoritmo: {self.algorithm}\n"
            f"Tabuleiro: {self.n}x{self.n}\n"
            f"Status: {status}\n"
            f"Estados explorados: {self.states_explored:,}\n"
            f"Profundidade da solução: {self.solution_depth}\n"
            f"Tempo de execução: {self.execution_time:.3f}s\n"
        )

class AStarSearch:
    """Implementação do algoritmo A*."""
    
    def __init__(self, heuristic_func: Callable[[NQueensState], int]):
        """
        Inicializa o algoritmo A*.
        
        Args:
            heuristic_func: Função heurística h(n)
        """
        self.heuristic = heuristic_func
        self.name = "A*"
    
    def search(self, initial_state: NQueensState, timeout: int = 300) -> SearchResult:
        """
        Executa busca A*.
        
        Args:
            initial_state: Estado inicial
            timeout: Tempo máximo em segundos
            
        Retorna:
            Resultado da busca
        """
        result = SearchResult(self.name, initial_state.n)
        start_time = time.time()
        
        # Estruturas de dados para A*
        open_set = []  # Fila de prioridade (f, g, estado)
        heapq.heappush(open_set, (0, 0, initial_state))
        
        g_score = {initial_state: 0}  # Custo do caminho do início até n
        came_from = {}  # Para reconstruir o caminho
        
        states_explored = 0
        
        while open_set:
            # Verifica timeout
            if time.time() - start_time > timeout:
                result.execution_time = time.time() - start_time
                return result
            
            # Pega o estado com menor f(n) = g(n) + h(n)
            current_f, current_g, current_state = heapq.heappop(open_set)
            states_explored += 1
            
            # Verifica se é objetivo
            if current_state.is_goal():
                result.solution = current_state
                result.solution_found = True
                result.states_explored = states_explored
                result.solution_depth = current_g
                result.execution_time = time.time() - start_time
                
                # Reconstrói o caminho
                path = []
                state = current_state
                while state in came_from:
                    path.append(state)
                    state = came_from[state]
                path.append(initial_state)
                result.solution_path = list(reversed(path))
                
                return result
            
            # Gera e processa sucessores
            for successor in current_state.get_successors():
                # Custo do caminho até o sucessor = g(current) + 1
                tentative_g = current_g + 1
                
                # Se encontramos um caminho melhor para este estado
                if successor not in g_score or tentative_g < g_score[successor]:
                    g_score[successor] = tentative_g
                    came_from[successor] = current_state
                    
                    # f(n) = g(n) + h(n)
                    f_score = tentative_g + self.heuristic(successor)
                    heapq.heappush(open_set, (f_score, tentative_g, successor))
        
        result.states_explored = states_explored
        result.execution_time = time.time() - start_time
        return result

class GreedySearch:
    """Implementação da Busca Gulosa."""
    
    def __init__(self, heuristic_func: Callable[[NQueensState], int]):
        """
        Inicializa a busca gulosa.
        
        Args:
            heuristic_func: Função heurística h(n)
        """
        self.heuristic = heuristic_func
        self.name = "Busca Gulosa"
    
    def search(self, initial_state: NQueensState, timeout: int = 300) -> SearchResult:
        """
        Executa busca gulosa.
        
        Args:
            initial_state: Estado inicial
            timeout: Tempo máximo em segundos
            
        Retorna:
            Resultado da busca
        """
        result = SearchResult(self.name, initial_state.n)
        start_time = time.time()
        
        # Fila de prioridade ordenada apenas pela heurística
        open_set = []
        heapq.heappush(open_set, (self.heuristic(initial_state), 0, initial_state))
        
        came_from = {}
        visited = set()
        states_explored = 0
        
        while open_set:
            # Verifica timeout
            if time.time() - start_time > timeout:
                result.execution_time = time.time() - start_time
                return result
            
            # Pega o estado com menor h(n)
            current_h, current_depth, current_state = heapq.heappop(open_set)
            
            if current_state in visited:
                continue
            
            visited.add(current_state)
            states_explored += 1
            
            # Verifica se é objetivo
            if current_state.is_goal():
                result.solution = current_state
                result.solution_found = True
                result.states_explored = states_explored
                result.solution_depth = current_depth
                result.execution_time = time.time() - start_time
                
                # Reconstrói o caminho
                path = []
                state = current_state
                while state in came_from:
                    path.append(state)
                    state = came_from[state]
                path.append(initial_state)
                result.solution_path = list(reversed(path))
                
                return result
            
            # Gera e processa sucessores
            for successor in current_state.get_successors():
                if successor not in visited:
                    came_from[successor] = current_state
                    h_score = self.heuristic(successor)
                    heapq.heappush(open_set, (h_score, current_depth + 1, successor))
        
        result.states_explored = states_explored
        result.execution_time = time.time() - start_time
        return result