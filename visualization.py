"""
visualization.py
Geração de gráficos e visualizações dos resultados.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Dict, List
from datetime import datetime

# Configuração do estilo dos gráficos
plt.style.use('seaborn-v0_8-darkgrid')
COLORS = {
    'A*': '#FF6B6B',        # Vermelho
    'Busca Gulosa': '#4ECDC4',  # Turquesa
    'A_star': '#FF6B6B',    # Vermelho (alternativo)
    'Greedy': '#4ECDC4'     # Turquesa (alternativo)
}

MARKERS = {
    'A*': 'o',
    'Busca Gulosa': 's',
    'A_star': 'o',
    'Greedy': 's'
}

class ResultsVisualizer:
    """Classe para visualização de resultados dos experimentos."""
    
    def __init__(self, output_dir: str = "plots"):
        """
        Inicializa o visualizador.
        
        Args:
            output_dir: Diretório para salvar os gráficos
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def plot_comparison(self, results: Dict, metric: str, title: str = None, 
                       ylabel: str = None, log_scale: bool = True, figsize=(10, 6)):
        """
        Plota comparação entre algoritmos para uma métrica específica.
        
        Args:
            results: Dicionário com resultados por n e algoritmo
            metric: Métrica a plotar ('execution_time', 'states_explored', etc.)
            title: Título do gráfico
            ylabel: Label do eixo Y
            log_scale: Se True, usa escala logarítmica no eixo Y
            figsize: Tamanho da figura
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Extrai dados
        algorithms = set()
        n_values = sorted(results.keys())
        
        for n in n_values:
            for algo in results[n].keys():
                algorithms.add(algo)
        
        algorithms = sorted(list(algorithms))
        
        # Prepara dados para plotagem
        data = {algo: [] for algo in algorithms}
        valid_n_values = []
        
        for n in n_values:
            valid_for_n = False
            for algo in algorithms:
                if algo in results[n] and results[n][algo].solution_found:
                    if hasattr(results[n][algo], metric):
                        data[algo].append(getattr(results[n][algo], metric))
                    else:
                        data[algo].append(results[n][algo].to_dict().get(metric, 0))
                    valid_for_n = True
                else:
                    data[algo].append(None)
            
            if valid_for_n:
                valid_n_values.append(n)
        
        # Plota cada algoritmo
        for algo in algorithms:
            values = [data[algo][n_values.index(n)] for n in valid_n_values 
                     if data[algo][n_values.index(n)] is not None]
            
            if values:
                ax.plot(valid_n_values[:len(values)], values, 
                       marker=MARKERS.get(algo, 'o'),
                       color=COLORS.get(algo, 'blue'),
                       linewidth=2, markersize=8, label=algo)
        
        if log_scale:
            ax.set_yscale('log')
        
        ax.set_xlabel('Tamanho do Tabuleiro (n)', fontsize=12)
        ax.set_ylabel(ylabel or self._get_metric_label(metric), fontsize=12)
        ax.set_title(title or f'Comparação de {self._get_metric_label(metric)}', fontsize=14)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Adiciona valores nos pontos
        for algo in algorithms:
            values = [data[algo][n_values.index(n)] for n in valid_n_values 
                     if data[algo][n_values.index(n)] is not None]
            if values:
                for i, (x, y) in enumerate(zip(valid_n_values[:len(values)], values)):
                    if y > 0:  # Só mostra se for maior que zero
                        ax.annotate(f'{self._format_number(y)}', 
                                   (x, y), textcoords="offset points", 
                                   xytext=(0,10), ha='center', fontsize=8)
        
        plt.tight_layout()
        
        # Salva o gráfico
        filename = f"{self.output_dir}/comparison_{metric}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()
        
        return filename
    
    def plot_multiple_metrics(self, results: Dict, metrics: List[str], 
                             titles: List[str] = None, figsize=(15, 8)):
        """
        Plota múltiplas métricas em subgráficos.
        
        Args:
            results: Dicionário com resultados
            metrics: Lista de métricas para plotar
            titles: Títulos para cada subgráfico
            figsize: Tamanho da figura
        """
        n_metrics = len(metrics)
        n_cols = min(3, n_metrics)
        n_rows = (n_metrics + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        
        if n_metrics == 1:
            axes = np.array([axes])
        if n_rows > 1 and n_cols > 1:
            axes = axes.flatten()
        elif n_rows == 1:
            axes = np.array(axes)
        
        for idx, metric in enumerate(metrics):
            if idx >= len(axes):
                break
                
            ax = axes[idx] if n_metrics > 1 else axes
            
            # Extrai dados para esta métrica
            algorithms = set()
            n_values = sorted(results.keys())
            
            for n in n_values:
                for algo in results[n].keys():
                    algorithms.add(algo)
            
            algorithms = sorted(list(algorithms))
            
            for algo in algorithms:
                x_vals = []
                y_vals = []
                
                for n in n_values:
                    if algo in results[n] and results[n][algo].solution_found:
                        x_vals.append(n)
                        if hasattr(results[n][algo], metric):
                            y_vals.append(getattr(results[n][algo], metric))
                        else:
                            y_vals.append(results[n][algo].to_dict().get(metric, 0))
                
                if x_vals:
                    ax.plot(x_vals, y_vals, 
                           marker=MARKERS.get(algo, 'o'),
                           color=COLORS.get(algo, 'blue'),
                           linewidth=2, markersize=6, label=algo)
            
            ax.set_xlabel('Tamanho do Tabuleiro (n)', fontsize=10)
            ax.set_ylabel(self._get_metric_label(metric), fontsize=10)
            
            if titles and idx < len(titles):
                ax.set_title(titles[idx], fontsize=11)
            else:
                ax.set_title(f'{self._get_metric_label(metric)}', fontsize=11)
            
            if idx == 0:  # Legenda apenas no primeiro
                ax.legend(fontsize=9)
            
            ax.grid(True, alpha=0.3)
            ax.set_yscale('log')
        
        # Esconde eixos extras se houver
        for idx in range(len(metrics), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        
        # Salva o gráfico
        filename = f"{self.output_dir}/multiple_metrics.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()
        
        return filename
    
    def plot_success_rate(self, results: Dict, figsize=(10, 6)):
        """
        Plota taxa de sucesso por algoritmo e tamanho do tabuleiro.
        
        Args:
            results: Dicionário com resultados
            figsize: Tamanho da figura
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        algorithms = set()
        n_values = sorted(results.keys())
        
        for n in n_values:
            for algo in results[n].keys():
                algorithms.add(algo)
        
        algorithms = sorted(list(algorithms))
        
        # Configuração do gráfico de barras
        bar_width = 0.35
        index = np.arange(len(n_values))
        
        for i, algo in enumerate(algorithms):
            success_rates = []
            for n in n_values:
                if algo in results[n]:
                    success_rates.append(1 if results[n][algo].solution_found else 0)
                else:
                    success_rates.append(0)
            
            ax.bar(index + i * bar_width, success_rates, bar_width,
                   label=algo, color=COLORS.get(algo, 'blue'))
        
        ax.set_xlabel('Tamanho do Tabuleiro (n)', fontsize=12)
        ax.set_ylabel('Taxa de Sucesso', fontsize=12)
        ax.set_title('Taxa de Sucesso por Algoritmo', fontsize=14)
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(n_values)
        ax.set_ylim(0, 1.1)
        ax.legend()
        
        # Adiciona valores nas barras
        for i, algo in enumerate(algorithms):
            for j, n in enumerate(n_values):
                if algo in results[n]:
                    height = 1 if results[n][algo].solution_found else 0
                    if height > 0:
                        ax.text(j + i * bar_width, height + 0.02, 
                               '✓', ha='center', fontsize=12)
        
        plt.tight_layout()
        
        # Salva o gráfico
        filename = f"{self.output_dir}/success_rate.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()
        
        return filename
    
    def plot_solution_board(self, solution: List[int], title: str = "Solução", figsize=(8, 8)):
        """
        Plota o tabuleiro com a solução.
        
        Args:
            solution: Lista com posições das rainhas
            title: Título do gráfico
            figsize: Tamanho da figura
        """
        n = len(solution)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Cria o tabuleiro (padrão xadrez)
        board = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                board[i, j] = (i + j) % 2
        
        # Plota o tabuleiro
        ax.imshow(board, cmap='binary', extent=(0, n, 0, n))
        
        # Plota as rainhas
        for row, col in enumerate(solution):
            # Rainha no centro da célula (col + 0.5, n - row - 0.5)
            ax.text(col + 0.5, n - row - 0.5, '♛', 
                   fontsize=min(300//n, 24), 
                   ha='center', va='center',
                   color='red')
        
        # Configurações do gráfico
        ax.set_xticks(np.arange(n) + 0.5)
        ax.set_yticks(np.arange(n) + 0.5)
        ax.set_xticklabels(range(n))
        ax.set_yticklabels(range(n))
        ax.set_xlabel('Coluna', fontsize=12)
        ax.set_ylabel('Linha', fontsize=12)
        ax.set_title(f'{title} (n={n})', fontsize=14, pad=20)
        ax.grid(True, color='black', linewidth=0.5)
        
        # Remove bordas
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        plt.tight_layout()
        
        # Salva o gráfico
        filename = f"{self.output_dir}/solution_n{n}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()
        
        return filename
    
    def create_summary_plot(self, results: Dict, figsize=(14, 10)):
        """
        Cria um plot com múltiplos subgráficos para análise completa.
        
        Args:
            results: Dicionário com resultados
            figsize: Tamanho da figura
        """
        fig = plt.figure(figsize=figsize)
        
        # Layout com 4 subgráficos
        gs = fig.add_gridspec(2, 3)
        
        # 1. Tempo de execução
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_metric_on_axis(ax1, results, 'execution_time', 'Tempo de Execução (s)')
        
        # 2. Estados explorados
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_metric_on_axis(ax2, results, 'states_explored', 'Estados Explorados')
        
        # 3. Estados gerados
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_metric_on_axis(ax3, results, 'states_generated', 'Estados Gerados')
        
        # 4. Taxa de sucesso
        ax4 = fig.add_subplot(gs[1, 0])
        self._plot_success_on_axis(ax4, results)
        
        # 5. Profundidade da solução
        ax5 = fig.add_subplot(gs[1, 1])
        self._plot_metric_on_axis(ax5, results, 'solution_depth', 'Profundidade da Solução')
        
        # 6. Razão Estados Explorados/Gerados
        ax6 = fig.add_subplot(gs[1, 2])
        self._plot_ratio_on_axis(ax6, results)
        
        plt.suptitle('Análise Comparativa - Problema das N-Rainhas', fontsize=16, y=1.02)
        plt.tight_layout()
        
        # Salva o gráfico
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/summary_analysis_{timestamp}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()
        
        return filename
    
    def _plot_metric_on_axis(self, ax, results: Dict, metric: str, ylabel: str):
        """Plota uma métrica específica em um eixo."""
        algorithms = set()
        n_values = sorted(results.keys())
        
        for n in n_values:
            for algo in results[n].keys():
                algorithms.add(algo)
        
        algorithms = sorted(list(algorithms))
        
        for algo in algorithms:
            x_vals = []
            y_vals = []
            
            for n in n_values:
                if algo in results[n] and results[n][algo].solution_found:
                    x_vals.append(n)
                    if hasattr(results[n][algo], metric):
                        y_vals.append(getattr(results[n][algo], metric))
                    else:
                        y_vals.append(results[n][algo].to_dict().get(metric, 0))
            
            if x_vals:
                ax.plot(x_vals, y_vals, 
                       marker=MARKERS.get(algo, 'o'),
                       color=COLORS.get(algo, 'blue'),
                       linewidth=2, markersize=6, label=algo)
        
        ax.set_xlabel('Tamanho do Tabuleiro (n)', fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(f'{ylabel} vs n', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')
        if metric == 'execution_time':
            ax.set_yscale('log')
    
    def _plot_success_on_axis(self, ax, results: Dict):
        """Plota taxa de sucesso em um eixo."""
        algorithms = set()
        n_values = sorted(results.keys())
        
        for n in n_values:
            for algo in results[n].keys():
                algorithms.add(algo)
        
        algorithms = sorted(list(algorithms))
        
        bar_width = 0.35
        index = np.arange(len(n_values))
        
        for i, algo in enumerate(algorithms):
            success_rates = []
            for n in n_values:
                if algo in results[n]:
                    success_rates.append(1 if results[n][algo].solution_found else 0)
                else:
                    success_rates.append(0)
            
            ax.bar(index + i * bar_width, success_rates, bar_width,
                   label=algo, color=COLORS.get(algo, 'blue'))
        
        ax.set_xlabel('Tamanho do Tabuleiro (n)', fontsize=10)
        ax.set_ylabel('Taxa de Sucesso', fontsize=10)
        ax.set_title('Taxa de Sucesso', fontsize=11)
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(n_values)
        ax.set_ylim(0, 1.1)
        ax.legend(fontsize=9)
    
    def _plot_ratio_on_axis(self, ax, results: Dict):
        """Plota razão entre estados explorados e gerados."""
        algorithms = set()
        n_values = sorted(results.keys())
        
        for n in n_values:
            for algo in results[n].keys():
                algorithms.add(algo)
        
        algorithms = sorted(list(algorithms))
        
        for algo in algorithms:
            x_vals = []
            y_vals = []
            
            for n in n_values:
                if algo in results[n] and results[n][algo].solution_found:
                    x_vals.append(n)
                    explored = results[n][algo].states_explored
                    generated = results[n][algo].states_generated
                    if generated > 0:
                        y_vals.append(explored / generated)
                    else:
                        y_vals.append(0)
            
            if x_vals:
                ax.plot(x_vals, y_vals, 
                       marker=MARKERS.get(algo, 'o'),
                       color=COLORS.get(algo, 'blue'),
                       linewidth=2, markersize=6, label=algo)
        
        ax.set_xlabel('Tamanho do Tabuleiro (n)', fontsize=10)
        ax.set_ylabel('Razão (Explorados/Gerados)', fontsize=10)
        ax.set_title('Eficiência da Exploração', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.1)
    
    def _get_metric_label(self, metric: str) -> str:
        """Retorna label formatado para métrica."""
        labels = {
            'execution_time': 'Tempo de Execução (s)',
            'states_explored': 'Estados Explorados',
            'states_generated': 'Estados Gerados',
            'solution_depth': 'Profundidade da Solução',
            'max_depth': 'Profundidade Máxima',
            'max_f_score': 'F-Score Máximo'
        }
        return labels.get(metric, metric.replace('_', ' ').title())
    
    def _format_number(self, num: float) -> str:
        """Formata número para exibição."""
        if num >= 1_000_000:
            return f'{num/1_000_000:.1f}M'
        elif num >= 1_000:
            return f'{num/1_000:.1f}K'
        else:
            return f'{num:.0f}'