# purpose of these classes are to reduce code duplication by having the colors have an associated value (white = +1,
# black = -1. Represents where the pawns can move
class Black:
    color = "black"
    opposite_color = None
    pawn_starting_rank = "7"
    pawn_promotion_rank = "1"

    @staticmethod
    def value(other: int):
        return int("-" + str(other))

    @staticmethod
    def pawn_coming_from():
        return +1
    def __repr__(self):
        return "Black"


class White:
    color = "white"
    opposite_color = None
    pawn_starting_rank = "2"
    pawn_promotion_rank = "8"

    @staticmethod
    def value(other: int):
        return int("+" + str(other))

    # used to show which tile a pawn came from. used in notation translation for pawns
    @staticmethod
    def pawn_coming_from():
        return -1
    def __repr__(self):
        return "White"


# the classes must have this attribute, we add it here, so we do not have any undefined values inside 'Black'
Black.opposite_color = White
White.opposite_color = Black
