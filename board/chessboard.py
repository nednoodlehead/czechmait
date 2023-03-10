# purpose of this file is to take in a chessboard as data, and analyze the position
import tests.boards
from image import export
from board.empty import Empty
from board.pieces import Piece, EnpassantRemnant, Pawn, Bishop, Knight, Rook, Queen, King
from tests.boards import enpass, default_board, enpass_real, testing_board
from board.color import Black, White


class ChessBoard:
    score = 0
    missing_pieces_black = []
    missing_pieces_white = []
    # tiles that have an enpassant remnant on them
    enpassant_tile = []

    def __init__(self, board=default_board):
        self.board = board

    def is_occupied(self, tile):
        # if the passed in tile is any type that inherits 'Piece', this does not cover en passant remnants
        if isinstance(self.board[tile], Piece):
            return True
        else:
            return False

    # export the current board to a png
    def export_png(self):
        export.hashmap_to_png(self.board)

    @staticmethod
    def handle_enpassant_remnant(board):
        """
        function to reduce all enpassant remnant 'decay' values by 1 and check if it is 0. If it is 0, remove remnant
        modifies self.board

        This should eventually be overhauled into Chessboard.board being its own type with associated piece counts &
        en passant lists, so this can be more effecient by first checking if there are any enpassant remnants. Because
        the average board doesn't have it, so there is a lot of redundant calculation. should work anyway
        """
        for tile, piece in board.items():
            if isinstance(piece, EnpassantRemnant):
                # remove one from decay
                piece.decay -= 1
                # if decay is at 0, we can remove the remnant
                if piece.decay == 0:
                    board[tile] = Empty()
        return board

    # used to see nearby tiles through calculations
    @staticmethod
    def convert_tile(tile, amount_letter, amount_number):
        """Takes in a tile, a and returns tile with new amounts added
            :param (str) tile: the tile notation to convert
            :param (int) amount_letter: amount to 'add' to the letter
            :param (int) amount_number: amount to add to the number

        :returns tile with the added amounts
        (h2, -2, 3) -> f5
        """
        # divide the tile into the letter and number separately
        org_let, org_num = tile[0], int(tile[1])
        # if the result of adding letters either goes above 104 (h) or lower than 97 (a), return None
        if amount_letter + ord(org_let) > 104 or amount_letter + ord(org_let) < 97:
            return None  # in this case, the given numbers are incorrect, but we just return none, like rust err-handlin
        # if the results of adding org number go above 8 or below 1, raise error
        if amount_number + org_num > 8 or amount_number + org_num < 1:
            return None
        # convert the letter -> ord number, add the desired amount, convert back, add new number to it
        return f"{chr(ord(org_let) + amount_letter)}{org_num + amount_number}"

    def is_occupied_enemy(self, tile, color):
        """
        Returns a bool based on if the given tile is occupied by opposite color. Does not include enpassant remnant
        :param tile: Tile, tile to inspect (tile class)
        :param color: str, either white or black, the color of the player querying
        :returns bool: is it occupied by enemy piece? aka, can it be taken?
        """
        if color == Black:
            # check that it is of color white, and it is not an enpassant remnant
            if self.board[tile].color == White and isinstance(self.board[tile], Piece):
                return True
            else:
                return False
        else:
            if self.board[tile].color == Black and isinstance(self.board[tile], Piece):
                return True
            else:
                return False

    def pawn_is_occupied_enemy(self, tile, color):
        """
        returns a bool based on if the given tile is of any enemy type, including enpassant remnants
        :param tile: str, tile to inspect
        :param color: White or Black, color of the current turn
        :return: bool (it is occupied by enemy or not)
        """
        if color == Black:
            if self.board[tile].color == White:
                return True
            else:
                return False
        else:
            if self.board[tile].color == Black:
                return True
            else:
                return False


    def get_tile(self, tile):
        """Returns the desired tile instance from given input
        :param tile (str) tile instance being requested
        """
        for key in self.board.keys():
            if key.tile == tile:
                return key

    # purpose of this function is to remove the unnessisary parts of the notation. All of these should be implied and
    # understood by the bot in different ways than explict notation
    @staticmethod
    def fix_notation(notation):
        new_str = ""
        for letter in notation:
            if letter in "+#x":
                pass
            else:
                new_str += letter
        return new_str

    def pawn_search(self, notation, turn: Black | White, taking):
        letter_map = {
            "Q": Queen,
            "N": Knight,
            "B": Bishop,
            "R": Rook
        }
        if "=" in notation:
            # find the index of where "=" is inside the notation
            equals_index = notation.index("=")
            # the return type will be denoted by the next letter, so what pawn promotes into
            return_type = letter_map[notation[equals_index + 1]]
            # adjust notation so rest of function works as expected and nothing else needs this portion so...
            notation = notation[:-2]
        else:
            return_type = Pawn
        # if there is an x in the notation
        if taking:  # cxb5
            new_tile = notation[2:]
            # if it is white, mark the tile above and on the first-letter file
            start_tile = notation[0] + str(int(notation[-1]) - 1)
            # if the tile that is being taken has no piece, an espassant occured
            if not self.is_occupied(new_tile):
                # if en passant is occuring, we return the tile being caputured, but also the update for the tile
                # that the piece dies on, which for white is -1 on numbers, -0 on letters
                # it will be parsed later that this extra arguement will set that tile to empty
                # turn.pawn_coming_from() tells us which direction (-1 for white, 1+ for black) the pawn is coming from
                # this is needed to make the extra args define Empty to the correct tile
                return (start_tile, new_tile, return_type), (self.convert_tile(new_tile, 0, turn.pawn_coming_from()), Empty)
                # represents the only tile on the board that a pawn could take a white piece on this square
            return start_tile, new_tile, return_type
        # there is no taking notation, it is a pawn move. e.g. b3
        else:
            # if the position below the notation is empty, the pawn did a double jump, so starting pos -> 4th
            if isinstance(self.get_tile(f"{notation[0]}{str(int(notation[1]) + turn.value(1))}"), Empty):
                # pawn did do a double jump:
                return notation[0] + str(int(notation[1]) - turn.value(2)), notation, return_type
            else:
                # pawn did not do a double jump
                return notation[0] + str(int(notation[1]) - turn.value(1)), notation, return_type

    def rook_search(self, notation, turn, piece):
        # check for the edge case that the notation is 5 long, and it is like: Rd5b5. so d5 -> b5
        if len(notation) == 5:
            return notation[1:3], notation[3:5], piece
        # this will be a list of all piece types that can move to that square
        piece_instances = []
        # a var to hold to notation. assumes post-self.fix_notation
        base_tile = notation[-2:]
        # these are the sets that represent going negative and positive in each direction
        num_sets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        # iterate over each set
        for num in num_sets:
            # pass into function that will do the calculation
            search = self.vert_hori_search(base_tile, piece, turn, num[0], num[1])
            if search is not None:
                # if it does not return None, append it to piece instances
                piece_instances.append(search)

        if len(piece_instances) == 1:
            return piece_instances[0], base_tile, piece
        else:
            for tile in piece_instances:
                if notation[1] in tile:
                    return tile, base_tile, piece

    def vert_hori_search(self, tile, piece, turn, amount_1, amount_2):
        # loop:
        while True:
            # define tile as the converted tile, while also passing an instance of itself in
            # this is important so the numbers passed in actually change.
            tile = self.convert_tile(tile, amount_1, amount_2)
            # if the tile is None, aka: hit edge of board, break loop for that direction
            if tile is None:
                break
            # if it is an instance of the desired piece (Rook or Queen)
            if isinstance(self.board[tile], piece):
                # if it is the color of the playing turn
                if self.board[tile].color == turn:
                    # return the tile
                    return tile
                # break if it reaches an enemy queen or rook (is instance of one, not same color)
                break
            # if the tile is occupied by a piece (and it is not one of the desired pieces, stop querying)
            if self.is_occupied(tile):
                break
        # return None if nothing is found
        return None

    def knight_search(self, notation, turn):
        tile_list = [(1, 2), (-1, 2), (2, -1), (2, 1), (-2, 1), (-2, -1), (1, -2), (-1, -2)]
        # used to store the list of the knights that are able to make the coordinate move. Usuaully, it is just one,
        # but multiple are used if notation
        nearby_knights = []
        # for each of the coordinates:
        for coords in tile_list:
            # convert the tile on notation with the coordniates into the tile object
            tile = self.get_tile(notation[-2:]).convert_tile(coords[0], coords[1])
            # if the occupant of the tile is a knight, add to knight list
            if tile:
                if isinstance(self.board[tile], Knight):
                    # if the color of the knight matches the current move (white to play)
                    if self.board[tile].color == turn:
                        nearby_knights.append(tile)
        if len(nearby_knights) == 0:
            raise ValueError("Invalid notation given with current board")
        if len(notation) == 3:  # case: Ne3
            # return the only available knight's square that can go there, and the notation telling which square
            # it is being moved to. There should also only be one item in nearby_knights
            return nearby_knights[0], notation[-2:], Knight
        # case where notation denotes that the second char is unique (letter or number). It
        elif len(notation) == 4:  # case Nde3 (b file knights goes to e3)
            # unique is the character that uniquely identifies the original square
            unique = notation[1]
            for item in nearby_knights:
                if unique in item:
                    return item, notation[-2:], Knight
        elif len(notation) == 5:
            return notation[1:3], notation[3:5], Knight  # (e.g. N3d4)

    def bishop_search(self, notation, turn, piece):
        """
                :param notation: "Be3". Must be parsed by fix_notation first
                :param piece: either Queen or Bishop
                :param turn: "black" or "white"
                :return: either None (No valid pieces found) or "<tile> <tile>": "b3", "a2"
        """
        operators = [("+", "+"), ("+", "-"), ("-", "+"), ("-", "-")]
        # will contain list of available moves where the bishop could have moved from
        bishop_tiles = []
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
                new_tile = self.convert_tile(notation[-2:], increment_number_1, increment_number_2)
                # if the tile is occupied by bishop or queen, append to list, and break. As more bishops have no impact
                if new_tile is None:
                    break
                elif isinstance(self.board[new_tile], piece):
                    if self.board[new_tile].color == turn:
                        bishop_tiles.append(new_tile)
                        break
                elif self.is_occupied(new_tile):
                    break
                # if the tile is non-existant (None) or is occupied by a piece, break the loop
                # add to the count!
                count += 1
        # this is guarding for the edge case that there are multiple bishops that can move to required square
        # in case where two bishops are able to move there:
        if len(notation) == 3:
            # case where the Queen type is querying, and it does not find anything
            if len(bishop_tiles) == 0:
                # return empty list as it will not matter, because later it will add lists together
                return [], notation[-2:], piece
            else:
                # if the list isn't empty, return the tile the piece is on, notation, and instance of piece
                return bishop_tiles[0], notation[-2:], piece
        # in case where there is a unique char as the first index, we can use that to determine which bishop is in
        # the notation
        if len(notation) == 4:
            for bishop in bishop_tiles:
                if notation[1] in bishop:
                    return bishop, notation[-2:], piece
        # if the length of the notation is greater than 4, then the 1st and 2nd chars are the first tile,
        # and 3rd and 4th are the ending notation. "Be3d2"
        if len(notation) > 4:
            return notation[1:3], notation[3:5], piece

    def king_search(self, notation, turn):
        # possible coordinate spots from the king
        spots = [(0, 1), (0, -1), (1, 0), (1, -1), (1, 1), (-1, 0), (-1, 1), (-1, -1)]
        # iterate over them
        for coords in spots:
            # make the new tile
            new_tile = self.convert_tile(notation[-2:], coords[0], coords[1])
            # if the tile contains a King type, return it. Impossible for a King to be there
            # that is an opposite color. Because then king could take king
            if isinstance(self.board[new_tile], King):
                return notation[-2:], new_tile, King

    def queen_search(self, notation, turn):
        bishop_results = self.bishop_search(notation, turn, Queen)
        rook_results = self.rook_search(notation, turn, Queen)
        if bishop_results is None:
            return rook_results
        else:
            return bishop_results

    @staticmethod
    def pawn_diff(tile_1, tile_2):
        """
        checks if the pawn did a double jump, needed for deciding to leave en passant remnant
        :return:
        """
        if int(tile_1[1]) - int(tile_2[1]) not in [-1, 1]:
            return True
        else:
            return False

    @staticmethod
    def handle_casting(notation, turn):
        if len(notation) == 3:
            if turn == Black:
                # black short castle:
                return "e8", "g8", King, ("h8", "f8", Rook)
            else:
                # white short castle:
                return "e1", "g1", King, ("h1", "f1", Rook)
        else:
            if turn == Black:
                # black long castle
                return "e8", "c8", King, ("a8", "d8", Rook)
            else:
                # white long castle
                return "e1", "c1", King, ("ai", "d1", Rook)

    def notation_translation(self, notation, turn):
        """
        :param notation: the notation for the move
        :param turn: who's turn is it? "white" or "black"
        :return: a tuple, (starting_square, ending_square) representing the notation
        """
        if "0" in notation or "O" in notation:
            return self.handle_casting(notation, turn)
        # if "x" is in the notation, we turn taking to true, so we can parse a bit easier
        taking = True if "x" in notation else False
        # ensure that turn is a correct param
        if turn not in [Black, White]:
            raise ValueError(f"Incorrect turn given :: {turn}")
        # if the first letter is not a capital, it is a pawn move. e.g. b5 or h3
        if ord(notation[0]) > 90 or ord(notation[0]) < 65:
            return self.pawn_search(notation, turn, taking)
        # knight  (Kb5 or Kge5(knight from g file to e5))
        elif notation[0] == "N":
            notation = self.fix_notation(notation)
            return self.knight_search(notation, turn)
        elif notation[0] == "B":  # bishop
            # would be a much easier notation if promoting to bishop wasn't a thing
            # parse the extras from notation out
            notation = self.fix_notation(notation)
            return self.bishop_search(notation, turn, Bishop)
        elif notation[0] == "R":  # rook
            notation = self.fix_notation(notation)
            return self.rook_search(notation, turn, Rook)
        elif notation[0] == "Q":  # queen
            notation = self.fix_notation(notation)
            return self.queen_search(notation, turn)
        else:  # in the instance of a king move ...
            notation = self.fix_notation(notation)
            return self.king_search(notation, turn)

    def update_board(self, board, tile_old, tile_new, type_piece, extra=None):
        """
        interface to update self.board with tile piece starts on, and tile it ends on
        :param board: chessboard.board type to modify. dict of Tile() and Piece() types
        :param tile_old: tile that the given piece begins on. Will become 'Empty()'
        :param tile_new: tile that the given piece moves to. Will inherit the instance of tile_old
        :param type_piece: check is done so if type_piece != piece instance, a pawn promotion has occured, and a new
                           piece is created on that tile
       :param extra: extra params passed in. Used for castling and en passant, as they affect multiple tiles. Passed in
       as tuple
        :returns modified board type
        """
        # calls the enpassant checker, will handle the enpassant remnants
        board = self.handle_enpassant_remnant(board)
        if extra is not None:
            # if a castle occurs:
            if len(extra) == 3:
                # move the king to the new location
                board[tile_new] = board[tile_old]
                # move the rook to the new location
                board[extra[1]] = board[extra[0]]
                # set the rook's old position to empty()
                board[extra[0]] = Empty()
                # set the king's position to empty()
                board[tile_old] = Empty()
            # in case of en passant
            else:
                # piece that is being removed, if empty, nothing is being removed
                # the piece that is moving:
                moving_piece = board[tile_old]
                # setting the old piece's tile as empty
                board[tile_old] = Empty()
                # making the new tile = the piece that is moving
                board[tile_new] = moving_piece
                # if the tile is not occupied by 'Empty', add that piece that is being taken to piece_list
                if not isinstance(board[tile_new], Empty):
                    if board[tile_new].color == Black:
                        self.missing_pieces_black.append(board[tile_new])
                    else:
                        self.missing_pieces_white.append(board[tile_new])
        else:
            if isinstance(type_piece, Pawn) and self.pawn_diff(tile_old, tile_new):
                # copy the new square with the old square (occupant)
                board[tile_new] = board[tile_old]
                board[tile_old] = Empty()
                if board[tile_new].color == Black:
                    color_and_value = -1, "black"
                else:
                    color_and_value = +1, "white"
                board[self.convert_tile(tile_old, 0, color_and_value[0])] = EnpassantRemnant(color_and_value[1])

            # if the type of the square before is not the same as what it will be after, a pawn promotion has occured
            # and, we will create a new instance of that type on the new
            if not isinstance(board[tile_old], type_piece):
                # we will make a new instance of that type, passing in the color, and the starting tile
                new_piece = type_piece(board[tile_old].color, tile_new)
            else:
                new_piece = board[tile_old]
            # setting the old piece's tile as empty
            board[tile_old] = Empty()
            # making the new tile = the piece that is moving
            board[tile_new] = new_piece
            # do we need a way to keep track of pieces off the board?
        return board


chs = ChessBoard(testing_board)
x = chs.notation_translation("Raxb5", Black)
print(x)
