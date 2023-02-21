# purpose of this file is to take in a chessboard as data, and analyze the position
from image import export
from empty.empty import Empty

class Tile:
    # creates the tile type
    def __init__(self, tile):
        self.tile = tile

    # used to see nearby tiles through calculations
    def convert_tile(self, amount_letter, amount_number):
        """Takes in a tile, a and returns tile with new amounts added
            :param (int) amount_letter: amount to 'add' to the letter
            :param (int) amount_number: amount to add to the number
        :returns tile with the added amounts
        (h2, -2, 3) -> f5
        """
        # divide the tile into the letter and number separately
        org_let, org_num = self.tile[0], int(self.tile[1])
        # if the result of adding letters either goes above 104 (h) or lower than 97 (a), return None
        if amount_letter + ord(org_let) > 104 or amount_letter + ord(org_let) < 97:
            return None  # in this case, the given numbers are incorrect, but we just return none, like rust err-handlin
        # if the results of adding org number go above 8 or below 1, raise error
        if amount_number + org_num > 8 or amount_number + org_num < 1:
            return None
        # convert the letter -> ord number, add the desired amount, convert back, add new number to it
        return f"{chr(ord(org_let) + amount_letter)}{org_num + amount_number}"

    # used for having a class instance be used as a hash key
    def __hash__(self):
        return hash(self.tile)

    # used mainly in the hashmap so accessing key "a4" will give you Tile("a4")
    def __eq__(self, other):
        return self.tile == other

    # used for calling Tile[0] to access the letter or number in the tile id
    def __getitem__(self, item):
        return self.tile[item]

    # used for printing & debuggin
    def __repr__(self):
        return f"{self.tile}"



class ChessBoard:
    score = 0

    def __init__(self, board=None):
        self.board = board if board is not None else default_board

    def is_occupied(self, tile):
        # is the passed in tile an instance of "Empty" (empty chess slot)
        if isinstance(self.board[tile], Empty):
            return False
        else:
            return True

    # export the current board to a png
    def export_png(self):
        export.hashmap_to_png(self.board)

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
        Returns a bool based on if the given tile is occupied by opposite color
        :param tile: Tile, tile to inspect (tile class)
        :param color: str, either white or black, the color of the player querying
        :returns bool: is it occupied by enemy piece? aka, can it be taken?
        """
        if color.lower() == "black":
            if self.board[tile].color == "white":
                return True
            else:
                return False
        elif color.lower() == "white":
            if self.board[tile].color == "black":
                return True
            else:
                return False
        else:
            raise ValueError(f"Did not input black or white :: {color}")

    def get_color(self, tile):
        """
        Returns either 'black', 'white' or none depending on the occupant of the tile
        :param tile: tile to be queried (e.g. "b3")
        """
        if self.board[tile].color not in ["black", "white"]:
            return None
        else:
            return self.board[tile].color

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

    def pawn_search(self, notation, turn, taking):
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
            if turn == "white":
                # represents the only tile on the board that a pawn could take a white piece on this square
                start_tile = notation[0] + str(int(notation[-1]) - 1)
                return start_tile, new_tile, return_type
            # if the color is black (all other cases were removed on the valueError above
            else:
                start_tile = notation[0] + str(int(notation[-1]) + 1)
            return start_tile, new_tile, return_type
        # there is no taking notation, it is a pawn move. e.g. b3
        else:
            if turn == "white":
                # if the position below the notation is empty, the pawn did a double jump, so starting pos -> 4th
                if isinstance(self.get_tile(f"{notation[0]}{str(int(notation[1]) - 1)}"), Empty):
                    # pawn did do a double jump:
                    return notation[0] + str(int(notation[1]) - 2), notation, return_type
                else:
                    # pawn did not do a double jump
                    return notation[0] + str(int(notation[1]) - 1), notation, return_type
            # if it is blacks turn
            else:
                # if the position above the notation is empty, the pawn did a double jump, so starting pos -> 5th
                if isinstance(self.get_tile(f"{notation[0]}{str(int(notation[1]) + 1)}"), Empty):
                    # the pawn did do a double jump
                    return notation[0] + str(int(notation[1]) + 2), notation, return_type
                else:
                    # the pawn did not do a double jump
                    return notation[0] + str(int(notation[1]) + 1), notation, return_type

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
        print(f"bishop: {bishop_results}")
        print(f'rook: {rook_results}')
        if bishop_results is None:
            return rook_results
        else:
            return bishop_results


    def notation_translation(self, notation, turn):
        """
        :param notation: the notation for the move
        :param turn: who's turn is it? "white" or "black"
        :return: a tuple, (starting_square, ending_square) representing the notation
        """
        # if "x" is in the notation, we turn taking to true, so we can parse a bit easier
        taking = True if "x" in notation else False
        # ensure that turn is a correct param
        if turn not in ["black", "white"]:
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

    def update_board(self, tile_old, tile_new, type_piece):
        """
        interface to update the board with tile piece starts on, and tile it ends on
        :param tile_old: tile that the given piece begins on. Will become 'Empty()'
        :param tile_new: tile that the given piece moves to. Will inherit the instance of tile_old
        :param type_piece: check is done so if type_piece != piece instance, a pawn promotion has occured, and a new
                           piece is created on that tile
        Modifies self.board
        """

    def move_piece(self, notation):
        pass


class Piece:

    def __init__(self, color, starting_tile):
        self.color = color
        self.starting_tile = starting_tile

    def on_starting_tile(self, tile: Tile):
        """ Returns a bool depending on the current tile vs original starting tile"""
        if tile.tile == self.starting_tile:
            return True
        return False


class Pawn(Piece):
    # value of piece defined here, this will be used to calculate material later
    value = 1
    # we pass in the color of the piece and what tile it begins on

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)
        self.color = color
        self.name = f"{color}_pawn"
        self.starting_tile = starting_tile

    def available_moves(self, tile: Tile, board: ChessBoard):  # returns a move notation list e.g. [a4, xb3]
        # tile = b3, h5
        # board = hashmap to represent the entire board
        # (black) if is on x7, can move two ahead
        # if it is not, it may move one ahead
        # rember to do ENPASSANT ?
        # if the tile to its front left or right is occupied by opposite color piece, it is able to take
        available = []
        # if the color is black
        if self.color == "black":
            # and it is on its default rank
            if tile == self.starting_tile:
                # if the letter position two ahead of it is unoccupied, you can move there
                print(board.is_occupied("f5"))
                if not board.is_occupied(f"{tile[0]}5"):
                    # add to available moves list
                    available.append(f"{tile[0]}5")
                    available.append(f"{tile[0]}6")
            # if the given tile is not on the seventh rank
            else:
                # if the tile infront of it is unoccupied, you can move there
                if not board.is_occupied(f"{tile[0]}{int(tile[1] -1)}"):
                    available.append(f"{tile[0]}{int(tile[1] -1)}")
            # if there is an opposite colored piece that is on its diagonals
            if board.is_occupied_enemy(tile.convert_tile(1, -1), self.color):
                available.append(f"{tile[0]}x{tile.convert_tile(1, -1)}")
            if board.is_occupied_enemy(tile.convert_tile(1, 1), self.color):
                available.append(f"{tile[0]}x{tile.convert_tile(1, 1)}")
        return available


class Rook(Piece):
    value = 5

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)
        self.color = color
        self.name = f"{color}_rook"


class Bishop(Piece):
    value = 3

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)
        self.color = color
        self.name = f"{color}_bishop"


class Knight(Piece):
    value = 3

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)
        self.color = color
        self.name = f"{color}_knight"


class Queen(Piece):
    value = 9

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)
        self.color = color
        self.name = f"{color}_queen"


class King(Piece):
    value = 100  # does 100 make sense? Worth more than everything on the board

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)
        self.color = color
        self.name = f"{color}_king"


default_board = {
    Tile("a1"): Rook("white", "a1"), Tile("a2"): Pawn("white", "a2"), Tile("a3"): Empty(),
    Tile("a4"): Empty(), Tile("a5"): Empty(), Tile("a6"): Empty(),
    Tile("a7"): Pawn("black", "a7"), Tile("a8"): Rook("black", "a7"), Tile("b1"): Knight("white", "b1"),
    Tile("b2"): Pawn("white", "b2"), Tile("b3"): Empty(), Tile("b4"): Empty(),
    Tile("b5"): Empty(), Tile("b6"): Empty(), Tile("b7"): Pawn("black", "b7"),
    Tile("b8"): Knight("black", "b8"), Tile("c1"): Bishop("white", "c1"), Tile("c2"): Pawn("white", "c2"),
    Tile("c3"): Empty(), Tile("c4"): Empty(), Tile("c5"): Empty(),
    Tile("c6"): Empty(), Tile("c7"): Pawn("black", "c7"), Tile("c8"): Bishop("black", "c8"),
    Tile("d1"): Empty(), Tile("d2"): Pawn("white", "d2"), Tile("d3"): Empty(),
    Tile("d4"): Empty(), Tile("d5"): Empty(), Tile("d6"): Empty(),
    Tile("d7"): Pawn("black", "d7"), Tile("d8"): Queen("black", "d8"), Tile("e1"): King("white", "e1"),
    Tile("e2"): Pawn("white", "e2"), Tile("e3"): Empty(), Tile("e4"): Empty(),
    Tile("e5"): Empty(), Tile("e6"): Empty(), Tile("e7"): Pawn("white", "e7"),
    Tile("e8"): King("black", "e8"), Tile("f1"): Bishop("white", "f1"), Tile("f2"): Pawn("white", "f2"),
    Tile("f3"): Empty(), Tile("f4"): Empty(), Tile("f5"): Empty(),
    Tile("f6"): Empty(), Tile("f7"): Pawn("black", "f7"), Tile("f8"): Bishop("black", "f8"),
    Tile("g1"): Knight("white", "g1"), Tile("g2"): Pawn("white", "g2"), Tile("g3"): Empty(),
    Tile("g4"): Empty(), Tile("g5"): Empty(), Tile("g6"): Empty(),
    Tile("g7"): Pawn("black", "g7"), Tile("g8"): Empty(), Tile("h1"): Rook("white", "h1"),
    Tile("h2"): Pawn("white", "h2"), Tile("h3"): Empty(), Tile("h4"): Empty(),
    Tile("h5"): Empty(), Tile("h6"): Empty(), Tile("h7"): Pawn("black", "h7"),
    Tile("h8"): Rook("black", "h8"),
    }

testing_board = {
    Tile("a1"): Rook("white", "a1"), Tile("a2"): Pawn("white", "a2"), Tile("a3"): Empty(),
    Tile("a4"): Empty(), Tile("a5"): Rook("black", "a1"), Tile("a6"): Empty(),
    Tile("a7"): Pawn("black", "a7"), Tile("a8"): Rook("black", "a7"), Tile("b1"): Knight("white", "b1"),
    Tile("b2"): Pawn("white", "b2"), Tile("b3"): Empty(), Tile("b4"): Empty(),
    Tile("b5"): Pawn("white", "b7"), Tile("b6"): Empty(), Tile("b7"): Empty(),
    Tile("b8"): Knight("black", "b8"), Tile("c1"): Bishop("white", "c1"), Tile("c2"): Pawn("white", "c2"),
    Tile("c3"): Empty(), Tile("c4"): Empty(), Tile("c5"): Empty(),
    Tile("c6"): Empty(), Tile("c7"): Pawn("black", "c7"), Tile("c8"): Bishop("black", "c8"),
    Tile("d1"): Empty(), Tile("d2"): Pawn("white", "d2"), Tile("d3"): Empty(),
    Tile("d4"): Empty(), Tile("d5"): Empty(), Tile("d6"): Empty(),
    Tile("d7"): Bishop("black", "c8"), Tile("d8"): Queen("black", "d8"), Tile("e1"): King("white", "e1"),
    Tile("e2"): Empty(), Tile("e3"): Empty(), Tile("e4"): Pawn("white", "e2"),
    Tile("e5"): Empty(), Tile("e6"): Empty(), Tile("e7"): Pawn("white", "e7"),
    Tile("e8"): King("black", "e8"), Tile("f1"): Bishop("white", "f1"), Tile("f2"): Pawn("white", "f2"),
    Tile("f3"): Empty(), Tile("f4"): Empty(), Tile("f5"): Empty(),
    Tile("f6"): Empty(), Tile("f7"): Pawn("black", "f7"), Tile("f8"): Bishop("black", "f8"),
    Tile("g1"): Knight("white", "g1"), Tile("g2"): Pawn("white", "g2"), Tile("g3"): Empty(),
    Tile("g4"): Empty(), Tile("g5"): Rook("black", "h1"), Tile("g6"): Empty(),
    Tile("g7"): Pawn("black", "g7"), Tile("g8"): Queen("white", "d1"), Tile("h1"): Rook("white", "h1"),
    Tile("h2"): Pawn("white", "h2"), Tile("h3"): Empty(), Tile("h4"): Empty(),
    Tile("h5"): Queen("white", "h3"), Tile("h6"): Empty(), Tile("h7"): Empty(),
    Tile("h8"): Rook("black", "h8"),
    }

# chs = ChessBoard(testing_board)

