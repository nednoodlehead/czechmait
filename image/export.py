from PIL import Image, ImageFont, ImageDraw
import os.path
from board.empty import Empty


def generate_map():
    piece_map = {}
    for path in os.listdir(r"./board/resources"):
        opened = Image.open(f"./board/resources/{path}")
        png = opened.convert("RGBA")
        piece_map[path[:-4]] = png
    return piece_map


def hashmap_to_png(board: dict, extra: str, open: bool):
    piece_key = generate_map()
    if open:
        image = Image.open(f"{os.getcwd()}\\regular_board_{extra}.png")
        image.show()
    print(f'export {os.getcwd()}\\extra')
    png_board = Image.open("./board/resources/chessboard.png")
    for key, value in board.items():
        # this covers enpassant remnants, they will have their name set to empty, we can just ignore it...
        if not isinstance(value, Empty):
            if value.name == Empty:
                pass
            y_value, x_value = tile_to_pixels(key.tile)
            png_board.paste(piece_key[value.name], (y_value, x_value), piece_key[value.name])
    png_board.save(f"regular_board_{extra}.png")


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
    num_map = {
        1: 700,
        2: 600,
        3: 500,
        4: 400,
        5: 300,
        6: 200,
        7: 100,
        8: 0
    }
    return char_map[tile[0]], num_map[int(tile[1])]


def generate_value_png(board: dict):
    img = Image.open("./board/resources/chessboard.png")
    font = ImageFont.truetype("./board/font/ArialNarrow7-9YJ9n.ttf", 45)
    draw = ImageDraw.Draw(img)
    for key, value in board.items():
        y_value, x_value = tile_to_pixels(key.tile)
        # add 50 so the text is more centered on the square : )
        draw.text((y_value + 25, x_value + 25), str(value), (0, 0, 0), font=font)
    img.save("value_board.png")
