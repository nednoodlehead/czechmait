from tests.boards import default_board
from board.empty import Empty
from board.pieces import Pawn, Bishop, Knight, Rook, Queen, King, EnpassantRemnant
from board.tile import Tile
from board.chessboard import ChessBoard
from board.color import Black, White
from board.data_structure import Move

def test_possible_moves_default():
    chs = ChessBoard(default_board)
    assert isinstance(x := chs.all_possible_moves(chs, White)[0], Move) and x.old_tile == Tile("a2") and x.new_tile == Tile("a3")
    assert isinstance(x := chs.all_possible_moves(chs, White)[-1], Move) and x.old_tile == Tile("h2") and x.new_tile == Tile("h4")
    print("all tests passed")

def test_options_from_check():
    chs = ChessBoard(default_board)
    chs.move_from_notation("e4", White)
    chs.move_from_notation("e5", Black)
    chs.move_from_notation("Qh5", White)
    chs.move_from_notation("g6", Black)
    chs.move_from_notation("Qxe5", White)
    print(chs.all_possible_moves(chs, Black))
