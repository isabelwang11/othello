import random
import time

class Strategy():
    def best_strategy(self, board, player, best_move, still_running):
        globalize(board, player)
        k = 1
        while k < 15:
            max, best_move.value = ab_pruning(k)
            k += 1

def globalize(state, p):
    global directions
    directions = [-11, -10, -9, -1, 1, 9, 10, 11]
    global board
    board = state
    global player
    player = p
    global other_player
    other_player = "o" if player == "@" else "@"
    global weight_matrix
    weight_matrix = [ 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                      0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
                      0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
                      0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
                      0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
                      0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
                      0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
                      0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
                      0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
                      0,   0,   0,   0,   0,   0,   0,   0,   0,   0]

def display(state):
    for i in range(10):
        for j in range(10):
            print(state[i*10+j], end=' ')
        print()
    print()

def legal_moves(state, token):
    moves = set()
    indices = [i for i in range(100) if state[i] == token]
    for index in indices:
        for dir in directions:
            temp = index + dir
            while state[temp] != "." and state[temp] != token and state[temp] != "?":
                temp += dir
            if abs(temp-index) > abs(dir) and state[temp] == ".": # check if it's not next to same token
                moves.add(temp)
    return sorted(list(moves))

def move(state, token, pos):
    state = state[:pos] + token + state[pos+1:]
    for dir in directions:
        flips = []
        temp = pos + dir
        while state[temp] != "." and state[temp] != token and state[temp] != "?":
            flips.append(temp)
            temp += dir
        if state[temp] == token:
            for index in flips:
                state = state[:index] + token + state[index+1:]
    return state

def game_over(state):
    if len(legal_moves(state, "@")) > 0 or len(legal_moves(state, "o")) > 0:
        for i in range(100):
            if state[i] == ".":
                return False
    return True

def ab_pruning(k):
    lm = legal_moves(board, player)
    if len(lm) == 0:
        num_b, num_w = num_pieces(board)
        return num_b+num_w, None
    return maximize(board, k, float("-inf"), float("inf"), player, other_player)

def maximize(state, depth, alpha, beta, token, other_token):
    if depth == 0 or game_over(state):
        return score(state), None
    max, max_index = float("-inf"), -1
    for m in legal_moves(state, token):
        new_state = move(state, token, m)
        min, min_index = minimize(new_state, depth-1, alpha, beta, other_token, token)
        if min != float("+inf") and min > max:
            max, max_index = min, m
        if max > alpha:
            alpha = max
        if alpha >= beta:
            return max, max_index
    return max, max_index

def minimize(state, depth, alpha, beta, token, other_token):
    if depth == 0 or game_over(state):
        return score(state), None
    min, min_index = float("inf"), -1
    for m in legal_moves(state, token):
        new_state = move(state, token, m)
        max, max_index = maximize(new_state, depth-1, alpha, beta, other_token, token)
        if max != float("-inf") and max < min:
            min, min_index = max, m
        if min < beta:
            beta = min
        if alpha >= beta:
            return min, min_index
    return min, min_index

def num_pieces(state):
    num_black, num_white = 0, 0
    for pc in state:
        if pc == "@":
            num_black += 1
        elif pc == "o":
            num_white += 1
    return num_black, num_white

def score(state):
    num_b, num_w = num_pieces(state)
    if num_b+num_w < 18: # change number?
        return mobility(state)
    else:
        return position(state)

def mobility(state):
    # actual mobility
    # num_ply_legal_moves = len(legal_moves(state, player))
    # num_opp_legal_moves = len(legal_moves(state, other_player))
    # return 100 * (num_ply_legal_moves - num_opp_legal_moves) / (num_ply_legal_moves + num_opp_legal_moves)
    # potential mobility
    num_ply_empty_spaces, num_opp_empty_spaces = 0, 0
    for i in range(100):
        ply_next_to_empty_space, opp_next_to_empty_space = False, False
        for dir in directions:
            if i+dir >= 0 and i+dir < 100:
                if state[i+dir] == player:
                    ply_next_to_empty_space = True
                elif state[i+dir] == other_player:
                    opp_next_to_empty_space = True
        if ply_next_to_empty_space:
            num_ply_empty_spaces += 1
        if opp_next_to_empty_space:
            num_opp_empty_spaces += 1
    return num_opp_empty_spaces - num_ply_empty_spaces

def position(state):
    score = 0
    for i in range(100):
        if state[i] == player:
            score += weight_matrix[i]
        elif state[i] == other_player:
            score -= weight_matrix[i]
    return score


def IDDFS(board, val, token):
    globalize(board, token)
    k = 1
    while k <= val:
        max, index = ab_pruning(k)
        print(index)
        # print("MAX VAL: %s, INDEX: %s" % (str(max), str(index)))
        k += 1

# IDDFS("???????????........??........??..o@....??..@@@...??...@o...??........??........??........???????????", 10, "o")