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


def bishop_analysis(board: ChessBoard, tile: str, color: type(Black) | type(White)):
    # this bit unironically copy and pasted from chessboard.py's bishop_search
    operators = [("+", "+"), ("+", "-"), ("-", "+"), ("-", "-")]
    # will contain list of available moves where the bishop could have moved from
    piece_instances = []
    # for each pair of operators:
    for operator_pair in operators:
        # count represents going just one square at a time
        count = 1
        # loop over each option of a diagonal (a1, b2, c3, d4...)
        while True:
            # create the x and y of the tile to pass to convert_tile (e.g. -1, +1 or +3, +3)
            increment_number_1 = int(operator_pair[0] + str(count))
            increment_number_2 = int(operator_pair[1] + str(count))
            # convert the numbers into a tile, relative to starting tile
            new_tile = board.convert_tile(tile, increment_number_1, increment_number_2)
            # if the tile is occupied by bishop or queen, append to list, and break. As more bishops have no impact
            if new_tile is None:
                break
            elif board.is_occupied_enemy(new_tile, color.color):
                piece_instances.append(new_tile)
                break
            elif board.is_occupied(new_tile):
                break
            else:
                piece_instances.append(new_tile)
            count += 1
    return piece_instances


def knight_analysis(board: ChessBoard, tile: str, color: type(Black) | type(White)):
    tile_list = [(1, 2), (-1, 2), (2, -1), (2, 1), (-2, 1), (-2, -1), (1, -2), (-1, -2)]
    # used to store the list of the knights that are able to make the coordinate move. Usuaully, it is just one,
    # but multiple are used if notation
    piece_instances = []
    # for each of the coordinates:
    for coords in tile_list:
        # create the new tile to query
        new_tile = board.convert_tile(tile, coords[0], coords[1])
        # if the occupant of the tile is a knight, add to knight list
        if not new_tile:
            pass
        else:
            if board.is_occupied(new_tile):
                if board.is_occupied_enemy(new_tile, color.color):
                    piece_instances.append(new_tile)
            else:
                piece_instances.append(new_tile)
    return piece_instances


def rook_analysis(board: ChessBoard, tile: str, color: type(Black) | type(White)):
    piece_instances = []
    # a var to hold to notation. assumes post-self.fix_notation
    # these are the sets that represent going negative and positive in each direction
    num_sets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    # iterate over each set
    for num in num_sets:
        val_1, val_2 = num[0], num[1]
        while True:
            new_tile = board.convert_tile(tile, val_1, val_2)
            print(new_tile)
            if not new_tile:
                break
            elif board.is_occupied_enemy(new_tile, color.color):
                piece_instances.append(new_tile)
                break
            elif board.is_occupied(new_tile):
                break
            else:
                piece_instances.append(new_tile)
            val_1 += num[0]
            val_2 += num[1]
    return piece_instances


def queen_analysis(board: ChessBoard, tile: str, color: type(Black) | type(White)):
    return rook_analysis(board, tile, color) + bishop_analysis(board, tile, color)


def king_analysis(board: ChessBoard, tile: str, color: type(Black) | type(White)):
    # possible coordinate spots from the king
    spots = [(0, 1), (0, -1), (1, 0), (1, -1), (1, 1), (-1, 0), (-1, 1), (-1, -1)]
    possible_moves = []
    # iterate over them
    for coords in spots:
        new_tile = board.convert_tile(tile, coords[0], coords[1])
        if not new_tile:
            continue
        # if the tile being checked is empty:
        if not board.is_occupied(new_tile):
            possible_moves.append(new_tile)
        elif board.is_occupied_enemy(new_tile, color.color):
            possible_moves.append(new_tile)
    return possible_moves
