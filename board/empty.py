class Empty:
    # used in the queries of what occupies a tile, returns None to that query. This is the alternative to error handing
    # within the queries themselves
    color = None
    def __repr__(self):
        return "EMPTY TILE INSTANCE"
