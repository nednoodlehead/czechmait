class Piece:

    def __init__(self, color, starting_tile):
        self.color = color
        self.starting_tile = starting_tile

    def on_starting_tile(self, tile):
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

    def available_moves(self, tile, board):  # returns a move notation list e.g. [a4, xb3]
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