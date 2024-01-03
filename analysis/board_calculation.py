# here we calculate the value of the board, which color is favoured, mate in x moves...
from board.chessboard import ChessBoard
from board.pieces import Pawn, EnpassantRemnant, Knight, Bishop, Rook, Queen, King
from board.empty import Empty
from board.color import Black, White
from tests.boards import testing_board
import copy
from board.data_structure import CheckMate

def evaluate_positional_board(board: ChessBoard, turn: type(White) | Black) -> float:
    # is used to determine who has a better position. So if white has more material, but black has more active pieces,
    # this will try to show that inbalance
    black_val, white_val = 0, 0
    for tile, piece in board.board.items():
        if isinstance(piece, Empty) or isinstance(piece, EnpassantRemnant):
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


def evaluate_material(board: ChessBoard) -> int:
    white_val, black_val = 0, 0
    for piece in board.board.values():
        # ignore the kings in the quick eval
        # if isinstance(piece, King):
            # continue
        if piece.color == White:
            white_val += piece.value
        elif piece.color == Black:
            black_val += piece.value
        else:
            pass
    return white_val - black_val

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


def is_checkmated(board: ChessBoard, color) -> bool:
    if len(board.all_possible_moves(board, color)) == 0:    
        return True
    return False




def minmaxroot(depth: int, board: ChessBoard, color, maximizing: bool):
    bestmove = -9999
    secondbest = -9999
    thirdbest = -9999
    bestmovefinal = None
    for possible_move in board.all_possible_moves(board, color):
        print(f'possible: {possible_move}')
        board.update_board(board, possible_move)
        value = minmax_2(depth, board, not maximizing, color)
        board.undo_move()
        if isinstance(value, CheckMate):
            print("FOUNDER")
            print(value > bestmove)
        if value > bestmove:
            print("Best score: " ,bestmove)
            print("Best move: ",bestmovefinal)
            print("Second best: ", secondbest)
            thirdbest = secondbest
            secondbest = bestmove
            bestmove = value
            bestmovefinal = possible_move
        else:
            print(f'{value} is not larger than {bestmove}')
    return bestmovefinal
        

def minmax_2(depth, board, is_maximizing, color):
    if depth == 0:
        return evaluate_material(board)
    if is_checkmated(board, color.opposite_color):
        print("FOUND")
        return CheckMate(is_maximizing, depth)
    else:
        print(f'{color.opposite_color} is not in checkmate')
        if isinstance(board.board["f7"], Queen):
            board.export_png("not mate", True)
            print("MATED")
            print(is_checkmated(board, Black))
    if is_maximizing:
        bestmove = -9999
        for possible_move in board.all_possible_moves(board, color):
            board.update_board(board, possible_move)
            val = minmax_2(depth -1, board, False, color.opposite_color)
            # print(f'val-max: {val}')
            if val > bestmove:
                bestmove = val
            board.undo_move()
        return bestmove
    else:
        bestmove = 9999
        for possible_move in board.all_possible_moves(board, color):
            board.update_board(board, possible_move)
            val = minmax_2(depth -1, board, False, color.opposite_color)
            # print(f'val-min: {val}')
            if val < bestmove:
                bestmove = val
            board.undo_move()
        return bestmove
