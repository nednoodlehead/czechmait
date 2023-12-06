
# purpose of this class / file is to standardize how 'last move' looks. since right now it is horrible
# as of pre november 2023 commits.
from board.tile import Tile
from board.color import Black, White
from board.pieces import Piece, EnpassantRemnant

# used to formalize showing additional information that comes with a move
# so it can be either castling, enpassant or a two-sqaure pawn move (creates an enpassant remnant)
class Extra:
    pass

class LastMove:
    def __init__(self, undone_tile: Tile, undone_occupant: Piece, original_tile: Tile, original_occupant: Piece, color: White | Black, extra: Extra | None):
        """
        example: 1. d4
        param: undone_tile: Tile. d4
        param: undone_occupant: Piece. pawn
        param: original_tile: Tile. d2
        param: original_occupant: Empty | Piece. Empty
        param: color: White | Black. 
        param: extra: Extra | None. Represents extra information like castling, en passant, or pawn double jump. None
        """
        self.undone_tile = undone_tile
        self.undone_occupant = undone_occupant
        self.original_tile = original_tile
        self.original_occupant = original_occupant
        self.color = color
        self.extra = extra
    def __str__(self):
        return f"undone_tile: ({self.undone_tile}\nundone_occupant: {self.undone_occupant}\noriginal_tile: {self.original_tile}\noriginal_occupant: {self.original_occupant}\ncolor: {self.color})"
    def __repr__(self):
        return f"undone_tile: ({self.undone_tile}\nundone_occupant: {self.undone_occupant}\noriginal_tile: {self.original_tile}\noriginal_occupant: {self.original_occupant}\ncolor: {self.color})"


class Enpassant(Extra):
# starting
    def __init__(self, death_tile: Tile, color: White | Black):
        """
        Arguments:
        starting_tile: Tile. Tile that the pawn begins on, so either 2nd or 7th rank
        death_tile: Tile. Tile that the pawn dies on, so either 4th or 5th rank
        color: Color. Black or White.
        """
        self.death_tile = death_tile
        self.color = color

class Castle(Extra):  # the king's movement is first class, so this will describe the rook's movement
    def __init__(self, rook_starting: Tile, rook_ending: Tile, color: White | Black):
        """
        Arguments:
        rook_starting: Tile. the tile that the rook begins the castle action in (a1, a8, h1, h8 only)
        rook_ending: Tile. the tile that the rook will end the castle movement on (d1, f1, d8, f8 only)
        color: Color. Black or White
        """

        self.rook_starting = rook_starting
        self.rook_ending = rook_ending
        self.color = color


class DoublePawnMove(Extra):
    # the pawn's nomal move (ex. d2 -> d4) is held outside of the extra type
    # this just contains the extra instruction for the move interperter to create an enpassant remnant
    # on the tile between the two (d3, in this case)
    def __init__(self, tile: Tile, color: White | Black):
        """
        Arguments:
        tile: Tile. tile that the enpassant remnant is on. (Must be on 3rd or 6th rank)
        color: Color. White or Black

        Info:
        self.type: EnpassantRemnant. Instance of enpassant remnant to represent the tile
        """
        self.tile = tile
        self.color = color
        self.type = EnpassantRemnant(self.color)

class Move:
    def __init__(self, old_tile: Tile, new_tile: Tile, piece: Piece, extra: Extra | None):
        """
        Arguments:
        old_tile: Tile. Tile that the piece was on before
        new_tile: Tile. Tile that the piece is now on
        piece: Piece. What piece is occupying it?
        extra: Extra or None. Optional extra information (castling, en passant, pawn double jump)    
        """
        self.old_tile = old_tile
        self.new_tile = new_tile
        self.piece = piece
        self.extra = extra  
    def __str__(self):
        return f"{self.piece} moves from {self.old_tile} to {self.new_tile}"
