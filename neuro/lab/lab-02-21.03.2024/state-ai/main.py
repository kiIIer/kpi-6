from queue import PriorityQueue

import random
import time
import pandas as pd


def shuffle_state(goal_state):
    def swap(state, i, j):
        state = list(state)
        state[i], state[j] = state[j], state[i]
        return tuple(state)

    state = goal_state
    moves = ['U', 'D', 'L', 'R']
    zero_index = state.index(0)
    for _ in range(500):
        row, col = divmod(zero_index, 3)
        move = random.choice(moves)
        if move == 'U' and row > 0:
            state = swap(state, zero_index, zero_index - 3)
            zero_index -= 3
        elif move == 'D' and row < 2:
            state = swap(state, zero_index, zero_index + 3)
            zero_index += 3
        elif move == 'L' and col > 0:
            state = swap(state, zero_index, zero_index - 1)
            zero_index -= 1
        elif move == 'R' and col < 2:
            state = swap(state, zero_index, zero_index + 1)
            zero_index += 1
    return state


def ldfs(initial_state, goal_state, limit):
    start_time = time.time()
    generated_nodes = 0
    max_nodes_in_memory = 0
    path_moves = []

    def is_goal(state):
        return state == goal_state

    def get_children(state):
        nonlocal generated_nodes

        def swap(state, i, j):
            state = list(state)
            state[i], state[j] = state[j], state[i]
            return tuple(state)

        moves = []
        zero_index = state.index(0)
        row, col = divmod(zero_index, 3)

        if row > 0: moves.append(('U', swap(state, zero_index, zero_index - 3)))
        if row < 2: moves.append(('D', swap(state, zero_index, zero_index + 3)))
        if col > 0: moves.append(('L', swap(state, zero_index, zero_index - 1)))
        if col < 2: moves.append(('R', swap(state, zero_index, zero_index + 1)))

        generated_nodes += len(moves)
        return moves

    def dfs(path, moves, depth):
        nonlocal max_nodes_in_memory
        if depth == 0: return None, []
        current_state = path[-1]
        if is_goal(current_state):
            return path, moves
        for move, child in get_children(current_state):
            if child not in path:
                max_nodes_in_memory = max(max_nodes_in_memory, len(path))
                new_path, new_moves = dfs(path + [child], moves + [move], depth - 1)
                if new_path: return new_path, new_moves
        return None, []

    for depth in range(limit + 1):
        path, path_moves = dfs([initial_state], [], depth)
        if path:
            time_taken = time.time() - start_time
            return path, path_moves, time_taken, generated_nodes, max_nodes_in_memory

    time_taken = time.time() - start_time
    return None, [], time_taken, generated_nodes, max_nodes_in_memory


def a_star_solver(initial_state, goal_state):
    start_time = time.time()
    generated_nodes = 0
    max_nodes_in_memory = 0

    def manhattan_distance(state):
        distance = 0
        for i in range(1, 9):
            current_index = state.index(i)
            goal_index = goal_state.index(i)
            current_row, current_col = divmod(current_index, 3)
            goal_row, goal_col = divmod(goal_index, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance

    def get_neighbors(state):
        neighbors = []
        zero_index = state.index(0)
        row, col = divmod(zero_index, 3)

        if row > 0: neighbors.append(('U', do_move(state, 'U')))
        if row < 2: neighbors.append(('D', do_move(state, 'D')))
        if col > 0: neighbors.append(('L', do_move(state, 'L')))
        if col < 2: neighbors.append(('R', do_move(state, 'R')))

        return neighbors

    def do_move(state, direction):
        zero_index = state.index(0)
        row, col = divmod(zero_index, 3)
        if direction == 'U': swap_with = zero_index - 3
        if direction == 'D': swap_with = zero_index + 3
        if direction == 'L': swap_with = zero_index - 1
        if direction == 'R': swap_with = zero_index + 1
        new_state = list(state)
        new_state[zero_index], new_state[swap_with] = new_state[swap_with], new_state[zero_index]
        return tuple(new_state)

    def reconstruct_path(came_from, current):
        total_path = [current]
        moves = []
        while current in came_from:
            next_state, move = came_from[current]
            total_path.append(next_state)
            moves.append(move)
            current = next_state
        total_path.reverse()
        moves.reverse()
        return total_path, moves

    open_set = PriorityQueue()
    open_set.put((manhattan_distance(initial_state), initial_state))
    came_from = {}
    g_score = {initial_state: 0}
    f_score = {initial_state: manhattan_distance(initial_state)}

    while not open_set.empty():
        _, current = open_set.get()
        max_nodes_in_memory = max(max_nodes_in_memory, open_set.qsize())

        if current == goal_state:
            path, moves = reconstruct_path(came_from, current)
            time_taken = time.time() - start_time
            return path, moves, time_taken, generated_nodes, max_nodes_in_memory

        for move, neighbor in get_neighbors(current):
            generated_nodes += 1
            tentative_g_score = g_score.get(current, float('inf')) + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = (current, move)
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor)
                if not any(neighbor == item[1] for item in open_set.queue):
                    open_set.put((f_score[neighbor], neighbor))

    return False, [], time.time() - start_time, generated_nodes, max_nodes_in_memory


def valid_moves(state):
    moves = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)

    if row > 0: moves.append('U')
    if row < 2: moves.append('D')
    if col > 0: moves.append('L')
    if col < 2: moves.append('R')
    return moves


def apply_move(state, move):
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)
    if move == 'U': swap_with = zero_index - 3
    if move == 'D': swap_with = zero_index + 3
    if move == 'L': swap_with = zero_index - 1
    if move == 'R': swap_with = zero_index + 1
    new_state = list(state)
    new_state[zero_index], new_state[swap_with] = new_state[swap_with], new_state[zero_index]
    return tuple(new_state)


def shuffle_puzzle(moves_count=100):
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    state = goal_state
    last_move = None

    for _ in range(moves_count):
        move_options = valid_moves(state)
        if last_move:
            reverse_moves = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
            if reverse_moves[last_move] in move_options:
                move_options.remove(reverse_moves[last_move])
        chosen_move = random.choice(move_options)
        state = apply_move(state, chosen_move)
        last_move = chosen_move

    return state


results = []

N = 100
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
limit = 40

for _ in range(N):
    initial_state = shuffle_state(goal_state)

    ldfs_solution, ldfs_moves, ldfs_time_taken, ldfs_generated_nodes, ldfs_max_nodes_in_memory = ldfs(initial_state, goal_state, limit)

    a_star_solution, a_star_moves, a_star_time_taken, a_star_generated_nodes, a_star_max_nodes_in_memory = a_star_solver(initial_state, goal_state)

    results.append({
        'starting_state': initial_state,
        'solution_moves': ldfs_moves,
        'moves_n': len(ldfs_moves),
        'time_taken': ldfs_time_taken,
        'algorithm': 'LDFS',
        'generated_nodes': ldfs_generated_nodes,
        'max_nodes_in_memory': ldfs_max_nodes_in_memory
    })

    results.append({
        'starting_state': initial_state,
        'solution_moves': a_star_moves,
        'moves_n': len(a_star_moves),
        'time_taken': a_star_time_taken,
        'algorithm': 'A*',
        'generated_nodes': a_star_generated_nodes,
        'max_nodes_in_memory': a_star_max_nodes_in_memory
    })

df_results = pd.DataFrame(results)
df_results.to_excel('results_report_ns.xlsx', index=False)

print(df_results)
