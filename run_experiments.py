"""
run_experiments.py
Script para executar experimentos controlados.
"""

import time
import json
import os
from datetime import datetime
from state import NQueensState
from heuristics import attacking_pairs_heuristic
from algorithms import AStarSearch, GreedySearch
from utils import create_results_table, save_results_to_file
from visualization import ResultsVisualizer

def run_experiments(n_values: list = None, timeout: int = 1200):
    """
    Executa experimentos para diferentes valores de n.
    
    Args:
        n_values: Lista de valores de n para testar
        timeout: Tempo máximo por execução (segundos)
    """
    if n_values is None:
        n_values = [8, 80, 800]  # Valores recomendados para teste
    
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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
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
            astar_success = "✓" if astar_result.solution_found else "✗"
            greedy_success = "✓" if greedy_result.solution_found else "✗"
            
            print(f"  A*:            {astar_success} {astar_result.states_explored:>10,} estados | {astar_result.execution_time:>7.3f}s")
            print(f"  Busca Gulosa:  {greedy_success} {greedy_result.states_explored:>10,} estados | {greedy_result.execution_time:>7.3f}s")
            
            if astar_result.solution_found and greedy_result.solution_found:
                ratio_states = greedy_result.states_explored / max(astar_result.states_explored, 1)
                ratio_time = greedy_result.execution_time / max(astar_result.execution_time, 0.001)
                print(f"  Razão Gulosa/A*: {ratio_states:.2f}x estados, {ratio_time:.2f}x tempo")

def generate_plots(results: dict):
    """Gera gráficos dos resultados."""
    print("\n" + "="*80)
    print("GERANDO GRÁFICOS")
    print("="*80)
    
    visualizer = ResultsVisualizer("plots")
    
    # Gráficos individuais
    print("\n[1] Gráfico de Tempo de Execução...")
    visualizer.plot_comparison(
        results, 
        metric='execution_time',
        title='Comparação de Tempo de Execução',
        ylabel='Tempo (segundos)',
        log_scale=True
    )
    
    print("\n[2] Gráfico de Estados Explorados...")
    visualizer.plot_comparison(
        results,
        metric='states_explored',
        title='Comparação de Estados Explorados',
        ylabel='Estados Explorados',
        log_scale=True
    )
    
    print("\n[3] Gráfico de Taxa de Sucesso...")
    visualizer.plot_success_rate(results)
    
    # Gráfico com múltiplas métricas
    print("\n[4] Gráfico com Múltiplas Métricas...")
    visualizer.plot_multiple_metrics(
        results,
        metrics=['execution_time', 'states_explored', 'solution_depth'],
        titles=['Tempo de Execução', 'Estados Explorados', 'Profundidade da Solução']
    )
    
    # Gráfico de resumo completo
    print("\n[5] Gráfico de Análise Completa...")
    visualizer.create_summary_plot(results)
    
    print(f"\nGráficos salvos na pasta 'plots/'")

def main():
    """Função principal do script de experimentos."""
    print("TRABALHO DE IA - PROBLEMA DAS N-RAINHAS")
    print("Executando experimentos controlados e gerando gráficos...")
    
    # Valores para teste
    test_values = [8, 80, 800]
   
    # Para testes mais rápidos:
    # test_values = [4, 8]
    
    # Para testes mais abrangentes:
    # test_values = [4, 8, 10, 12, 15]
    
    # Executa experimentos
    results = run_experiments(test_values, timeout=1200)
    
    # Analisa resultados
    analyze_results(results)
    
    # Gera gráficos
    generate_plots(results)
    
    print("\n" + "="*80)
    print("EXPERIMENTOS CONCLUÍDOS")
    print("="*80)

if __name__ == "__main__":
    main()