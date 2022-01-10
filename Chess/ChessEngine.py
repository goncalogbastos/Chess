class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.moveLog = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"  # square behind becomes empty
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.white_to_move = not self.white_to_move  # Swap players

    def undo_move(self):
        if len(self.moveLog) != 0:  # Make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = [Move((6, 4), (4, 4), self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.white_to_move) and (turn == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == "p":
                        self.get_pawn_moves(r, c, moves)
                    elif piece == "R":
                        self.get_rook_moves(r, c, moves)
                    elif piece == "N":
                        self.get_knight_moves(r, c, moves)
                    elif piece == "B":
                        self.get_bishop_moves(r, c, moves)
                    elif piece == "Q":
                        self.get_queen_moves(r, c, moves)
                    elif piece == "K":
                        self.get_king_moves(r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        pass

    def get_rook_moves(self, r, c, moves):
        pass

    def get_knight_moves(self, r, c, moves):
        pass

    def get_bishop_moves(self, r, c, moves):
        pass

    def get_queen_moves(self, r, c, moves):
        pass

    def get_king_moves(self, r, c, moves):
        pass


class Move:
    rank_to_row = {
        "1": 7,
        "2": 6,
        "3": 5,
        "4": 4,
        "5": 3,
        "6": 2,
        "7": 1,
        "8": 0
    }
    file_to_col = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7
    }
    row_to_rank = {v: k for k, v in rank_to_row.items()}
    col_to_file = {v: k for k, v in file_to_col.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_ID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        print(self.move_ID)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.col_to_file[c] + self.row_to_rank[r]
