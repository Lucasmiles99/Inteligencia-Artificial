import random
from collections import deque

# Função para gerar um estado inicial aleatório
def generate_initial_state():
    numbers = list(range(1, 9)) + [0]  # Gera uma Lista de 1 a 9 sendo 0 representação do espaço vazio
    random.shuffle(numbers)
    return [numbers[i:i + 3] for i in range(0, 9, 3)]

# Função para encontrar a posição do espaço vazio (0)
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Função para verificar se o estado atual é o estado final
def is_goal(state):
    return state == [[1, 2, 3], [4, 0, 5], [6, 7, 8 ]]

# Função para gerar os estados sucessores
def get_successors(state):
    successors = []
    blank_x, blank_y = find_blank(state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cima, Baixo, Esquerda, Direita

    for dx, dy in directions:
        new_x, new_y = blank_x + dx, blank_y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [row[:] for row in state]
            new_state[blank_x][blank_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[blank_x][blank_y]
            successors.append(new_state)

    return successors

# Função para realizar a busca em largura
def bfs(initial_state):
    queue = deque([(initial_state, [])]) #Cria uma Fila que armazenará o estado inicial
    visited = set()
    visited.add(tuple(map(tuple, initial_state)))

    while queue:
        state, path = queue.popleft()

        if is_goal(state):
            return path

        for successor in get_successors(state):
            state_tuple = tuple(map(tuple, successor))
            if state_tuple not in visited:
                visited.add(state_tuple)
                queue.append((successor, path + [successor]))# Adicionar Solução à fila se não houver um já adicionado

    return None  # Se não encontrar solução

# Gera um estado inicial e tenta resolvê-lo
initial_state = generate_initial_state()
print("Estado inicial:")
for row in initial_state:
    print(row)

solution = bfs(initial_state)

if solution:
    print("\nSolução encontrada com", len(solution), "movimentos:")
    for step in solution:
        for row in step:
            print(row)
        print()
else:
    print("Não foi possível encontrar uma solução.")