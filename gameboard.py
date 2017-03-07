"""GameBoard of Sodoku."""


INTTOODOMETER = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6",
                 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D",
                 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K",
                 21: "L", 22: "M", 23: "N", 24: "O", 25: "P", 26: "Q", 27: "R",
                 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y",
                 35: "Z"}


class GameBoard:

    def __init__(self, N=None, p=None, q=None, board=None):
        """
        Init a game board.
        p, q, N represent the dimensions of a game board.
        Assuming a game board has values p = 3, q = 4, N = 12,
        an empty board will look like this.

        [] [] [] [] | [] [] [] [] | [] [] [] []
        [] [] [] [] | [] [] [] [] | [] [] [] []
        [] [] [] [] | [] [] [] [] | [] [] [] []
        ---------------------------------------
        [] [] [] [] | [] [] [] [] | [] [] [] []
        [] [] [] [] | [] [] [] [] | [] [] [] []
        [] [] [] [] | [] [] [] [] | [] [] [] []
        ---------------------------------------
        [] [] [] [] | [] [] [] [] | [] [] [] []
        [] [] [] [] | [] [] [] [] | [] [] [] []
        [] [] [] [] | [] [] [] [] | [] [] [] []
        ---------------------------------------
        [] [] [] [] | [] [] [] [] | [] [] [] []
        [] [] [] [] | [] [] [] [] | [] [] [] []
        [] [] [] [] | [] [] [] [] | [] [] [] []
        """
        if (N < 1 or (N != p * q)):
            print('Board parameters invalid. ' +
                  'Creating a 9x9 sudoku file instead.')
            self.p = 3
            self.q = 3
            self.N = 9
            self.board = [[0 for j in range(9)] for i in range(9)]
        else:
            self.p = p  # number of rows in a block && number of blocks per row
            self.q = q  # number of cols in a block && number of blocks per col
            self.N = N  # number of cells in a block && edge length of NxN

            if board is None:
                self.board = [[0 for j in range(9)] for i in range(9)]
            else:
                self.board = board

    # --------- String Representation ---------
    def __str__(self):
        output = "N:" + str(self.N) + "\tp:" + str(self.p) + "\tq:" \
            + str(self.q) + "\n"
        for i in range(self.N):
            for j in range(self.N):
                try:
                    output += INTTOODOMETER[self.board[i][j]] + " "
                except IndexError:
                    pass

                if (j + 1) % self.q == 0 and j != 0 and j != (self.N - 1):
                    output += "| "

            output += "\n"
            if (i + 1) % self.p == 0 and i != 0 and i != (self.N - 1):
                for k in range(self.N + self.p - 1):
                    output += "- "
                output += "\n"
        return output
