class Piece:

    def __init__(self, color, starting_tile):
        self.color = color
        self.starting_tile = starting_tile

    def __repr__(self):
        return f"starting: {self.starting_tile}"


class Pawn(Piece):
    # value of piece defined here, this will be used to calculate material later
    value = 1
    # we pass in the color of the piece and what tile it begins on

    def __init__(self, color, starting_tile):
        super().__init__(color, starting_tile)
        self.color = color
        self.name = f"{color}_pawn"


class EnpassantRemnant:  # does not inherit from 'Piece', because it is logically not a piece, and to distinguish from
    # normal pieces

    # purpose of this class is to leave this behind in the square that was jumped over during a double jump pawn move
    # it must have special properties to not have it block sightlines for other pieces, but be visible to pawns
    # it must also decay one move after being placed
    value = 1  # value = 1 cause it is a pawn capture...
    # decay of all enpassant remnants will be reduced by 1 each turn, and will be removed if it == 0
    # one is removed on said turn i believe, so 3 should make sense
    decay = 3

    def __init__(self, color):
        self.color = color
        self.name = f"{color}_en"


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
