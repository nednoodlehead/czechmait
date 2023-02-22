class Tile:
    # creates the tile type
    def __init__(self, tile):
        self.tile = tile

    # used to see nearby tiles through calculations
    def convert_tile(self, amount_letter, amount_number):
        """Takes in a tile, a and returns tile with new amounts added
            :param (int) amount_letter: amount to 'add' to the letter
            :param (int) amount_number: amount to add to the number
        :returns tile with the added amounts
        (h2, -2, 3) -> f5
        """
        # divide the tile into the letter and number separately
        org_let, org_num = self.tile[0], int(self.tile[1])
        # if the result of adding letters either goes above 104 (h) or lower than 97 (a), return None
        if amount_letter + ord(org_let) > 104 or amount_letter + ord(org_let) < 97:
            return None  # in this case, the given numbers are incorrect, but we just return none, like rust err-handlin
        # if the results of adding org number go above 8 or below 1, raise error
        if amount_number + org_num > 8 or amount_number + org_num < 1:
            return None
        # convert the letter -> ord number, add the desired amount, convert back, add new number to it
        return f"{chr(ord(org_let) + amount_letter)}{org_num + amount_number}"

    # used for having a class instance be used as a hash key
    def __hash__(self):
        return hash(self.tile)

    # used mainly in the hashmap so accessing key "a4" will give you Tile("a4")
    def __eq__(self, other):
        return self.tile == other

    # used for calling Tile[0] to access the letter or number in the tile id
    def __getitem__(self, item):
        return self.tile[item]

    # used for printing & debuggin
    def __repr__(self):
        return f"{self.tile}"
