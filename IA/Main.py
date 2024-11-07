from PuzzleState import a_star_search, PuzzleState
import numpy as np
import random

def generate_random_board():
    # Gera uma configuração aleatória válida para o Puzzle-8
    board = list(range(9))  # Cria uma lista de números de 0 a 8
    random.shuffle(board)  # Embaralha a lista para obter um estado aleatório
    board = np.array(board).reshape(3, 3)  # Converte para um array 3x3
    return board

if __name__ == "__main__":
    print("Bem-vindo ao Puzzle-8!")
    
    # Gera um estado inicial aleatório
    initial_board = generate_random_board()
    
    # Exibe o tabuleiro inicial aleatório
    print("Tabuleiro inicial aleatório:")
    for row in initial_board:
        print(row)
    
    # Executa o algoritmo A* para resolver o puzzle
    solution = a_star_search(initial_board)
    
    if solution:
        print("Caminho da solução encontrado:")
        path = []
        while solution:
            path.append(solution.board)
            solution = solution.previous
        path.reverse()
        for step in path:
            print(step)
            print("-----")
    else:
        print("Solução não encontrada.")