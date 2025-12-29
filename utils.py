"""
utils.py
Funções utilitárias para o projeto.
"""

import os
import json
from typing import List, Dict
from state import NQueensState

def validate_solution(solution: List[int]) -> bool:
    """
    Valida se uma solução é válida.
    
    Args:
        solution: Lista onde solution[i] = coluna da rainha na linha i
        
    Retorna:
        True se a solução for válida, False caso contrário
    """
    n = len(solution)
    
    # Verifica limites
    for col in solution:
        if col < 0 or col >= n:
            return False
    
    # Verifica conflitos
    for i in range(n):
        for j in range(i + 1, n):
            if solution[i] == solution[j]:  # Mesma coluna
                return False
            if abs(i - j) == abs(solution[i] - solution[j]):  # Mesma diagonal
                return False
    
    return True

def print_solution_board(solution: List[int]) -> None:
    """
    Imprime a solução em formato de tabuleiro.
    
    Args:
        solution: Lista com posições das rainhas
    """
    n = len(solution)
    
    print("\n" + "=" * (2 * n + 3))
    for row in range(n):
        print("|", end="")
        for col in range(n):
            if solution[row] == col:
                print(" ♛ |", end="")
            else:
                print("   |", end="")
        print()
        print("+" + "---+" * n)
    print()

def save_results_to_file(results: Dict, filename: str) -> None:
    """
    Salva resultados em arquivo JSON.
    
    Args:
        results: Dicionário com resultados
        filename: Nome do arquivo (sem extensão)
    """
    os.makedirs("results", exist_ok=True)
    
    # Converte objetos para formatos serializáveis
    serializable_results = {}
    for key, value in results.items():
        if hasattr(value, '__dict__'):
            serializable_results[key] = value.__dict__
        else:
            serializable_results[key] = value
    
    filepath = f"results/{filename}.json"
    with open(filepath, 'w') as f:
        json.dump(serializable_results, f, indent=2, default=str)
    
    print(f"Resultados salvos em: {filepath}")

def create_results_table(results: Dict) -> str:
    """
    Cria uma tabela formatada com os resultados.
    
    Args:
        results: Dicionário com resultados por n e algoritmo
        
    Retorna:
        String com tabela formatada
    """
    table = []
    table.append("="*80)
    table.append("RESULTADOS - PROBLEMA DAS N-RAINHAS")
    table.append("="*80)
    table.append(f"{'n':<6} {'Algoritmo':<15} {'Sucesso':<10} {'Estados':<12} {'Tempo(s)':<10} {'Profund.'}")
    table.append("-"*80)
    
    for n, algo_results in results.items():
        for algo_name, result in algo_results.items():
            success = "✓" if result.solution_found else "✗"
            table.append(f"{n:<6} {algo_name:<15} {success:<10} {result.states_explored:<12,} {result.execution_time:<10.3f} {result.solution_depth}")
    
    return "\n".join(table)