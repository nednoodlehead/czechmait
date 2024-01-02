from board.chessboard import ChessBoard
from board.pieces import Rook, is_in_check, King, Bishop, Queen, Pawn
import pytest
from board.color import Black, White
from board.empty import Empty


def test_check():
     chs = ChessBoard()
     chs.move_from_notation("d4", White)
     chs.move_from_notation("d5", Black)
     chs.board["e1"] = Empty()
     chs.board["c4"] = King(White)
     chs.board["h4"] = Rook(Black)
     assert(is_in_check(chs, White) == True)
     chs.move_from_notation("Kb4", White)
     assert(is_in_check(chs, White) == False)
     chs.board["d6"] = Bishop(Black)
     assert(is_in_check(chs, White) == True)
