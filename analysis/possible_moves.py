from board.tile import Tile
from board.pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from board.chessboard import ChessBoard
from board.color import Black, White


def pawn_analysis(board: ChessBoard, tile: str, color: Black | White):
    """
    function to analyze and return possible moves for specified pawn
    :param board: chessboard that is being analyzed
    :param tile: the tile that the pawn is currently on
    :param color: the color moving
    :return: list of tuples (notation, chessboard), chessboard is the board if that move is done
    """
    ret_list = []
    # get the tile in front of it, using the color's associated value
    front_tile = board.convert_tile(tile, color.value, 0)
    # if that tile is not occupied
    if not board.is_occupied(front_tile):
        # update the board with that new tile
        board.update_board(tile, front_tile, Pawn)
        # append all of that to the new return list
        ret_list.append((front_tile, board.board))
    # this is the tile in the left most side (white perspective) for either color
    front_left_tile = board.convert_tile(tile, color.value, -1)
    # if that tile is occupied, we can take it
    if board.is_occupied_enemy(front_left_tile, color.color):


