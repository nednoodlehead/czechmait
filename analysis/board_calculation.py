# here we calculate the value of the board, which color is favoured, mate in x moves...
from board.chessboard import ChessBoard
from board.pieces import Pawn, EnpassantRemnant, Knight, Bishop, Rook, Queen, King
from board.empty import Empty
from board.color import Black, White
from tests.boards import testing_board
import copy


def evaluate_positional_board(board: ChessBoard, turn: type(White) | Black) -> float:
    # is used to determine who has a better position. So if white has more material, but black has more active pieces,
    # this will try to show that inbalance
    black_val, white_val = 0, 0
    for tile, piece in board.board.items():
        if isinstance(piece, Empty):
            # if the tile is empty, no need to evaluate it
            continue
        if piece.color == Black:
            black_val += get_specific_value(board, tile)
        else:
            white_val += get_specific_value(board, tile)
    # we will return white / black, negative value favors black, positive favors white
    return white_val / black_val
    # todo might want to have material value included, it is fairly important. also who's turn it is matters a lot
    # todo also need to work around checks. perhaps return a bool that signals if enemy is in check
    # todo perhaps dividing the white_val by black_val is beneficial, so it is a lower number and can be added to
    # todo material count


def get_board_value(board: ChessBoard, turn: type(White) | type(Black)) -> float:
    positional_value = evaluate_positional_board(board, turn)
    raw_value = evaluate_material(board)
    return float((raw_value[0] - raw_value[1])) + positional_value


def get_specific_value(board, tile):
    """
    will return specific value of specified piece, this depends on various information about the piece, how many tiles
    it affects, if it is preventing the (enemy) king from moving
    :param board: Chessboard to analyze
    :param tile: tile where the piece is
    :return: float (value of piece)
    """
    piece, color = board.board[tile], board.board[tile].color
    tiles_reached = piece.analysis(board, tile)
    value_board = generate_tile_values(board, color)
    value = 0
    for new_tile in tiles_reached:
        value += value_board[new_tile[0]]
    return value


def generate_tile_values(board: ChessBoard, color: type(Black) | type(White)) -> dict:
    """
    function to generate value-board showing which tiles are "worth" more in terms of occupying.
    :param color: which color is asking. The tiles around enemy king are more valuable than nearby ones
    :param board: board to analyze
    :return: board with all occupying pieces replaced with numbers. These numbers are the values that the square holds
    these are mostly based on king proximity and past-pawn opportunities
    """
    # start top left, go clockwise. letter_increment, number_increment
    inner_ring = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
    outter_ring = [(-2, 2), (-1, -2), (0, -2), (1, -2), (2, -2), (2, 1), (2, 0), (2, -1), (2, -2), (1, -2), (0, -2),
                   (-1, -2), (-2, -2), (-2, -1), (-2, 0), (-2, 1)]
    # make new dict, each
    value_board = {value: 0.5 for value in board.board}
    # controlling center of board is usually important i think. idk im 700 elo
    value_board["d4"] = 5
    value_board["d5"] = 5
    value_board["e4"] = 5
    value_board["e5"] = 5
    value_board["d3"] = 4.5
    value_board["e3"] = 4.5
    value_board["c4"] = 4.5
    value_board["c5"] = 4.5
    value_board["d6"] = 4.5
    value_board["e6"] = 4.5
    value_board["f5"] = 4.5
    value_board["f4"] = 4.5
    # check if each tile is near a king. tiles near the enemy king will be given a higher value
    # you don't win by defending you win by attacking
    for tile, value in board.board.items():
        if isinstance(value, King):
            if board.board[tile].color == color:
                # if the king is the same color as the color being passed in, it is less important to control our king
                color_vals = (3, 2)
                value_board[tile] += 7
            else:
                # higher value for enemy king
                color_vals = (10, 8)
                value_board[tile] += 15
                # for each tile in the inner ring of the king, add
            for letter_inc, number_inc in inner_ring:
                new_tile = board.convert_tile(tile, letter_inc, number_inc)
                # if the tile is invalid / doesn't exist
                if not new_tile:
                    continue
                # if the tile does exist, give it a value of 3. it is important to control tiles near king
                else:
                    value_board[new_tile] += color_vals[0]
            for letter_inc, number_inc in outter_ring:
                new_tile = board.convert_tile(tile, letter_inc, number_inc)
                if not new_tile:
                    pass
                # give a value of 2 :)
                else:
                    value_board[new_tile] += color_vals[1]
    return value_board


def evaluate_material(board: ChessBoard) -> (int, int):
    white_val, black_val = 0, 0
    for piece in board.board.values():
        # ignore the kings in the quick eval
        if isinstance(piece, King):
            continue
        if piece.color == White:
            white_val += piece.value
        elif piece.color == Black:
            black_val += piece.value
        else:
            pass
    return white_val, black_val


def is_in_check(board: ChessBoard, color):
    # color = color that we are checking is in check. So: is_in_check(White) == White is in check
    king_tile = find_king(board, color)  # could be passed in to save resources perhaps
    # we pass in the opposite color of the color that we need to check for check. so white's check depends on black's
    # pieces and what they see
    attacked_tiles = board.all_attacking_tiles(board, color.opposite_color)
    # we need to anticipate that there may be an enpassantremnant, so we unpack like this:
    for tile in attacked_tiles:
        if tile[1] == king_tile:
            return True
    else:
        return False


def find_king(board, color):
    for tile, piece in board.board.items():
        if isinstance(piece, King):
            if piece.color == color:
                return tile


def find_checkmate(board: ChessBoard, color):
    mate_line = []
    for possible_move in board.all_possible_moves(board, color):
        old_tile, new_tile, type_piece, *extra = possible_move
        org_board = copy.deepcopy(board)
        theory_board = org_board.update_board(org_board, old_tile, new_tile, type_piece, extra)
        if is_in_check(theory_board, color.opposite_color):
            if not leave_check(theory_board, color.opposite_color):
                print(f'checkmate: {type_piece} to {new_tile}')
            else:
                print(f'moving {type_piece} to {new_tile} puts the {color.opposite_color.color} in check')


def find_best_moves_recursive(board: ChessBoard, color: type(White) | type(Black), total_depth, minimax: bool):
    # perhaps a second, different function for looking for checkmates? and perhaps combine them at some point
    # will be returned, shows the moves required for mate. only appended to when mate is confirmed
    mate_line = []
    # list containing the chessboards for current move
    temp_line = []
    def search(temp_board, temp_color, minimax_val: int):
        boards = []
        for possible_move in temp_board.all_possible_moves(temp_board, temp_color):
            old_tile, new_tile, type_piece, *extra = possible_move
            org_board = copy.deepcopy(temp_board)
            # store in hashmap containing notation as key, sorted(boards, key=lambda: get_board_value(hashmap.values())?
            theory_board = org_board.update_board(org_board, old_tile, new_tile, type_piece, extra)
            board_val = get_board_value(theory_board, temp_color)
            boards.append((board_val, theory_board))
        # organize the boards from lowest to highest (based on the value of board)
        boards = sorted(boards, key=lambda x: x[0])
        return boards[minimax_val]
    # current depth
    cur_depth = 0
    # temp board, needed to make changes to the boards
    temp_board = copy.deepcopy(board)
    # our minimax value. 0 = maximizing. -1 minimizing. represents the index in sorted list
    mini_or_max = 0 if minimax else 1
    while cur_depth < total_depth:
        mini_or_max = 1 if mini_or_max == 0 else 0
        temp_board = search(temp_board, color, mini_or_max)
        temp_line.append(temp_board)


        # switching
        color = color.opposite_color
        cur_depth += 1
    return temp_line


def minimax(board, depth, color, maximizing):
    # covering end-recursion cases
    if depth <= 0:
        return get_board_value(board, color)
    elif is_checkmated(board, color):
        return f'{color.color} has been checkmated!'
    elif is_checkmated(board, color.opposite_color):
        return f'{color.opposite_color.color} has been checkmated!'

    if maximizing:
        maxeval = -1000.0
        for possible_moves in board.all_possible_moves(board, color):
            old_tile, new_tile, type_piece, *extra = possible_moves
            brd = copy.deepcopy(board)
            theory_board = brd.update_board(brd, old_tile, new_tile, type_piece, extra)
            new_color = color.opposite_color
            board_eval = minimax(theory_board, depth - 1, new_color, False)  # Adjust the depth for each recursive call
            maxeval = max(maxeval, board_eval)
        return maxeval
    else:
        mineval = +1000.0
        for possible_moves in board.all_possible_moves(board, color):
            old_tile, new_tile, type_piece, *extra = possible_moves
            brd = copy.deepcopy(board)
            theory_board = brd.update_board(brd, old_tile, new_tile, type_piece, extra)
            new_color = color.opposite_color
            board_eval = minimax(theory_board, depth - 1, new_color, True)  # Adjust the depth for each recursive call
            mineval = min(mineval, board_eval)
        return mineval


def slow_checker(board: ChessBoard, depth, color, maximizing):
    # end cases:
    if depth == 0:
        return board, get_board_value(board, color), []
    elif is_checkmated(board, color):
        return f'{color.color} has been checkmated!'  # not a comprehensive checkmate check btw
    elif is_checkmated(board, color.opposite_color):
        return f'{color.opposite_color.color} has been checkmated!'
    # will return top 3 best moves

    if maximizing:
        max_eval = -1000.0
        moves = []
        for possible_moves in board.all_possible_moves(board, color):
            old_tile, new_tile, type_piece, *extra = possible_moves
            board = board.update_board(board, old_tile, new_tile, type_piece, extra)
            _, eval_score, _ = slow_checker(board, depth - 1, color.opposite_color, False)
            eval_score = get_board_value(board, color)
            if eval_score > max_eval:
                max_eval = eval_score
                moves = [(board, eval_score)]
            else:
                moves.append((board, eval_score))
            board.undo_move()
        return board, max_eval, moves

    else:
        min_eval = 10000.0
        moves = []
        for possible_moves in board.all_possible_moves(board, color):
            old_tile, new_tile, type_piece, *extra = possible_moves
            board = board.update_board(board, old_tile, new_tile, type_piece, extra)
            _, eval_score, _ = slow_checker(board, depth - 1, color.opposite_color, True)
            eval_score = get_board_value(board, color)
            if eval_score < min_eval:
                min_eval = eval_score
                moves = [(board, eval_score)]
            else:
                moves.append((board, eval_score))
            board.undo_move()
        return board, min_eval, moves



def three_move_cont(board: ChessBoard, three_moves, depth, color):
    # takes in a list that contains the three best moves, this function will get the best move for each player
    # in the sense of possible (and best) continuation
    for top_three in three_moves:
        val, old_tile_top, new_tile_top, type_piece_top, *extra = top_three
        local_depth = 0
        best_continuation = []
        local_board_copy = copy.deepcopy(board)
        local_board = local_board_copy.update_board(local_board_copy, old_tile_top, new_tile_top, type_piece_top, extra)
        maximizing = True  # maybe inherit from function signature?
        while local_depth != depth:
            moves = []
            print(f'ALL POSSIBLE: {board.all_possible_moves(local_board, color)}')
            for possible_moves in board.all_possible_moves(local_board, color):
                old_tile, new_tile, type_piece, *extra = possible_moves
                temp_board = copy.deepcopy(local_board)
                temp_board.update_board(temp_board, old_tile, new_tile, type_piece, extra)
                # breakpoint()
                val = get_board_value(temp_board, color)
                moves.append((val, old_tile, new_tile, type_piece, extra))
            best_continuation.append(sorted(moves, key=lambda board_val: board_val[0])[0])
            print(f'at depth={local_depth} maximizing={maximizing} and color={color}')
            local_depth += 1
            maximizing = False if maximizing else True
            color = color.opposite_color
            local_board.update_board(local_board, best_continuation[-1][1], best_continuation[-1][2], best_continuation[-1][3], best_continuation[-1][4])
        print(f'best cont: {best_continuation}')
        for item in best_continuation:
            print(f'{color.color} moves {item[3]} from {item[1]} to {item[2]}')
            color = color.opposite_color


def create_minimax_struct(board: ChessBoard, color, depth=5):
    best_move = -9999
    local_board = copy.deepcopy(board)
    for possible_moves in board.all_possible_moves(local_board, color):
        old_tile, new_tile, type_piece, *extra = possible_moves
        value = max(best_move, minimax())







def is_checkmated(board, color) -> bool:
    if is_in_check(board, color) and not leave_check(board, color):
        return True
    else:
        return False




def leave_check(board: ChessBoard, color: type(White) | type(Black)):
    # given color will return valid moves that result in not being in check anymore
    valid_moves = []
    possible_moves = board.all_possible_moves(board, color)
    for move in possible_moves:
        old_tile, new_tile, type_piece, *extra = move
        org_board = copy.deepcopy(board.board)
        chs = ChessBoard(org_board)
        theory_board = chs.update_board(chs, old_tile, new_tile, type_piece, extra)
        if not is_in_check(theory_board, color):
            valid_moves.append((old_tile, new_tile, type_piece, extra))
    return valid_moves
