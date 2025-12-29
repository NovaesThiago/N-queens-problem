"""
heuristics.py
Funções heurísticas para o problema das n-rainhas.
"""

from state import NQueensState

def attacking_pairs_heuristic(state: NQueensState) -> int:
    """
    Heurística especificada no trabalho:
    Número de pares de rainhas que se atacam direta ou indiretamente.
    
    Args:
        state: Estado do problema
        
    Retorna:
        Número de pares em conflito
    """
    return state.count_conflicts()

# Podemos adicionar outras heurísticas se necessário
def remaining_queens_heuristic(state: NQueensState) -> int:
    """
    Heurística alternativa: número de rainhas que faltam posicionar.
    É admissível e pode ser usada para comparação.
    """
    return state.n - state.count_queens()