import pytest
from board.chessboard import ChessBoard
from tests.boards import default_board as db
from board.color import White, Black
from board.pieces import Knight, Pawn, King, Queen, Rook, Bishop
from board.tile import Tile
from board.empty import Empty
from board.data_structure import LastMove

# testing if the Chessboard class adds to self.last_move and undos moves correctly



def test_three_move_undo():
    chs = ChessBoard(db)
    chs.move_from_notation("d4", White)
    chs.move_from_notation("d5", Black)
    chs.move_from_notation("Nf3", White)
    
    assert isinstance( x := chs.last_move[-1], LastMove) and x.undone_tile == Tile("f3") and isinstance(x.undone_occupant, Knight) and x.original_tile == Tile("g1") and isinstance(x.original_occupant, Empty) and x.color == White
    chs.undo_move()
    assert isinstance(x := chs.last_move[-1], LastMove) and x.undone_tile == Tile("d5") and isinstance(x.undone_occupant, Pawn) and x.original_tile == Tile("d7") and isinstance(x.original_occupant, Empty) and x.color == Black

    print("Undo tests passed")
