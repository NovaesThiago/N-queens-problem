"""
run_experiments.py
Script para executar experimentos controlados.
"""

import time
from state import NQueensState
from heuristics import attacking_pairs_heuristic
from algorithms import AStarSearch, GreedySearch
from utils import create_results_table, save_results_to_file

def run_experiments(n_values: list = None, timeout: int = 60):
    """
    Executa experimentos para diferentes valores de n.
    
    Args:
        n_values: Lista de valores de n para testar
        timeout: Tempo máximo por execução (segundos)
    """
    if n_values is None:
        n_values = [4, 8, 10, 12]  # Valores recomendados para teste
    
    print("\n" + "="*80)
    print("EXPERIMENTOS - PROBLEMA DAS N-RAINHAS")
    print("="*80)
    print(f"Valores de n: {n_values}")
    print(f"Timeout: {timeout}s por execução")
    print("="*80)
    
    all_results = {}
    
    for n in n_values:
        print(f"\n[+] Testando n = {n}")
        print("-"*40)
        
        initial_state = NQueensState(n)
        results_n = {}
        
        # A*
        print(f"  Executando A*...", end="", flush=True)
        start_time = time.time()
        astar = AStarSearch(attacking_pairs_heuristic)
        result_astar = astar.search(initial_state, timeout=timeout)
        elapsed = time.time() - start_time
        
        status = "✓" if result_astar.solution_found else "✗"
        print(f" {status} ({elapsed:.1f}s)")
        results_n['A*'] = result_astar
        
        # Busca Gulosa
        print(f"  Executando Busca Gulosa...", end="", flush=True)
        start_time = time.time()
        greedy = GreedySearch(attacking_pairs_heuristic)
        result_greedy = greedy.search(initial_state, timeout=timeout)
        elapsed = time.time() - start_time
        
        status = "✓" if result_greedy.solution_found else "✗"
        print(f" {status} ({elapsed:.1f}s)")
        results_n['Busca Gulosa'] = result_greedy
        
        all_results[n] = results_n
    
    # Imprime tabela de resultados
    print("\n" + "="*80)
    table = create_results_table(all_results)
    print(table)
    
    # Salva resultados
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    save_results_to_file(all_results, f"experiment_results_{timestamp}")
    
    return all_results

def analyze_results(results: dict):
    """Analisa e compara os resultados dos experimentos."""
    print("\n" + "="*80)
    print("ANÁLISE DOS RESULTADOS")
    print("="*80)
    
    for n, algo_results in results.items():
        print(f"\nn = {n}:")
        
        astar_result = algo_results.get('A*')
        greedy_result = algo_results.get('Busca Gulosa')
        
        if astar_result and greedy_result:
            print(f"  A*:            {astar_result.states_explored:>10,} estados | {astar_result.execution_time:>7.3f}s")
            print(f"  Busca Gulosa:  {greedy_result.states_explored:>10,} estados | {greedy_result.execution_time:>7.3f}s")
            
            if astar_result.solution_found and greedy_result.solution_found:
                ratio = greedy_result.states_explored / max(astar_result.states_explored, 1)
                print(f"  Razão (Gulosa/A*): {ratio:.2f}x")

def main():
    """Função principal do script de experimentos."""
    print("TRABALHO DE IA - PROBLEMA DAS N-RAINHAS")
    print("Executando experimentos controlados...")
    
    # Valores para teste (pode ajustar conforme necessário)
    test_values = [4, 8, 10, 12]
    
    # Para testes mais rápidos:
    # test_values = [4, 8]
    
    # Para testes mais abrangentes (pode demorar):
    # test_values = [4, 8, 10, 12, 15]
    
    results = run_experiments(test_values, timeout=120)
    analyze_results(results)
    
    print("\n" + "="*80)
    print("EXPERIMENTOS CONCLUÍDOS")
    print("="*80)

if __name__ == "__main__":
    main()