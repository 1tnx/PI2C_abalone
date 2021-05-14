import time
import copy

board_weight = [
            [1, 2, 3, 2, 1, 0, 0, 0, 0],
            [1, 2, 3, 3, 2, 1, 0, 0, 0],
            [1, 2, 3, 4, 3, 2, 1, 0, 0],
            [1, 2, 3, 4, 4, 3, 2, 1, 0],
            [1, 2, 3, 4, 5, 4, 3, 2, 1],
            [0, 1, 2, 3, 4, 4, 3, 2, 1],
            [0, 0, 1, 2, 3, 4, 3, 2, 1],
            [0, 0, 0, 1, 2, 3, 3, 2, 1],
            [0, 0, 0, 0, 1, 2, 3, 2, 1]
]

directions = {
    "NE": [-1, 0],
    "E": [0, 1],
    "SE": [1, 1],
    "SW": [1, 0],
    "W": [0, -1],
    "NW": [-1, -1]
}

def possible_moves(board, player_color):
    """
    return a list of all possible moves a player can and pass it to legal_moves()
    """
    moves = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == player_color:
                for d in directions:
                    direction = directions[d]
                    next_marble = [a + b for a, b in zip([i, j], direction)]
                    if next_marble[0] in range(9) and next_marble[1] in range(9):
                        next_marble_value = board[next_marble[0]][next_marble[1]]
                        if next_marble_value == "E" or next_marble_value == switch_player(player_color):
                            moves.append({"marbles": [[i, j]], "direction": d})
                            # find a double marble move
                            second_marble = [a - b for a, b in zip([i, j], direction)]
                            if second_marble[0] in range(9) and second_marble[1] in range(9):
                                second_marble_value = board[second_marble[0]][second_marble[1]]
                                if second_marble_value == player_color:
                                    moves.append({"marbles": [[i, j], second_marble], "direction": d})
                            # find a triple marble move
                            third_marble = [a - b for a, b in zip(second_marble, direction)]
                            if third_marble[0] in range(9) and third_marble[1] in range(9):
                                third_marble_value = board[third_marble[0]][third_marble[1]]
                                if third_marble_value == player_color and second_marble_value == player_color:
                                    moves.append({"marbles": [[i, j], second_marble, third_marble], "direction": d})
    return legal_moves(board, moves, player_color)

def legal_moves(board, moves, player_color):
    """
    return a list all legal moves and pass it so sort_moves()
    """
    legal_moves_list = []
    opponent_color = switch_player(player_color)
    for move in moves:
        next_marble = [a + b for a, b in zip(move["marbles"][0], directions[move["direction"]])]
        second_next_marble = [a + b for a, b in zip(next_marble, directions[move["direction"]])]
        third_next_marble = [a + b for a, b in zip(second_next_marble, directions[move["direction"]])]
        if len(move["marbles"]) == 1:
            if next_marble[0] in range(9) and next_marble[1] in range(9):
                if (board[next_marble[0]][next_marble[1]] != player_color and
                    board[next_marble[0]][next_marble[1]] != opponent_color):
                    legal_moves_list.append(move)
        if len(move["marbles"]) == 2:
            if next_marble[0] in range(9) and next_marble[1] in range(9):
                if second_next_marble[0] in range(9) and second_next_marble[1] in range(9):
                    if (board[second_next_marble[0]][second_next_marble[1]] != player_color and
                        board[second_next_marble[0]][second_next_marble[1]] != opponent_color):
                        legal_moves_list.append(move)
                elif second_next_marble[0] not in range(9) or second_next_marble[1] not in range(9):
                    legal_moves_list.append(move)
        if len(move["marbles"]) == 3:
            if next_marble[0] in range(9) and next_marble[1] in range(9):
                if second_next_marble[0] in range(9) and second_next_marble[1] in range(9):
                    if third_next_marble[0] in range(9) and third_next_marble[1] in range(9):
                        if (board[second_next_marble[0]][second_next_marble[1]] != player_color and
                            board[second_next_marble[0]][second_next_marble[1]] != opponent_color and
                            board[third_next_marble[0]][third_next_marble[1]] != player_color and
                            board[third_next_marble[0]][third_next_marble[1]] != opponent_color):
                            legal_moves_list.append(move)
                    elif third_next_marble[0] not in range(9) or third_next_marble[1] not in range(9):
                        if board[second_next_marble[0]][second_next_marble[1]] != player_color:
                            legal_moves_list.append(move)
                elif second_next_marble[0] not in range(9) or second_next_marble[1] not in range(9):
                    legal_moves_list.append(move)
    return sort_moves(board, legal_moves_list, player_color)

def sort_moves(board, moves, player_color):
    """
    sort moves in the following order: 1. push opponent outside the board 2. push opponent to the borders 3. move marbles to the center
    """
    sorted_moves = []
    # return kill moves in priority
    for move in moves:
        next_marble = [a + b for a, b in zip(move["marbles"][0], directions[move["direction"]])]
        if board[next_marble[0]][next_marble[1]] == switch_player(player_color):
            marbles_to_add = [elem * len(move["marbles"]) for elem in directions[move["direction"]]]
            marble_after_opponent = [a + b for a, b in zip(move["marbles"][0], marbles_to_add)]
            if marble_after_opponent[0] not in range(9) or marble_after_opponent[1] not in range(9):
                return [move]
            elif board[marble_after_opponent[0]][marble_after_opponent[1]] == "X":
                return [move]
    # moves that push ennemy marbles to the borders
    for move in moves:
        current_opponent_weight = compute_weight(board, switch_player(player_color))
        new_board = apply(board, move, player_color)
        new_opponent_weight = compute_weight(new_board, switch_player(player_color))
        if new_opponent_weight < current_opponent_weight:
            move["weight"] = (current_opponent_weight - new_opponent_weight)*10
            sorted_moves.append(move)
    # try to move marbles to the center
    for move in moves:
        current_weight_sum = 0
        new_weight_sum = 0
        for marble in move["marbles"]:
            current_marble_weight = board_weight[marble[0]][marble[1]]
            current_weight_sum += current_marble_weight
        new_marble_list = new_marbles_position(move)
        for marble in new_marble_list:
            new_marble_weight = board_weight[marble[0]][marble[1]]
            new_weight_sum += new_marble_weight
        if new_weight_sum > current_weight_sum:
            move["weight"] = new_weight_sum
            sorted_moves.append(move)

    sorted_moves.sort(key=lambda move: move["weight"], reverse=True)
    # if there are still no moves, append any move
    if len(sorted_moves) == 0:
        sorted_moves.append(moves)
    # return only the 15 best moves or the negamax will take too much time to compute each move (3s timeout)
    return sorted_moves[:15]

def compute_weight(board, player_color):
    """
    compute the total weight of a players
    """
    weight_sum = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] == player_color:
                marble_weight = board_weight[i][j]
                weight_sum += marble_weight
    return weight_sum

def game_winner(board, player_color):
    """
    returns the game winner if the game is over
    """
    player_count = 0
    opponent_count = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] == player_color:
                player_count += 1
            elif board[i][j] == switch_player(player_color):
                opponent_count += 1
    if player_count == 8:
        return switch_player(player_color)
    elif opponent_count == 8:
        return player_color
    else:
        return None

def game_over(board, player_color):
    """
    returns True/False if the game is finished or not
    """
    if game_winner(board, player_color) is not None:
        return True
    else:
        return False

def new_marbles_position(move):
    """
    returns the list of marbles after the move is applied
    """
    new_list = []
    direction = directions[move["direction"]]
    for marble in move["marbles"]:
        new_marble = [a + b for a, b in zip(marble, direction)]
        new_list.append(new_marble)
    return new_list

def apply(board, move, player):
    """
    applies the move to the board and return the new board state
    """
    res = copy.deepcopy(board)
    new_marbles = new_marbles_position(move)
    for marble in new_marbles:
        res[marble[0]][marble[1]] = player
    if len(move["marbles"]) == 1:
        res[move["marbles"][0][0]][move["marbles"][0][1]] = "E"
    if len(move["marbles"]) > 1:
        if len(move["marbles"][1]) >= 2:
            res[move["marbles"][1][0]][move["marbles"][1][1]] = "E"
        if len(move["marbles"][1]) == 3:
            res[move["marbles"][2][0]][move["marbles"][2][1]] = "E"
    return res

def switch_player(player):
    """
    return the opponent's color
    """
    if player == "B":
        return "W"
    else:
        return "B"

def marble_difference(board, player):
    """
    compute the difference of marbles between 2 players
    """
    player_count = 0
    opponent_count = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] == player:
                player_count += 1
            elif board[i][j] == switch_player(player):
                opponent_count += 1
    if player_count > opponent_count:
        return player_count - opponent_count
    elif player_count < opponent_count:
        return player_count - opponent_count
    else:
        return 0

def heuristic(board, player):
    """
    compute the utiliy of a final state
    """
    if game_over(board, player):
        winner = game_winner(board, player)
        if winner is None:
            return 0
        elif winner == player:
            return 9
        else:
            return -9
    res = marble_difference(board, player)
    return res

def negamax(board, player, depth=4, alpha=float('-inf'), beta=float('inf')):
    """
    negamax algorithm with alpha-beta pruning and a depth of 4
    """
    if game_over(board, player) or depth == 0:
        return -heuristic(board, player), None

    the_value, the_move = float('-inf'), None
    for move in possible_moves(board, player):
        successor = apply(board, move, player)
        value, _ = negamax(successor, switch_player(player),  depth-1, -beta, -alpha)
        if value > the_value:
            the_value, the_move = value, move
        alpha = max(alpha, the_value)
        if alpha >= beta:
            break
    return -the_value, the_move

def timeit(fun):
    """
    compute the time a function takes to execute
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        res = fun(*args, **kwargs)
        print("-- Move executed in {}s:".format(time.time() - start))
        return res
    return wrapper

@timeit
def run(board, player_color):
    """
    launch the search for the best move
    """
    _, move = negamax(board, player_color)
    return move
