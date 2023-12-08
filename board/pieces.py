from board.color import Black, White
from board.data_structure import Move, DoublePawnMove, Enpassant, Castle


class Piece:
    def __init__(self, color):
        self.color = color

    # def __repr__(self):
    #     return f"starting: {self.starting_tile}"


def diagonal_analysis(board, tile: str, piece):
    color = board.board[tile].color
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
            elif board.is_occupied_enemy(new_tile, color):
                piece_instances.append(Move(tile, new_tile, piece, None))
                break
            elif board.is_occupied(new_tile):
                break
            else:
                piece_instances.append(Move(tile, new_tile, piece, None))
            count += 1
    return piece_instances


def horizontal_analysis(board, tile: str, piece):
    color = board.board[tile].color  # should access White not "white"
    piece_instances = []
    # a var to hold to notation. assumes post-self.fix_notation
    # these are the sets that represent going negative and positive in each direction
    num_sets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    # iterate over each set
    for num in num_sets:
        val_1, val_2 = num[0], num[1]
        while True:
            new_tile = board.convert_tile(tile, val_1, val_2)
            if not new_tile:
                break
            elif board.is_occupied_enemy(new_tile, color):
                piece_instances.append(Move(tile, new_tile, piece, None))
                break
            elif board.is_occupied(new_tile):
                break
            else:
                piece_instances.append(Move(tile, new_tile, piece, None))
            val_1 += num[0]
            val_2 += num[1]
    return piece_instances


def knight_analysis(board, tile):
    color = board.board[tile].color
    tile_list = [(1, 2), (-1, 2), (2, -1), (2, 1), (-2, 1), (-2, -1), (1, -2), (-1, -2)]
    # used to store the list of the knights that are able to make the coordinate move. Usuaully, it is just one,
    # but multiple are used if notation
    possible_moves = []
    # for each of the coordinates:
    for coords in tile_list:
        # create the new tile to query
        new_tile = board.convert_tile(tile, coords[0], coords[1])
        # if the occupant of the tile is a knight, add to knight list
        if not new_tile:
            pass
        else:
            if board.is_occupied(new_tile):
                if board.is_occupied_enemy(new_tile, color):
                    possible_moves.append(Move(tile, new_tile, Knight, None))
            else:
                possible_moves.append(Move(tile, new_tile, Knight, None))
    return possible_moves

def king_analysis(board, tile):
    color = board.board[tile].color
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
            possible_moves.append(Move(tile, new_tile, King, None))
        elif board.is_occupied_enemy(new_tile, color):
            possible_moves.append(Move(tile, new_tile, King, None))
    return possible_moves


class Pawn(Piece):
    # value of piece defined here, this will be used to calculate material later
    value = 1
    # we pass in the color of the piece and what tile it begins on

    def __init__(self, color):
        super().__init__(color)
        self.color = color
        # this turns into: white_pawn or black_pawn
        self.name = f"{color.color}_pawn"

    def __repr__(self):
        return f'{self.color.color}_Pawn'

    @staticmethod
    def analysis(board, tile: str):
        """
        function to analyze and return possible moves for specified pawn
        :param board: chessboard that is being analyzed
        :param tile: the tile that the pawn is currently on
        :return: list of tuples (piece_starting, piece_ending, piece_occupying, (extra params)),
        chessboard is the board if that move is done
        piece occupying is a type of piece, Pawn, Knight, etc... that will be on that square
        extra params is for castling and en passant where multiple
        """
        color = board.board[tile].color
        promotion_list = [Knight, Bishop, Rook, Queen]
        ret_list = []
        # get the tile in front of it, using the color's associated value
        front_tile = board.convert_tile(tile, 0, color.value(1))
        if front_tile is None:
            breakpoint()

        # if that tile is not occupied
        if board.is_occupied(front_tile) is False:
            if front_tile[1] == color.pawn_promotion_rank:
                for promotion_option in promotion_list:
                    # add each promotion option to available moves
                    ret_list.append(Move(tile, front_tile, promotion_option, None))
            else:
                ret_list.append(Move(tile, front_tile, Pawn, None))
            # two tiles infront of the pawn in question
            two_infront = board.convert_tile(front_tile, 0, color.value(1))
            # if it is on the second last rank, two_infront will return none, so we skip that edge case
            if two_infront is None:
                pass
            # if there is two empty squares (the closest coming from the above if statement) and pawn is on starting rank
            # it is allowed to double jump
            elif not board.is_occupied(two_infront) and tile[1] == color.pawn_starting_rank:
                ret_list.append(Move(tile, two_infront, Pawn, Enpassant(front_tile, color, ) ) )
        # this is the tile in the left most side (white perspective) for either color
        front_left_and_right_tile = [board.convert_tile(tile, 1, color.value(1)),
                                     board.convert_tile(tile, -1, color.value(1))]
        # if that tile is occupied, we can take it, so we can add it to return list in a second:
        # for the two tiles infront of the pawn (front left and right)
        for front_tiles in front_left_and_right_tile:
            if front_tiles is None:
                # if the tile does not exist, skip past it
                continue
            # if that tile is occupied by an enemy
            if board.pawn_is_occupied_enemy(front_tiles, color):
                # if that tile being targeted is the promotion rank for the selected color, we can append each available
                # promotion option to our list
                if front_tiles[1] == color.pawn_promotion_rank:
                    for promotion_option in promotion_list:
                        # add each promotion option to available moves
                        ret_list.append(Move(tile, front_tiles, promotion_option, None))
                        # the extra param passed through is the tile where the current pawn is, and it will be replaced by
                        # Empty
                else:
                    # so if the tile is occupied by enemy, we can do that move, with the check for promotion rank failing
                    # we just append
                    ret_list.append(Move(tile, front_tiles, Pawn, None))
        return ret_list

    @staticmethod
    # this method is required for all classes to follow polymorphism, and to show that where a pawn can move != tiles it
    # attacks. A pawn will always attack the two tiles to its front side
    def tiles_attacking(board, tile):
        # positive or negative 1, depending on color
        color_val = board.board[tile].color.value(1)
        # the two tiles infront of the pawn
        front_1, front_2 = board.convert_tile(tile, color_val, +1), board.convert_tile(tile, color_val, -1)
        # return all tiles that are valid
        return [(tile, new_tile, Pawn) for new_tile in (front_1, front_2) if new_tile is not None]


class EnpassantRemnant:  # does not inherit from 'Piece', because it is logically not a piece, and to distinguish from
    # normal pieces

    # purpose of this class is to leave this behind in the square that was jumped over during a double jump pawn move
    # it must have special properties to not have it block sightlines for other pieces, but be visible to pawns
    # it must also decay one move after being placed
    value = 1  # value = 1 cause it is a pawn capture...
    # decay of all enpassant remnants will be reduced by 1 each turn, and will be removed if it == 0
    # one is removed on said turn i believe, so 2 should make sense
    decay = 2  
    def __init__(self, color):
        self.color = color
        self.name = f"{color.color}_en"

    def __repr__(self):
        return f'{self.color}_enpassant'


    @staticmethod
    def analysis(_board, _tile):
        # this is just to appease board_calculations in get_specific_value
        return []

    @staticmethod
    # i think this is probably better than making an if/else clause inside the things that call this
    def tiles_attacking(_board, _tile):
        return []

class Rook(Piece):
    value = 5

    def __init__(self, color):
        super().__init__(color)
        self.color = color
        self.name = f"{color.color}_rook"

    def __repr__(self):
        return f'{self.color.color}_Rook'

    @staticmethod
    def analysis(board, tile: str):
        return horizontal_analysis(board, tile, Rook)

    @staticmethod
    def tiles_attacking(board, tile):
        return horizontal_analysis(board, tile, Rook)


class Bishop(Piece):
    value = 3

    def __init__(self, color):
        super().__init__(color)
        self.color = color
        self.name = f"{color.color}_bishop"

    def __repr__(self):
        return f'{self.color.color}_Bishop'

    @staticmethod
    def analysis(board, tile: str):
        return diagonal_analysis(board, tile, Bishop)

    @staticmethod
    def tiles_attacking(board, tile):
        return diagonal_analysis(board, tile, Bishop)


class Knight(Piece):
    value = 3

    def __init__(self, color):
        super().__init__(color)
        self.color = color
        self.name = f"{color.color}_knight"

    def __repr__(self):
        return f'{self.color.color}_Knight'

    @staticmethod
    def analysis(board, tile: str):
        return knight_analysis(board, tile)

    @staticmethod
    def tiles_attacking(board, tile):
        return knight_analysis(board, tile)


class Queen(Piece):
    value = 9

    def __init__(self, color):
        super().__init__(color)
        self.color = color
        self.name = f"{color.color}_queen"

    def __repr__(self):
        return f'{self.color.color}_Queen'

    @staticmethod
    def analysis(board, tile: str):
        return horizontal_analysis(board, tile, Queen) + diagonal_analysis(board, tile, Queen)

    @staticmethod
    def tiles_attacking(board, tile):
        return horizontal_analysis(board, tile, Queen) + diagonal_analysis(board, tile, Queen)


class King(Piece):
    value = 100  # does 100 make sense? Worth more than everything on the board

    def __init__(self, color):
        super().__init__(color)
        self.color = color
        self.name = f"{color.color}_king"

    def __repr__(self):
        return f'{self.color.color}_king'

    @staticmethod
    def analysis(board, tile: str):
        return king_analysis(board, tile)

    @staticmethod
    def tiles_attacking(board, tile):
        return king_analysis(board, tile)
