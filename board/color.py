# purpose of these classes are to reduce code duplication by having the colors have an associated value (white = +1,
# black = -1. Represents where the pawns can move
class Black:
    color = "black"

    @staticmethod
    def value(other: int):
        return int("-" + str(other))

    @staticmethod
    def pawn_coming_from():
        return +1


class White:
    color = "white"

    @staticmethod
    def value(other: int):
        return int("+" + str(other))

    # used to show which tile a pawn came from. used in notation translation for pawns
    @staticmethod
    def pawn_coming_from():
        return -1
