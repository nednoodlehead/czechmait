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
        # is the passed in tile an instance of "Empty" (empty chess slot)
        if isinstance(self.board[tile], Empty):
            return False
        else:
            return True

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
            # if there is an x in the notation
            if taking:  # cxb5
                new_tile = notation[2:]
                # if it is white, mark the tile above and on the first-letter file
                if turn == "white":
                    # represents the only tile on the board that a pawn could take a white piece on this square
                    start_tile = notation[0] + str(int(notation[-1] - 1))
                    print(f"{start_tile} is taking to: {new_tile}")
                # if the color is black (all other cases were removed on the valueError above
                else:
                    start_tile = notation[0] + str(int(notation[-1]) + 1)
                    print("WHAT")
                return start_tile, new_tile
            # there is no taking notation, it is a pawn move. e.g. b3
            else:
                if turn == "white":
                    # if the position below the notation is empty, the pawn did a double jump, so starting pos -> 4th
                    if isinstance(self.get_tile(f"{notation[0]}{str(int(notation[1] - 1))}"), Empty):
                        # pawn did do a double jump:
                        return f"{notation[0]}{str(int(notation[1]) - 2)}", notation
                    else:
                        # pawn did not do a double jump
                        return f"{notation[0]}{str(int(notation[1]) - 1)}", notation
                # if it is blacks turn
                else:
                    # if the position above the notation is empty, the pawn did a double jump, so starting pos -> 5th
                    if isinstance(self.get_tile(f"{notation[0]}{str(int(notation[1]) + 1)}"), Empty):
                        # the pawn did do a double jump
                        return f"{notation[0]}{str(int(notation[1]) + 2)}", notation
                    else:
                        # the pawn did not do a double jump
                        return f"{notation[0]}{str(int(notation[1]) + 1)}", notation
        # knight  (Kb5 or Kge5(knight from g file to e5))
        elif notation[0] == "N":
            new_str = ""
            for letter in notation:
                if letter in "+#x":
                    pass
                else:
                    new_str += letter
            notation = new_str
            # this is from the given tile, where could knights come from: represented in coordinates relative to notat
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
                return nearby_knights[0], notation[-2:]
            # case where notation denotes that the second char is unique (letter or number). It
            elif len(notation) == 4:  # case Nde3 (b file knights goes to e3)
                # unique is the character that uniquely identifies the original square
                unique = notation[1]
                for item in nearby_knights:
                    if unique in item:
                        return item, notation[-2:]
            elif len(notation) == 5:
                return notation[1:3], notation[3:5]  # (e.g. N3d4)

        elif notation[0] == "B":  # bishop
            # would be a much easier notation if promoting to bishop wasn't a thing
            # parse the extras from notation out
            new_str = ""
            for letter in notation:
                if letter in "x+#":
                    pass
                else:
                    new_str += letter
            notation = new_str
            ops = [("+", "+"), ("+", "-"), ("-", "+"), ("-", "-")]
            # will contain list of available moves where the bishop could have moved from
            bishop_tiles = []
            # for each pair of operators:
            for operator_pair in ops:
                # count represents going just one square at a time
                count = 1
                # loop over each option of a diagonal (a1, b2, c3, d4...)
                while True:
                    # create the x and y of the tile to pass to convert_tile (e.g. -1, +1)
                    increment_number_1 = int(operator_pair[0] + str(count))
                    increment_number_2 = int(operator_pair[1] + str(count))
                    # convert the numbers into a tile, relative to starting tile
                    new_tile = self.convert_tile(notation[-2:], increment_number_1, increment_number_2)
                    # if the tile is occupied by bishop, append to list, and break. As more bishops have no impact
                    if new_tile is None:
                        break
                    elif isinstance(self.board[new_tile], Bishop):
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
                print(notation, bishop_tiles)
                return bishop_tiles[0], notation[-2:]
            # in case where there is a unique char as the first index, we can use that to determine which bishop is in
            # the notation
            if len(notation) == 4:
                for bishop in bishop_tiles:
                    if notation[1] in bishop:
                        return bishop, notation[-2:]
            # if the length of the notation is greater than 4, then the 1st and 2nd chars are the first tile,
            # and 3rd and 4th are the ending notation
            if len(notation) > 4:
                return notation[1:3], notation[3:5]
        elif notation[0] == "R":  # rook
            pass
        elif notation[0] == "Q":  # queen
            pass
        else:  # in the instance of a king move ...
            pass


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


class Bishop(Piece):
    value = 3

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)
        self.color = color


class Knight(Piece):
    value = 3

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)
        self.color = color


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

testing_board = {
    Tile("a1"): Rook("white", "a1"), Tile("a2"): Pawn("white", "a2"), Tile("a3"): Empty(),
    Tile("a4"): Empty(), Tile("a5"): Empty(), Tile("a6"): Empty(),
    Tile("a7"): Pawn("black", "a7"), Tile("a8"): Rook("black", "a7"), Tile("b1"): Knight("white", "b1"),
    Tile("b2"): Pawn("white", "b2"), Tile("b3"): Empty(), Tile("b4"): Empty(),
    Tile("b5"): Pawn("black", "b7"), Tile("b6"): Empty(), Tile("b7"): Empty(),
    Tile("b8"): Knight("black", "b8"), Tile("c1"): Bishop("white", "c1"), Tile("c2"): Pawn("white", "c2"),
    Tile("c3"): Empty(), Tile("c4"): Empty(), Tile("c5"): Empty(),
    Tile("c6"): Empty(), Tile("c7"): Pawn("black", "c7"), Tile("c8"): Bishop("black", "c8"),
    Tile("d1"): Queen("white", "d1"), Tile("d2"): Pawn("white", "d2"), Tile("d3"): Empty(),
    Tile("d4"): Empty(), Tile("d5"): Empty(), Tile("d6"): Empty(),
    Tile("d7"): Bishop("black", "c8"), Tile("d8"): Queen("black", "d8"), Tile("e1"): King("white", "e1"),
    Tile("e2"): Empty(), Tile("e3"): Empty(), Tile("e4"): Pawn("white", "e2"),
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

chs = ChessBoard(testing_board)
# x = chs.is_occupied_enemy(chs.get_tile("g5"), "black")
x = chs.notation_translation("Bxb5", "white")

print(f"{x[0]} moved to {x[1]}")




