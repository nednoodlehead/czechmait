import pytest
from analysis.analysis import ChessBoard, Tile, Pawn, Rook, Bishop, Queen, King, Knight
from empty.empty import Empty

@pytest.fixture()
def board():
    testing_board = {
        Tile("a1"): Rook("white", "a1"), Tile("a2"): Pawn("white", "a2"), Tile("a3"): Empty(),
        Tile("a4"): Empty(), Tile("a5"): Rook("black", "a1"), Tile("a6"): Empty(),
        Tile("a7"): Pawn("black", "a7"), Tile("a8"): Rook("black", "a7"), Tile("b1"): Knight("white", "b1"),
        Tile("b2"): Pawn("white", "b2"), Tile("b3"): Empty(), Tile("b4"): Empty(),
        Tile("b5"): Pawn("white", "b7"), Tile("b6"): Empty(), Tile("b7"): Empty(),
        Tile("b8"): Knight("black", "b8"), Tile("c1"): Bishop("white", "c1"), Tile("c2"): Pawn("white", "c2"),
        Tile("c3"): Empty(), Tile("c4"): Empty(), Tile("c5"): Empty(),
        Tile("c6"): Empty(), Tile("c7"): Pawn("black", "c7"), Tile("c8"): Bishop("black", "c8"),
        Tile("d1"): Empty(), Tile("d2"): Pawn("white", "d2"), Tile("d3"): Empty(),
        Tile("d4"): Empty(), Tile("d5"): Empty(), Tile("d6"): Empty(),
        Tile("d7"): Bishop("black", "c8"), Tile("d8"): Queen("black", "d8"), Tile("e1"): King("white", "e1"),
        Tile("e2"): Empty(), Tile("e3"): Empty(), Tile("e4"): Pawn("white", "e2"),
        Tile("e5"): Empty(), Tile("e6"): Empty(), Tile("e7"): Pawn("white", "e7"),
        Tile("e8"): King("black", "e8"), Tile("f1"): Bishop("white", "f1"), Tile("f2"): Pawn("white", "f2"),
        Tile("f3"): Empty(), Tile("f4"): Empty(), Tile("f5"): Empty(),
        Tile("f6"): Empty(), Tile("f7"): Pawn("black", "f7"), Tile("f8"): Bishop("black", "f8"),
        Tile("g1"): Knight("white", "g1"), Tile("g2"): Pawn("white", "g2"), Tile("g3"): Empty(),
        Tile("g4"): Empty(), Tile("g5"): Rook("black", "h1"), Tile("g6"): Empty(),
        Tile("g7"): Pawn("black", "g7"), Tile("g8"): Queen("white", "d1"), Tile("h1"): Rook("white", "h1"),
        Tile("h2"): Pawn("white", "h2"), Tile("h3"): Empty(), Tile("h4"): Empty(),
        Tile("h5"): Queen("white", "h3"), Tile("h6"): Empty(), Tile("h7"): Empty(),
        Tile("h8"): Rook("black", "h8"),
        }
    return ChessBoard(testing_board)



def test_notation_translation(board: ChessBoard):
    #                                notation, color       starting tile, ending tile, piece that will be on ending tile
    assert board.notation_translation("Raxb5", "black") == ("a5", "b5", Rook)
    assert board.notation_translation("Bf5", "black") == ("d7", "f5", Bishop)
    assert board.notation_translation("exd8=Q", "white") == ("e7", "d8", Queen)
    assert board.notation_translation("e5", "white") == ("e4", "e5", Pawn)
    assert board.notation_translation("Qgxh8", "white") == ("g8", "h8", Queen)
    assert board.notation_translation("Nc6", "black") == ("b8", "c6", Knight)
