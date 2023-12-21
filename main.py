from board.color import Black, White
from tests.test_analysis import test_notation_translation  # call tests
from tests.test_undo import test_three_move_undo
from board.chessboard import ChessBoard
from tests.boards import proper_testing_board, default_board
from tests.test_in_check import test_check
from analysis.board_calculation import evaluate_material, basic_minmax
from board.empty import Empty
from board.pieces import is_in_check, Rook
from tests.test_possible_moves import test_possible_moves_default, test_options_from_check
from board.data_structure import Move
from board.tile import Tile
from board.pieces import Pawn

def main():
     chs = ChessBoard()
     chs.move_from_notation("Nc3", White)
     chs.move_from_notation("c6", Black)
     chs.move_from_notation("Nd5", White)
     chs.move_from_notation("Qa5", Black)
     chs.move_from_notation("e3", White)
     chs.move_from_notation("Qb4", Black)
     x = basic_minmax(chs, White, True, 2)
     print(f'bets move is: {x[1]} with eval score of {x[0]}')          
main() 

