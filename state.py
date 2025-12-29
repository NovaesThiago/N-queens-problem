"""
state.py
Representação do estado do problema das n-rainhas.
"""

from typing import List, Optional

class NQueensState:
    """Representa um estado do problema das n-rainhas."""
    
    def __init__(self, n: int, positions: List[int] = None):
        """
        Inicializa um estado do tabuleiro n x n.
        
        Args:
            n: Tamanho do tabuleiro
            positions: Lista de colunas das rainhas por linha
                      positions[i] = coluna da rainha na linha i
                      -1 indica que a linha está vazia
        """
        self.n = n
        if positions is None:
            self.positions = [-1] * n  # Tabuleiro vazio
        else:
            self.positions = positions.copy()
    
    def __eq__(self, other) -> bool:
        """Compara dois estados."""
        if not isinstance(other, NQueensState):
            return False
        return self.n == other.n and self.positions == other.positions
    
    def __hash__(self) -> int:
        """Hash para usar em conjuntos/dicionários."""
        return hash(tuple(self.positions))
    
    def __str__(self) -> str:
        """Representação string do estado."""
        return str(self.positions)
    
    def __repr__(self) -> str:
        """Representação para debug."""
        return f"NQueensState(n={self.n}, positions={self.positions})"
    
    def __lt__(self, other) -> bool:
        """
        Método necessário para comparação no heapq.
        Compara baseado nas posições das rainhas.
        """
        if not isinstance(other, NQueensState):
            return NotImplemented
        return str(self.positions) < str(other.positions)
    
    def is_goal(self) -> bool:
        """Verifica se é estado objetivo (solução completa)."""
        # Todas as linhas devem ter rainhas
        if -1 in self.positions:
            return False
        
        # Verifica se não há rainhas se atacando
        return self.count_conflicts() == 0
    
    def is_valid(self) -> bool:
        """Verifica se o estado atual é válido (sem conflitos)."""
        # Pega as rainhas já posicionadas
        queens = []
        for row in range(self.n):
            if self.positions[row] != -1:
                queens.append((row, self.positions[row]))
        
        # Verifica conflitos entre rainhas posicionadas
        for i in range(len(queens)):
            for j in range(i + 1, len(queens)):
                r1, c1 = queens[i]
                r2, c2 = queens[j]
                
                # Mesma coluna
                if c1 == c2:
                    return False
                # Mesma diagonal (|r1-r2| == |c1-c2|)
                if abs(r1 - r2) == abs(c1 - c2):
                    return False
        
        return True
    
    def get_next_empty_row(self) -> Optional[int]:
        """Retorna a próxima linha vazia, ou None se todas estiverem ocupadas."""
        try:
            return self.positions.index(-1)
        except ValueError:
            return None
    
    def get_successors(self) -> List['NQueensState']:
        """
        Gera estados sucessores colocando uma rainha na próxima linha vazia.
        
        Retorna:
            Lista de estados sucessores válidos
        """
        successors = []
        next_row = self.get_next_empty_row()
        
        # Se não há linha vazia, não há sucessores
        if next_row is None:
            return successors
        
        # Tenta colocar uma rainha em cada coluna da próxima linha vazia
        for col in range(self.n):
            # Cria novo estado com rainha na posição (next_row, col)
            new_positions = self.positions.copy()
            new_positions[next_row] = col
            new_state = NQueensState(self.n, new_positions)
            
            # Só adiciona se for válido
            if new_state.is_valid():
                successors.append(new_state)
        
        return successors
    
    def count_conflicts(self) -> int:
        """
        Conta o número de pares de rainhas que se atacam.
        Esta é a heurística especificada no trabalho.
        
        Retorna:
            Número de pares de rainhas em conflito
        """
        conflicts = 0
        
        # Encontra todas as rainhas posicionadas
        queens = []
        for row in range(self.n):
            if self.positions[row] != -1:
                queens.append((row, self.positions[row]))
        
        # Conta conflitos entre cada par de rainhas
        for i in range(len(queens)):
            for j in range(i + 1, len(queens)):
                r1, c1 = queens[i]
                r2, c2 = queens[j]
                
                # Conflito na mesma coluna
                if c1 == c2:
                    conflicts += 1
                # Conflito na mesma diagonal
                elif abs(r1 - r2) == abs(c1 - c2):
                    conflicts += 1
        
        return conflicts
    
    def count_queens(self) -> int:
        """Conta quantas rainhas já foram posicionadas."""
        return sum(1 for pos in self.positions if pos != -1)
    
    def to_board_string(self) -> str:
        """Converte para representação visual do tabuleiro."""
        board_str = ""
        for row in range(self.n):
            line = "|"
            for col in range(self.n):
                if self.positions[row] == col:
                    line += " Q |"
                else:
                    line += "   |"
            board_str += line + "\n"
            if row < self.n - 1:
                board_str += "+" + "---+" * self.n + "\n"
        return board_str