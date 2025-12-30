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
        self.states_generated = 0
        self.solution_depth = 0
        self.execution_time = 0.0
        self.solution_path = []
        self.max_f_score = 0  # Para análise
        self.max_depth = 0    # Para análise
    
    def __str__(self) -> str:
        """Representação string dos resultados."""
        status = "SOLUÇÃO ENCONTRADA" if self.solution_found else "SEM SOLUÇÃO"
        return (
            f"Algoritmo: {self.algorithm}\n"
            f"Tabuleiro: {self.n}x{self.n}\n"
            f"Status: {status}\n"
            f"Estados gerados: {self.states_generated:,}\n"
            f"Estados explorados: {self.states_explored:,}\n"
            f"Profundidade da solução: {self.solution_depth}\n"
            f"Profundidade máxima: {self.max_depth}\n"
            f"Tempo de execução: {self.execution_time:.3f}s\n"
        )
    
    def to_dict(self) -> Dict:
        """Converte para dicionário para serialização."""
        return {
            'algorithm': self.algorithm,
            'n': self.n,
            'solution_found': self.solution_found,
            'solution': self.solution.positions if self.solution else None,
            'states_explored': self.states_explored,
            'states_generated': self.states_generated,
            'solution_depth': self.solution_depth,
            'max_depth': self.max_depth,
            'max_f_score': self.max_f_score,
            'execution_time': self.execution_time
        }

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
        open_set = []  # Fila de prioridade (f, g, id, estado)
        heapq.heappush(open_set, (0, 0, id(initial_state), initial_state))
        
        g_score = {initial_state: 0}  # Custo do caminho do início até n
        came_from = {}  # Para reconstruir o caminho
        
        states_generated = 1  # Estado inicial
        states_explored = 0
        max_depth = 0
        max_f_score = 0
        
        while open_set:
            # Verifica timeout
            if time.time() - start_time > timeout:
                result.execution_time = time.time() - start_time
                result.states_explored = states_explored
                result.states_generated = states_generated
                result.max_depth = max_depth
                result.max_f_score = max_f_score
                return result
            
            # Pega o estado com menor f(n) = g(n) + h(n)
            current_f, current_g, _, current_state = heapq.heappop(open_set)
            states_explored += 1
            
            # Atualiza métricas
            max_depth = max(max_depth, current_g)
            max_f_score = max(max_f_score, current_f)
            
            # Verifica se é objetivo
            if current_state.is_goal():
                result.solution = current_state
                result.solution_found = True
                result.states_explored = states_explored
                result.states_generated = states_generated
                result.solution_depth = current_g
                result.max_depth = max_depth
                result.max_f_score = max_f_score
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
                states_generated += 1
                
                # Custo do caminho até o sucessor = g(current) + 1
                tentative_g = current_g + 1
                
                # Se encontramos um caminho melhor para este estado
                if successor not in g_score or tentative_g < g_score[successor]:
                    g_score[successor] = tentative_g
                    came_from[successor] = current_state
                    
                    # f(n) = g(n) + h(n)
                    h = self.heuristic(successor)
                    f_score = tentative_g + h
                    heapq.heappush(open_set, (f_score, tentative_g, id(successor), successor))
        
        result.states_explored = states_explored
        result.states_generated = states_generated
        result.max_depth = max_depth
        result.max_f_score = max_f_score
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
        heapq.heappush(open_set, (self.heuristic(initial_state), 0, id(initial_state), initial_state))
        
        came_from = {}
        visited = set()
        states_generated = 1  # Estado inicial
        states_explored = 0
        max_depth = 0
        
        while open_set:
            # Verifica timeout
            if time.time() - start_time > timeout:
                result.execution_time = time.time() - start_time
                result.states_explored = states_explored
                result.states_generated = states_generated
                result.max_depth = max_depth
                return result
            
            # Pega o estado com menor h(n)
            current_h, current_depth, _, current_state = heapq.heappop(open_set)
            
            if current_state in visited:
                continue
            
            visited.add(current_state)
            states_explored += 1
            max_depth = max(max_depth, current_depth)
            
            # Verifica se é objetivo
            if current_state.is_goal():
                result.solution = current_state
                result.solution_found = True
                result.states_explored = states_explored
                result.states_generated = states_generated
                result.solution_depth = current_depth
                result.max_depth = max_depth
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
                states_generated += 1
                if successor not in visited:
                    came_from[successor] = current_state
                    h_score = self.heuristic(successor)
                    heapq.heappush(open_set, (h_score, current_depth + 1, id(successor), successor))
        
        result.states_explored = states_explored
        result.states_generated = states_generated
        result.max_depth = max_depth
        result.execution_time = time.time() - start_time
        return result