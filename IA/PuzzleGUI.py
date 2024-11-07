import tkinter as tk
import numpy as np
import random
import time
from PuzzleState import a_star_search, breadth_first_search  # Adicione a busca em largura como alternativa
from queue import PriorityQueue

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8 Puzzle Solver")
        self.board = self.generate_solvable_board()  # Garante um estado inicial solucionável
        self.create_widgets()

        # Chama o método solve_puzzle automaticamente após a criação dos widgets
        self.master.after(1000, self.solve_puzzle)

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                button = tk.Label(self.frame, text=str(self.board[i][j]) if self.board[i][j] != 0 else "",
                                  width=4, height=2, bg="lightgreen", font=("Helvetica", 24))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        self.status_label = tk.Label(self.master, text="", font=("Helvetica", 14))
        self.status_label.grid(row=1, column=0, pady=10)

    def generate_solvable_board(self):
        """ Gera um tabuleiro aleatório que é garantidamente solucionável """
        while True:
            numbers = list(range(9))
            random.shuffle(numbers)
            board = [numbers[i:i+3] for i in range(0, 9, 3)]
            if self.is_solvable(np.array(board)):
                return np.array(board)

    def is_solvable(self, board):
        """ Verifica se o tabuleiro é solucionável """
        flat_board = board.flatten()
        inversions = 0
        for i in range(len(flat_board)):
            for j in range(i + 1, len(flat_board)):
                if flat_board[i] and flat_board[j] and flat_board[i] > flat_board[j]:
                    inversions += 1
        return inversions % 2 == 0

    def update_board(self, board):
        for i in range(3):
            for j in range(3):
                num = board[i][j]
                text = str(num) if num != 0 else ""
                self.buttons[i][j].config(text=text, bg="lightgreen")
        self.frame.update()

    def solve_puzzle(self):
        start_time = time.time()
        if self.is_solvable(self.board):
            # Escolha entre BFS ou A*
            solution, explored_nodes, max_depth = a_star_search(self.board)  # ou breadth_first_search(self.board)

            if solution:
                self.status_label.config(text=f"Solução encontrada em {len(solution) - 1} movimentos!")
                self.show_solution(solution)
                end_time = time.time()
                execution_time = end_time - start_time

                print(f"Tempo de execução: {execution_time:.4f} segundos")
                print(f"Total de nós explorados: {explored_nodes}")
                print(f"Profundidade da árvore: {max_depth}")
                print(f"Número de movimentos: {len(solution) - 1}")
            else:
                self.status_label.config(text="Solução não encontrada.")
        else:
            self.status_label.config(text="Estado inicial não é solucionável.")

    def show_solution(self, solution):
        path = [state.board for state in solution]

        def animate(step=0):
            if step < len(path):
                self.update_board(path[step])
                self.status_label.config(text=f"Passo {step + 1} de {len(path)}")
                self.master.after(500, animate, step + 1)
            else:
                self.status_label.config(text="Solução concluída!")

        animate()

root = tk.Tk()
app = PuzzleGUI(root)
root.mainloop()