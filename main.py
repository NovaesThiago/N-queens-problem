"""
main.py
Programa principal para resolver o problema das n-rainhas.
"""

import argparse
from state import NQueensState
from heuristics import attacking_pairs_heuristic
from algorithms import AStarSearch, GreedySearch
from utils import print_solution_board, validate_solution, create_results_table

def solve_n_queens(n: int, algorithms: list = ['astar', 'greedy']) -> dict:
    """
    Resolve o problema das n-rainhas com os algoritmos especificados.
    
    Args:
        n: Tamanho do tabuleiro
        algorithms: Lista de algoritmos a executar
        
    Retorna:
        Dicionário com resultados
    """
    print(f"\n{'='*60}")
    print(f"PROBLEMA DAS {n}-RAINHAS")
    print(f"{'='*60}")
    
    # Estado inicial: tabuleiro vazio
    initial_state = NQueensState(n)
    print(f"Estado inicial: {initial_state}")
    print(f"Heurística: Pares de rainhas em conflito")
    
    results = {}
    
    # Executa A* se solicitado
    if 'astar' in algorithms:
        print(f"\n[1] Executando A*...")
        astar = AStarSearch(attacking_pairs_heuristic)
        result_astar = astar.search(initial_state)
        results['A*'] = result_astar
        
        print(f"   Status: {'✓ Solução encontrada' if result_astar.solution_found else '✗ Sem solução'}")
        print(f"   Estados explorados: {result_astar.states_explored:,}")
        print(f"   Tempo: {result_astar.execution_time:.3f} segundos")
        
        if result_astar.solution_found:
            print(f"   Profundidade: {result_astar.solution_depth}")
            print(f"   Solução: {result_astar.solution.positions}")
            
            # Valida a solução
            is_valid = validate_solution(result_astar.solution.positions)
            print(f"   Solução válida: {'✓' if is_valid else '✗'}")
            
            if n <= 15:  # Só mostra tabuleiro para n pequeno
                print_solution_board(result_astar.solution.positions)
    
    # Executa Busca Gulosa se solicitado
    if 'greedy' in algorithms:
        print(f"\n[2] Executando Busca Gulosa...")
        greedy = GreedySearch(attacking_pairs_heuristic)
        result_greedy = greedy.search(initial_state)
        results['Busca Gulosa'] = result_greedy
        
        print(f"   Status: {'✓ Solução encontrada' if result_greedy.solution_found else '✗ Sem solução'}")
        print(f"   Estados explorados: {result_greedy.states_explored:,}")
        print(f"   Tempo: {result_greedy.execution_time:.3f} segundos")
        
        if result_greedy.solution_found:
            print(f"   Profundidade: {result_greedy.solution_depth}")
            print(f"   Solução: {result_greedy.solution.positions}")
            
            # Valida a solução
            is_valid = validate_solution(result_greedy.solution.positions)
            print(f"   Solução válida: {'✓' if is_valid else '✗'}")
            
            if n <= 15 and (not results.get('A*') or 
                           results['A*'].solution.positions != result_greedy.solution.positions):
                print_solution_board(result_greedy.solution.positions)
    
    return results

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description='Resolve o problema das n-rainhas usando A* e Busca Gulosa.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py 8                    # Resolve para n=8 com ambos algoritmos
  python main.py 8 --algorithm astar  # Usa apenas A*
  python main.py 8 --algorithm greedy # Usa apenas Busca Gulosa
        """
    )
    
    parser.add_argument('n', type=int, help='Número de rainhas (tamanho do tabuleiro)')
    parser.add_argument('--algorithm', choices=['astar', 'greedy', 'both'], 
                       default='both', help='Algoritmo a usar (padrão: ambos)')
    
    args = parser.parse_args()
    
    # Converte 'both' para lista de algoritmos
    if args.algorithm == 'both':
        algorithms = ['astar', 'greedy']
    else:
        algorithms = [args.algorithm]
    
    # Verifica se n é válido
    if args.n <= 0:
        print("Erro: n deve ser um número positivo.")
        return
    
    if args.n > 20:
        print(f"Aviso: n={args.n} pode resultar em busca muito lenta.")
        confirm = input("Deseja continuar? (s/n): ")
        if confirm.lower() != 's':
            return
    
    # Executa a solução
    try:
        results = solve_n_queens(args.n, algorithms)
        
        # Resumo comparativo
        print(f"\n{'='*60}")
        print("RESUMO COMPARATIVO")
        print(f"{'='*60}")
        
        for algo_name, result in results.items():
            if result.solution_found:
                print(f"{algo_name:<15} | ✓ Solução | {result.states_explored:>12,} estados | {result.execution_time:>7.3f}s")
            else:
                print(f"{algo_name:<15} | ✗ Sem solução | {result.states_explored:>12,} estados | {result.execution_time:>7.3f}s")
        
        print(f"\n{'='*60}")
        
    except KeyboardInterrupt:
        print("\n\nBusca interrompida pelo usuário.")
    except Exception as e:
        print(f"\nErro durante a execução: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()