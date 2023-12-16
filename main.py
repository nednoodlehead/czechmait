from board.color import Black, White
from tests.test_analysis import test_notation_translation  # call tests
from tests.test_undo import test_three_move_undo
from board.chessboard import ChessBoard
from tests.boards import proper_testing_board, default_board
from tests.test_in_check import test_check
from analysis.board_calculation import evaluate_material
from board.empty import Empty
from board.pieces import is_in_check, Rook
from tests.test_possible_moves import test_possible_moves_default, test_options_from_check

def main():
     chs = ChessBoard()
     chs.move_from_notation("d4", White)
     chs.move_from_notation("e5", Black)
     chs.move_from_notation("dxe5", White)
     chs.move_from_notation("Bb4+", Black)
     print(f'white moves: {chs.all_possible_moves(chs, White)}')   

     
main() 

