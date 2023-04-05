# purpose is to be able to give a string of move orders, and create a chessboard object from that
from board.chessboard import ChessBoard
from tests.boards import default_board
from board.color import White, Black


def parse_to_cmd(input_val: str):
    """
    turns a move set into a command list, readable by this program (Chessboard.notation_translation)
    :param input_val: input string. e.g. "1. d4 e5 2. dxe5 Nc6 3. Nf3 Qe7" for englund gambit
    :return: chessboard object with the move order as the board. mostly for debugging and whatnot
    """
    new_value = []
    split_str = input_val.split()
    for item in split_str:
        if "." in item:
            continue
        else:
            new_value.append(item)
    return new_value


def cmd_to_chessboard(value_list, color=White):
    chs = ChessBoard(default_board)
    for count, pre_command in enumerate(value_list):
        command = chs.notation_translation(pre_command, color)
        old, new, piece, *extra = command
        chs.update_board(chs, old, new, piece, extra)
        # chs.export_png(f"SET_{count}")
        # switch the colors for next loop (the other color will move next, duh)
        color = color.opposite_color
    return chs


