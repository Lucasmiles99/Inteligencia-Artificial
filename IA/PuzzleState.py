import tkinter as tk
import numpy as np
import time
from queue import Queue  # Corrigir importação
from queue import PriorityQueue
import random

class PuzzleState:
    def __init__(self, board, g=0, previous=None):
        self.board = board
        self.g = g
        self.previous = previous
        self.h = self.calculate_manhattan_distance()  # Para a versão A*.
        self.f = self.g + self.h  # A* f(x) = g(x) + h(x) para a versão Heurística

    def __lt__(self, other):
        return self.f < other.f

    def calculate_manhattan_distance(self):
        distance = 0
        goal_positions = {0: (2, 2), 1: (0, 0), 2: (0, 1), 3: (0, 2),
                          4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1)}
        
        for i in range(3):
            for j in range(3):
                value = self.board[i][j]
                if value != 0:
                    goal_position = goal_positions[value]
                    distance += abs(goal_position[0] - i) + abs(goal_position[1] - j)
        
        return distance

    def is_goal(self):
        return np.array_equal(self.board, np.array([[1, 2, 3], [7, 0, 8], [4, 5, 6]]))

    def generate_successors(self):
        successors = []
        zero_pos = tuple(np.argwhere(self.board == 0)[0])
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_zero_pos = (zero_pos[0] + move[0], zero_pos[1] + move[1])
            if 0 <= new_zero_pos[0] < 3 and 0 <= new_zero_pos[1] < 3:
                new_board = self.board.copy()
                new_board[zero_pos], new_board[new_zero_pos] = new_board[new_zero_pos], new_board[zero_pos]
                successors.append(PuzzleState(new_board, self.g + 1, self))

        return successors

def breadth_first_search(start_board):
    start_state = PuzzleState(start_board)
    frontier = Queue()
    frontier.put(start_state)
    explored = set()
    explored_nodes = 0
    max_depth = 0

    while not frontier.empty():
        current_state = frontier.get()
        explored_nodes += 1

        if current_state.is_goal():
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.previous
            return path[::-1], explored_nodes, max_depth

        explored.add(tuple(map(tuple, current_state.board)))

        for successor in current_state.generate_successors():
            if tuple(map(tuple, successor.board)) not in explored:
                frontier.put(successor)
                max_depth = max(max_depth, successor.g)

    return None, explored_nodes, max_depth

def a_star_search(start_board):
    start_state = PuzzleState(start_board)
    frontier = PriorityQueue()
    frontier.put((start_state.f, start_state))
    explored = set()
    explored_nodes = 0
    max_depth = 0

    while not frontier.empty():
        _, current_state = frontier.get()
        explored_nodes += 1

        if current_state.is_goal():
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.previous
            return path[::-1], explored_nodes, max_depth

        explored.add(tuple(map(tuple, current_state.board)))

        for successor in current_state.generate_successors():
            if tuple(map(tuple, successor.board)) not in explored:
                frontier.put((successor.f, successor))
                max_depth = max(max_depth, successor.g)

    return None, explored_nodes, max_depth