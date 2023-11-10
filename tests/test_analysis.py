import pytest
from board.empty import Empty
from board.pieces import Pawn, Bishop, Knight, Rook, Queen, King
from board.tile import Tile
from board.chessboard import ChessBoard
from board.color import Black, White
from tests.boards import proper_testing_board, test_castling_board, test_enpassant_board
from board.data_structure import Move, LastMove
@pytest.fixture()
def board():
    testing_board = {
        Tile("a1"): Rook(White), Tile("a2"): Pawn(White), Tile("a3"): Empty(),
        Tile("a4"): Empty(), Tile("a5"): Rook(Black), Tile("a6"): Empty(),
        Tile("a7"): Pawn(Black), Tile("a8"): Rook(Black), Tile("b1"): Knight(White),
        Tile("b2"): Pawn(White), Tile("b3"): Empty(), Tile("b4"): Empty(),
        Tile("b5"): Pawn(White), Tile("b6"): Empty(), Tile("b7"): Empty(),
        Tile("b8"): Knight(Black), Tile("c1"): Bishop(White), Tile("c2"): Pawn(White),
        Tile("c3"): Empty(), Tile("c4"): Empty(), Tile("c5"): Empty(),
        Tile("c6"): Empty(), Tile("c7"): Pawn(Black), Tile("c8"): Bishop(Black),
        Tile("d1"): Empty(), Tile("d2"): Pawn(White), Tile("d3"): Empty(),
        Tile("d4"): Empty(), Tile("d5"): Empty(), Tile("d6"): Empty(),
        Tile("d7"): Bishop(Black), Tile("d8"): Queen(Black), Tile("e1"): King(White),
        Tile("e2"): Empty(), Tile("e3"): Empty(), Tile("e4"): Pawn(White),
        Tile("e5"): Empty(), Tile("e6"): Empty(), Tile("e7"): Pawn(White),
        Tile("e8"): King(Black), Tile("f1"): Bishop(White), Tile("f2"): Pawn(White),
        Tile("f3"): Empty(), Tile("f4"): Empty(), Tile("f5"): Empty(),
        Tile("f6"): Empty(), Tile("f7"): Pawn(Black), Tile("f8"): Bishop(Black),
        Tile("g1"): Knight(White), Tile("g2"): Pawn(White), Tile("g3"): Empty(),
        Tile("g4"): Empty(), Tile("g5"): Rook(Black), Tile("g6"): Empty(),
        Tile("g7"): Pawn(Black), Tile("g8"): Queen(White), Tile("h1"): Rook(White),
        Tile("h2"): Pawn(White), Tile("h3"): Empty(), Tile("h4"): Empty(),
        Tile("h5"): Queen(White), Tile("h6"): Empty(), Tile("h7"): Empty(),
        Tile("h8"): Rook(Black),
        }
    return ChessBoard(testing_board)


@pytest.fixture()
def castle_board():
    castling_board = {
        Tile("a1"): Rook(White), Tile("a2"): Pawn(White), Tile("a3"): Empty(),
        Tile("a4"): Empty(), Tile("a5"): Empty(), Tile("a6"): Empty(),
        Tile("a7"): Pawn(Black), Tile("a8"): Rook(Black), Tile("b1"): Knight(White),
        Tile("b2"): Pawn(White), Tile("b3"): Empty(), Tile("b4"): Empty(),
        Tile("b5"): Empty(), Tile("b6"): Empty(), Tile("b7"): Pawn(Black),
        Tile("b8"): Empty(), Tile("c1"): Bishop(White), Tile("c2"): Pawn(White),
        Tile("c3"): Empty(), Tile("c4"): Empty(), Tile("c5"): Empty(),
        Tile("c6"): Empty(), Tile("c7"): Pawn(Black), Tile("c8"): Empty(),
        Tile("d1"): Empty(), Tile("d2"): Pawn(White), Tile("d3"): Empty(),
        Tile("d4"): Empty(), Tile("d5"): Empty(), Tile("d6"): Empty(),
        Tile("d7"): Pawn(Black), Tile("d8"): Empty(), Tile("e1"): King(White),
        Tile("e2"): Pawn(White), Tile("e3"): Empty(), Tile("e4"): Empty(),
        Tile("e5"): Empty(), Tile("e6"): Empty(), Tile("e7"): Pawn(White),
        Tile("e8"): King(Black), Tile("f1"): Empty(), Tile("f2"): Pawn(White),
        Tile("f3"): Empty(), Tile("f4"): Empty(), Tile("f5"): Empty(),
        Tile("f6"): Empty(), Tile("f7"): Pawn(Black), Tile("f8"): Bishop(Black),
        Tile("g1"): Empty(), Tile("g2"): Pawn(White), Tile("g3"): Empty(),
        Tile("g4"): Empty(), Tile("g5"): Empty(), Tile("g6"): Empty(),
        Tile("g7"): Pawn(Black), Tile("g8"): Empty(), Tile("h1"): Rook(White),
        Tile("h2"): Pawn(White), Tile("h3"): Empty(), Tile("h4"): Empty(),
        Tile("h5"): Empty(), Tile("h6"): Empty(), Tile("h7"): Pawn(Black),
        Tile("h8"): Rook(Black),
    }
    return ChessBoard(castling_board)


@pytest.fixture()
def enpassant_board():
    enpassant = {
        Tile("a1"): Rook(White), Tile("a2"): Pawn(White), Tile("a3"): Empty(),
        Tile("a4"): Empty(), Tile("a5"): Empty(), Tile("a6"): Empty(),
        Tile("a7"): Pawn(Black), Tile("a8"): Rook(Black), Tile("b1"): Knight(White),
        Tile("b2"): Pawn(White), Tile("b3"): Empty(), Tile("b4"): Empty(),
        Tile("b5"): Empty(), Tile("b6"): Empty(), Tile("b7"): Pawn(Black),
        Tile("b8"): Knight(Black), Tile("c1"): Bishop(White), Tile("c2"): Pawn(White),
        Tile("c3"): Empty(), Tile("c4"): Empty(), Tile("c5"): Empty(),
        Tile("c6"): Empty(), Tile("c7"): Pawn(Black), Tile("c8"): Bishop(Black),
        Tile("d1"): Empty(), Tile("d2"): Pawn(White), Tile("d3"): Empty(),
        Tile("d4"): Empty(), Tile("d5"): Pawn(Black), Tile("d6"): Empty(),
        Tile("d7"): Pawn(Black), Tile("d8"): Queen(Black), Tile("e1"): King(White),
        Tile("e2"): Empty(), Tile("e3"): Empty(), Tile("e4"): Empty(),
        Tile("e5"): Pawn(White), Tile("e6"): Empty(), Tile("e7"): Empty(),
        Tile("e8"): King(Black), Tile("f1"): Bishop(White), Tile("f2"): Pawn(White),
        Tile("f3"): Empty(), Tile("f4"): Empty(), Tile("f5"): Empty(),
        Tile("f6"): Empty(), Tile("f7"): Pawn(Black), Tile("f8"): Bishop(Black),
        Tile("g1"): Knight(White), Tile("g2"): Pawn(White), Tile("g3"): Empty(),
        Tile("g4"): Empty(), Tile("g5"): Empty(), Tile("g6"): Empty(),
        Tile("g7"): Pawn(Black), Tile("g8"): Empty(), Tile("h1"): Rook(White),
        Tile("h2"): Pawn(White), Tile("h3"): Empty(), Tile("h4"): Empty(),
        Tile("h5"): Empty(), Tile("h6"): Empty(), Tile("h7"): Pawn(Black),
        Tile("h8"): Rook(Black),
    }
    return ChessBoard(enpassant)


def test_notation_translation():
    #                                notation, color       starting tile, ending tile, piece that will be on ending tile
    import tests   
    board = ChessBoard(proper_testing_board)
    castle_board = ChessBoard(test_castling_board)
    enpassant_board = ChessBoard(test_enpassant_board)
    # asserting that it will give out a correct instance
    assert isinstance(result := board.notation_translation("Raxb5", Black), Move) and result.old_tile == Tile("a5") and result.new_tile == Tile("b5") and isinstance(result.piece, Rook) and result.piece.color == Black
    assert isinstance(result := board.notation_translation("Bf5", Black), Move) and result.old_tile == Tile("d7") and result.new_tile == Tile("f5") and isinstance(result.piece, Bishop) and result.piece.color == Black
    assert isinstance(result := board.notation_translation("exd8=Q", White), Move) and result.old_tile == Tile("e7") and result.new_tile == Tile("d8") and isinstance(result.piece, Queen) and result.piece.color == White
    assert isinstance(result := board.notation_translation("e5", White), Move) and result.old_tile == Tile("e4") and result.new_tile == Tile("e5") and isinstance(result.piece, Pawn) and result.piece.color == White
    assert isinstance(result := board.notation_translation("Qgxh8", White), Move) and result.old_tile == Tile("g8") and result.new_tile == Tile("h8") and isinstance(result.piece, Queen) and result.piece.color == White 
    assert isinstance(result := board.notation_translation("Nc6", Black), Move) and result.old_tile == Tile("b8") and result.new_tile == Tile("c6") and isinstance(result.piece, Knight) and result.piece.color == Black
    assert isinstance(result := board.notation_translation("0-0-0", Black), Move) and result.old_tile == Tile("e8") and result.new_tile == Tile("c8") and isinstance(result.piece, King) and result.piece.color == Black     
    assert isinstance(result := board.notation_translation("O-O", White), Move) and result.old_tile == Tile("e1") and result.new_tile == Tile("g1") and isinstance(result.piece, King) and result.piece.color == White and result.extra.rook_starting == Tile("h1") and result.extra.rook_ending == Tile("f1")
    assert isinstance(result := enpassant_board.notation_translation("exd6", White), Move) and result.old_tile == Tile("e5") and result.new_tile == Tile("d6") and result.extra.death_tile == Tile("d5") and result.extra.color == Black
    # assert enpassant_board.notation_translation("exd6", White) == ("e5", "d6", Pawn, "d5", Empty)
