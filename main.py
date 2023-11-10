from board.color import Black, White
from tests.test_analysis import test_notation_translation  # call tests
from tests.test_undo import test_three_move_undo
from board.chessboard import ChessBoard
from tests.boards import proper_testing_board, default_board

def main():
     # test_notation_translation()
    
    # bd = ChessBoard(proper_testing_board)
    # print(bd.notation_translation("Raxb5", Black))
    # chs = ChessBoard(default_board)
    # chs.move_from_notation("d4", White)
    # chs.move_from_notation("d5", Black)
    # chs.move_from_notation("Nf3", White)
    
    print(test_three_move_undo())
main() 


