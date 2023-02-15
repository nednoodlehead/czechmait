# purpose of this file is to take in a chessboard as data, and analyze the position

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
        # if the result of adding letters either goes above 104 (h) or lower than 97 (a), raise error
        if amount_letter + ord(org_let) > 104 or amount_letter + ord(org_let) < 97:
            raise ValueError("Invalid numbers entered. Please have the result be between A1-H8")
        # if the results of adding org number go above 8 or below 1, raise error
        if amount_number + org_num > 8 or amount_number + org_num < 1:
            raise ValueError("Invalid numbers entered. Please have the result be between A1-H8")
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
        if not self.board[tile]:
            return False
        else:
            return True

    def is_occupied_enemy(self, tile, color):
        """ Returns a bool based on if the given tile is occupied by opposite color
        :param tile: Tile, tile to inspect (tile class)
        :param color: str, either white or black, the color of the player querying
        :returns bool: is it occupied by enemy piece? aka, can it be taken?"""
        if color.lower() == "black":
            if self.board[tile].color:
                pass
        if color.lower == "white":
            if self.board[tile].color:
                pass
        else:
            raise ValueError(f"Did not input black or white :: {color}")

    def testin(self):
        print(self.board["a1"])


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
            if tile[0] == "7":
                # if the letter position two ahead of it is unoccupied, you can move there
                if not board.is_occupied(f"{tile[0]}5"):
                    # add to available moves list
                    available.append(f"{tile[0]}5")
            # if the given tile is not on the seventh rank
            else:
                # if the tile infront of it is unoccupied, you can move there
                if not board.is_occupied(f"{tile[0]}{int(tile[1] -1)}"):
                    available.append(f"{tile[0]}{int(tile[1] -1)}")
            # if there is an opposite colored piece that is on its diagonals
            # if tile.convert_tile(1, -1)


class Rook(Piece):
    value = 5

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)


class Bishop(Piece):
    value = 3

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)


class Knight(Piece):
    value = 3

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)


class Queen(Piece):
    value = 9

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)


class King(Piece):
    value = 100  # does 100 make sense? Worth more than everything on the board

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)


default_board = {
    Tile("a1"): None, Tile("a2"): None, Tile("a3"): None,
    Tile("a4"): None, Tile("a5"): None, Tile("a6"): None,
    Tile("a7"): None, Tile("a8"): None, Tile("b1"): None,
    Tile("b2"): None, Tile("b3"): None, Tile("b4"): None,
    Tile("b5"): None, Tile("b6"): None, Tile("b7"): None,
    Tile("b8"): None, Tile("c1"): None, Tile("c2"): None,
    Tile("c3"): None, Tile("c4"): None, Tile("c5"): None,
    Tile("c6"): None, Tile("c7"): None, Tile("c8"): None,
    Tile("d1"): None, Tile("d2"): None, Tile("d3"): None,
    Tile("d4"): None, Tile("d5"): None, Tile("d6"): None,
    Tile("d7"): None, Tile("d8"): None, Tile("e1"): None,
    Tile("e2"): None, Tile("e3"): None, Tile("e4"): None,
    Tile("e5"): None, Tile("e6"): None, Tile("e7"): None,
    Tile("e8"): None, Tile("f1"): None, Tile("f2"): None,
    Tile("f3"): None, Tile("f4"): None, Tile("f5"): None,
    Tile("f6"): None, Tile("f7"): None, Tile("f8"): None,
    Tile("g1"): None, Tile("g2"): None, Tile("g3"): None,
    Tile("g4"): None, Tile("g5"): None, Tile("g6"): None,
    Tile("g7"): None, Tile("g8"): None, Tile("h1"): None,
    Tile("h2"): None, Tile("h3"): None, Tile("h4"): None,
    Tile("h5"): None, Tile("h6"): None, Tile("h7"): None,
    Tile("h8"): None,
    }

chs = ChessBoard()
chs.testin()




