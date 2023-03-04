from board.tile import Tile
from board.pieces import Piece, Pawn, EnpassantRemnant, Knight, Bishop, Rook, Queen, King
from board.chessboard import ChessBoard
from board.color import Black, White
from tests.boards import default_board, testing_board, enpass_real
from board.empty import Empty


def pawn_analysis(board: ChessBoard, tile: str, color: type(Black) | type(White)):
    """
    function to analyze and return possible moves for specified pawn
    :param board: chessboard that is being analyzed
    :param tile: the tile that the pawn is currently on
    :param color: the color moving
    :return: list of tuples (piece_starting, piece_ending, piece_occupying, chessboard, (extra params)),
    chessboard is the board if that move is done
    piece occupying is a type of piece, Pawn, Knight, etc... that will be on that square
    extra params is for castling and en passant where multiple
    """
    promotion_list = [Knight, Bishop, Rook, Queen]
    ret_list = []
    # get the tile in front of it, using the color's associated value
    front_tile = board.convert_tile(tile, 0, color.value(1))
    # if that tile is not occupied
    if board.is_occupied(front_tile) is False:
        # append all of that to the new return list
        ret_list.append((tile, front_tile, Pawn, board.update_board(board.board, tile, front_tile, Pawn)))
        if front_tile[1] == color.pawn_promotion_rank and not board.is_occupied(front_tile):
            for promotion_option in promotion_list:
                # add each promotion option to available moves
                ret_list.append((tile, front_tile, promotion_option, board.update_board(board.board, tile,
                                                                                        front_tile,
                                                                                        promotion_option)))
        # two tiles infront of the pawn in question
        two_infront = board.convert_tile(front_tile, 0, color.value(1))
        # if there is two empty squares (the closest coming from the above if statement) and pawn is on starting rank
        # it is allowed to double jump
        if not board.is_occupied(two_infront) and tile[1] == color.pawn_starting_rank:
            ret_list.append((tile, two_infront, Pawn, board.update_board(board.board, tile, two_infront, Pawn),
                             # append the tile where we will place the enpassant remnant, and the type
                             (front_tile, EnpassantRemnant)))
    # this is the tile in the left most side (white perspective) for either color
    front_left_and_right_tile = [board.convert_tile(tile, 1, color.value(1)), board.convert_tile(tile, -1, color.value(1))]
    # if that tile is occupied, we can take it, so we can add it to return list in a second:
    # for the two tiles infront of the pawn (front left and right)
    for front_tiles in front_left_and_right_tile:
        # if that tile is occupied by an enemy
        if board.pawn_is_occupied_enemy(front_tiles, color.color):
            # if that tile being targeted is the promotion rank for the selected color, we can append each available
            # promotion option to our list
            if front_tiles[1] == color.pawn_promotion_rank:
                for promotion_option in promotion_list:
                    # add each promotion option to available moves
                    ret_list.append((tile, front_tiles,
                                     promotion_option, board.update_board(board.board, tile, front_tiles,
                                                                          promotion_option)))
                    # the extra param passed through is the tile where the current pawn is, and it will be replaced by
                    # Empty
            else:
                # so if the tile is occupied by enemy, we can do that move, with the check for promotion rank failing
                # we just append
                ret_list.append((tile, front_tiles, Pawn, board.update_board(board.board, tile, front_tiles, Pawn,
                                                                             (board.convert_tile(front_tiles, 0,
                                                                                                 color.
                                                                                                 pawn_coming_from()
                                                                                                 ), Empty))))
                # if it not a promotion rank, only a pawn can occupy that square from a pawn move
                # print("added 5")
                # ret_list.append((tile, front_tiles, Pawn, board.update_board(board.board, tile, front_tiles, Pawn)))
    return ret_list




