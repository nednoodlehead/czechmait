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


# represents an empty tile
class Empty:
    # used in the queries of what occupies a tile, returns None to that query. This is the alternative to error handing
    # within the queries themselves
    color = None


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
            # raise ValueError(f"Did not input black or white :: {color}")
            return "balls?"

    def testin(self):
        print(self.board["a1"].color)

    def get_tile(self, tile):
        """Returns the desired tile instance from given input
        :param tile (str) tile instance being requested"""
        for key in self.board.keys():
            if key.tile == tile:
                return key


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
                if not board.is_occupied(f"{tile[0]}5"):
                    # add to available moves list
                    available.append(f"{tile[0]}5")
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
    Tile("a1"): Rook("white", "a1"), Tile("a2"): Pawn("white", "a2"), Tile("a3"): Empty(),
    Tile("a4"): Empty(), Tile("a5"): Empty(), Tile("a6"): Empty(),
    Tile("a7"): Pawn("black", "a7"), Tile("a8"): Rook("black", "a7"), Tile("b1"): Knight("white", "b1"),
    Tile("b2"): Pawn("white", "b2"), Tile("b3"): Empty(), Tile("b4"): Empty(),
    Tile("b5"): Empty(), Tile("b6"): Empty(), Tile("b7"): Pawn("black", "b7"),
    Tile("b8"): Knight("black", "b8"), Tile("c1"): Bishop("white", "c1"), Tile("c2"): Pawn("white", "c2"),
    Tile("c3"): Empty(), Tile("c4"): Empty(), Tile("c5"): Empty(),
    Tile("c6"): Empty(), Tile("c7"): Pawn("black", "c7"), Tile("c8"): Bishop("black", "c8"),
    Tile("d1"): Queen("white", "d1"), Tile("d2"): Pawn("white", "d2"), Tile("d3"): Empty(),
    Tile("d4"): Empty(), Tile("d5"): Empty(), Tile("d6"): Empty(),
    Tile("d7"): Pawn("black", "d7"), Tile("d8"): Queen("black", "d8"), Tile("e1"): King("white", "e1"),
    Tile("e2"): Pawn("white", "e2"), Tile("e3"): Empty(), Tile("e4"): Empty(),
    Tile("e5"): Empty(), Tile("e6"): Empty(), Tile("e7"): Pawn("white", "e7"),
    Tile("e8"): King("black", "e8"), Tile("f1"): Bishop("white", "f1"), Tile("f2"): Pawn("white", "f2"),
    Tile("f3"): Empty(), Tile("f4"): Empty(), Tile("f5"): Empty(),
    Tile("f6"): Empty(), Tile("f7"): Pawn("black", "f7"), Tile("f8"): Bishop("black", "f8"),
    Tile("g1"): Knight("white", "g1"), Tile("g2"): Pawn("white", "g2"), Tile("g3"): Empty(),
    Tile("g4"): Empty(), Tile("g5"): Empty(), Tile("g6"): Empty(),
    Tile("g7"): Pawn("black", "g7"), Tile("g8"): Knight("black", "g8"), Tile("h1"): Rook("white", "h1"),
    Tile("h2"): Pawn("white", "h2"), Tile("h3"): Empty(), Tile("h4"): Empty(),
    Tile("h5"): Empty(), Tile("h6"): Empty(), Tile("h7"): Pawn("black", "h7"),
    Tile("h8"): Rook("black", "h8"),
    }

chs = ChessBoard()
# x = chs.is_occupied_enemy(chs.get_tile("g5"), "black")
x = chs.board["c7"].available_moves(chs.get_tile("c7"), chs)

print(x)




