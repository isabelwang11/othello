import sys

class Strategy():
    def best_strategy(self, board, player, best_move, still_running):
        globalize(board, player)
        k = 1
        while k < 15:
            max, index = ab_pruning(k)
            if index != None:
                best_move.value = index
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
                      0, 150, -30,  20,   5,   5,  20, -30, 150,   0,
                      0, -30, -50,  -5,  -5,  -5,  -5, -50, -30,   0,
                      0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
                      0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
                      0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
                      0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
                      0, -30, -50,  -5,  -5,  -5,  -5, -50, -30,   0,
                      0, 150, -30,  20,   5,   5,  20, -30, 150,   0,
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

def ab_pruning(k): # PRUNING
    lm = legal_moves(board, player)
    if len(lm) == 0:
        num_b, num_w = num_pieces(board)
        return num_b+num_w, None
    return maximize(board, k, float("-inf"), float("inf"), player, other_player) # calls minimax with alpha-beta parameters

def maximize(state, depth, alpha, beta, token, other_token):
    if depth == 0 or game_over(state):
        return score(state), None
    max, max_index = float("-inf"), None
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
    min, min_index = float("inf"), None
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
    num_player, num_opponent = 0, 0
    for pc in state:
        if pc == player:
            num_player += 1
        elif pc == other_player:
            num_opponent += 1
    return num_player, num_opponent

def score(state): # CHANGES
    num_p, num_o = num_pieces(state)
    if num_p+num_o < 20: # when there are less than 20 pieces on the board, return score from mobility heuristic
        return mobility(state)
    elif num_p+num_o < 60: # when there are between 20 and 59 pieces on the board, return score from stability/position heuristic
        return position(state)
    else: # when there are 60 or more pieces on the board, return score from victory heuristic
        return victory(num_p, num_o)

def mobility(state):
    # actual mobility
    # num_ply_legal_moves = len(legal_moves(state, player))
    # num_opp_legal_moves = len(legal_moves(state, other_player))
    # return num_ply_legal_moves - num_opp_legal_moves
    # potential mobility
    num_ply_empty_spaces, num_opp_empty_spaces = 0, 0
    for i in range(100):
        ply_next_to_empty_space, opp_next_to_empty_space = False, False
        # if state[i] == ".": # delete this line?
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

def victory(num_p, num_o):
    return num_p - num_o

def IDDFS(board, val, token):
    globalize(board, token)
    k = 1
    while k <= val:
        max, index = ab_pruning(k)
        if index != None:
            print(index)
        # print("MAX VAL: %s, INDEX: %s" % (str(max), str(index)))
        k += 1

IDDFS(sys.argv[1], 100, sys.argv[2])