from PIL import Image
import os.path
from empty.empty import Empty

# os.chdir(r"F:\Projects\Python Projects\czechmait")

def generate_map():
    piece_map = {}
    print(os.getcwd())
    for path in os.listdir(r"./resources"):
        print(path)
        opened = Image.open(f"./resources/{path}")
        png = opened.convert("RGBA")
        piece_map[path[:-4]] = png
    return piece_map


def hashmap_to_png(board: dict):
    piece_key = generate_map()
    png_board = Image.open("./resources/chessboard.png")
    for key, value in board.items():
        if not isinstance(value, Empty):
            print(value)
            y_value, x_value = tile_to_pixels(key.tile)
            png_board.paste(piece_key[value.name], (y_value, x_value), piece_key[value.name])
    png_board.save("OUTPUT.png")



def tile_to_pixels(tile: str) -> (int, int):
    char_map = {
        "a": 0,
        "b": 100,
        "c": 200,
        "d": 300,
        "e": 400,
        "f": 500,
        "g": 600,
        "h": 700
    }
    return char_map[tile[0]], (int(tile[1]) - 1) * 100







