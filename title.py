class Tile:
    def __init__(self, row, column):
        self.row = row
        self.column = column

        self.isMine = False
        self.revealed = False
        self.flagged = False
        self.adjacent = 0