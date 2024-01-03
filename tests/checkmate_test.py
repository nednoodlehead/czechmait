from board.chessboard import ChessBoard
from board.data_structure import CheckMate
from board.pieces import Queen, Pawn, Bishop, Rook, Knight, King
from tests.boards import empty_board
from board.empty import Empty
from board.tile import Tile
from board.color import Black, White
from analysis.board_calculation import is_checkmated

def test_if_in_checkmate():
     chs = ChessBoard(empty_board)
     chs.board["a1"] == Rook(White)
     chs.board["b1"] == Rook(White)
     chs.board["a8"] == King(Black)
     chs.board["h1"] == King(White)
     assert (is_checkmated(chs, Black) == True)

def test_scholars():
     chs = ChessBoard()
     chs.move_from_game("e4 e5 Qh5 a6 Bc4 Nf6 Qxf7")
     print(is_checkmated(chs, Black))
     print(chs.all_possible_moves(chs, Black))
     print(chs)
