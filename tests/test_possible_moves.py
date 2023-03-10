import pytest
from board.empty import Empty
from board.pieces import Pawn, Bishop, Knight, Rook, Queen, King, EnpassantRemnant
from board.tile import Tile
from board.chessboard import ChessBoard
from board.color import Black, White


@pytest.fixture()
def board():
    testing_board = {
        Tile("a1"): Rook(White, "a1"), Tile("a2"): Pawn(White, "a2"), Tile("a3"): Empty(),
        Tile("a4"): Empty(), Tile("a5"): Rook(Black, "a1"), Tile("a6"): Empty(),
        Tile("a7"): Pawn(Black, "a7"), Tile("a8"): Rook(Black, "a7"), Tile("b1"): Knight(White, "b1"),
        Tile("b2"): Pawn(White, "b2"), Tile("b3"): Empty(), Tile("b4"): Empty(),
        Tile("b5"): Pawn(White, "b7"), Tile("b6"): Empty(), Tile("b7"): Empty(),
        Tile("b8"): Knight(Black, "b8"), Tile("c1"): Bishop(White, "c1"), Tile("c2"): Pawn(White, "c2"),
        Tile("c3"): Empty(), Tile("c4"): Knight(White, "c4"), Tile("c5"): Empty(),
        Tile("c6"): Empty(), Tile("c7"): Pawn(Black, "c7"), Tile("c8"): Bishop(Black, "c8"),
        Tile("d1"): Empty(), Tile("d2"): Pawn(White, "d2"), Tile("d3"): Empty(),
        Tile("d4"): Empty(), Tile("d5"): Empty(), Tile("d6"): Empty(),
        Tile("d7"): Bishop(Black, "c8"), Tile("d8"): Queen(Black, "d8"), Tile("e1"): King(White, "e1"),
        Tile("e2"): Empty(), Tile("e3"): Empty(), Tile("e4"): Pawn(White, "e2"),
        Tile("e5"): Empty(), Tile("e6"): Empty(), Tile("e7"): Pawn(White, "e7"),
        Tile("e8"): King(Black, "e8"), Tile("f1"): Bishop(White, "f1"), Tile("f2"): Pawn(White, "f2"),
        Tile("f3"): Empty(), Tile("f4"): Empty(), Tile("f5"): Empty(),
        Tile("f6"): Empty(), Tile("f7"): Pawn(Black, "f7"), Tile("f8"): Bishop(Black, "f8"),
        Tile("g1"): Knight(White, "g1"), Tile("g2"): Pawn(White, "g2"), Tile("g3"): Empty(),
        Tile("g4"): Empty(), Tile("g5"): Rook(Black, "h1"), Tile("g6"): Empty(),
        Tile("g7"): Pawn(Black, "g7"), Tile("g8"): Queen(White, "d1"), Tile("h1"): Rook(White, "h1"),
        Tile("h2"): Pawn(White, "h2"), Tile("h3"): Empty(), Tile("h4"): Empty(),
        Tile("h5"): Queen(White, "h3"), Tile("h6"): Empty(), Tile("h7"): Empty(),
        Tile("h8"): Rook(Black, "h8"),
    }
    return ChessBoard(testing_board)


def test_available_move(board: ChessBoard):
    assert board.board["e7"].analysis(board, "e7") == [("f8", Knight), ("f8", Bishop), ("f8", Rook), ("f8", Queen),
                                                 ("d8", Knight), ("d8", Bishop), ("d8", Rook), ("d8", Queen)]
    assert board.board["c7"].analysis(board, "c7") == [("c6", Pawn), ("c5", Pawn, ("c6", EnpassantRemnant))]
    assert board.board["f1"].analysis(board, "f1") == [("e2", Bishop), ("d3", Bishop)]
    assert board.board["d7"].analysis(board, "d7") == [("e6", Bishop), ("f5", Bishop), ("g4", Bishop),
                                                           ("h3", Bishop), ("c6", Bishop), ("b5", Bishop)]
    assert board.board["c4"].analysis(board, "c4") == [("d6", Knight), ("b6", Knight), ("e3", Knight), ("e5", Knight),
                                                   ("a5", Knight), ("a3", Knight)]
    assert board.board["b8"].analysis(board, "b8") == [("c6", Knight), ("a6", Knight)]
    assert board.board["h8"].analysis(board, "h8") == [("g8", Rook), ("h7", Rook), ("h6", Rook), ("h5", Rook)]
    assert board.board["a5"].analysis(board, "a5") == [("b5", Rook), ("a6", Rook), ("a4", Rook), ("a3", Rook),
                                                       ("a2", Rook)]
    assert board.board["d8"].analysis(board, "d8") == [("e7", Queen)]
    assert board.board["h5"].analysis(board, "h5") == [("h6", Queen), ("h7", Queen), ("h8", Queen), ("g5", Queen),
                                                  ("h4", Queen), ("h3", Queen), ("g6", Queen), ("f7", Queen),
                                                  ("g4", Queen), ("f3", Queen), ("e2", Queen), ("d1", Queen)]
    assert board.board["e1"].analysis(board, "e1") == ["e2", "d1"]
    assert board.board["e8"].analysis(board, "e8") == ["e7"]
    