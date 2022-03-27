from random import randint

def globalize(state):
    global board
    board = state
    global directions
    directions = [-11, -10, -9, -1, 1, 9, 10, 11]

def display(state):
    for i in range(10):
        for j in range(10):
            print(state[i*10+j], end=' ')
        print()
    print()

def possible_moves(state, token):
    moves = set()
    indices = [i for i in range(100) if state[i] == token]
    for index in indices:
        for dir in directions:
            temp = index + dir
            while state[temp] != "." and state[temp] != token and state[temp] != "?":
                temp += dir
            if abs(temp-index) > abs(dir) and state[temp] == ".": #check if it's not next to same token
                moves.add(temp)
    return sorted(list(moves))

def move(state, token, pos):
    state = state[:pos] + token + state[pos + 1:]
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

def num_pieces(state):
    num_black, num_white = 0, 0
    for pc in state:
        if pc == "@":
            num_black += 1
        elif pc == "o":
            num_white += 1
    return num_black, num_white

def game_over(state):
    if len(possible_moves(state, "@")) > 0 or len(possible_moves(state, "o")) > 0:
        for i in range(100):
            if state[i] == ".":
                return False
    return True

def play_game(state, token, moves):
    display(state)
    num_black, num_white = num_pieces(state)
    if game_over(state):
        return state, num_black, num_white, moves
    print("Black: %s" % str(num_black))
    print("White: %s" % str(num_white))
    if token == "@":
        color = "Black"
        next_token = "o"
    else:
        color = "White"
        next_token = "@"
    possible = possible_moves(state, token)
    print("%s Possible Moves: %s" % (color, str(possible)))
    if len(possible) > 0:
        chosen = possible[randint(0, len(possible)-1)]
        moves.append(chosen)
        print("Choose %s" % str(chosen))
        state = move(state, token, chosen)
        state, num_black, num_white, moves = play_game(state, next_token, moves)
    else:
        moves.append(-1)
        print("%s passes" % color)
        state, num_black, num_white, moves = play_game(state, next_token, moves)
    return state, num_black, num_white, moves

def run_game(token):
    final_state, num_black, num_white, move_order = play_game(board, token, [])
    print("Black: %s" % str(num_black))
    print("White: %s" % str(num_white))
    display(final_state)
    print("Percent Black: %s" % str(num_black / 64))
    print("Percent White: %s" % str(num_white / 64))
    print(move_order)


globalize("???????????........??........??........??...o@...??...@o...??........??........??........???????????")
run_game("@")