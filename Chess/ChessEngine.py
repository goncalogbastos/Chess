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
        self.move_functions = {"p": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
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
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)  # calls move function based on piece type
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move:  # White pawn to move
            if self.board[r - 1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 squares move
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # capture to the left
                if self.board[r - 1][c - 1][0] == "b":  # Enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # capture to the right
                if self.board[r - 1][c + 1][0] == "b":  # Enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # Black pawn to move
            if self.board[r + 1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 squares move
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "w":  # Enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == "w":  # Enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def get_rook_moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.white_to_move:
            enemy_color = "b"
        else:
            enemy_color = "w"

        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Valid empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece on square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break  # Friendly piece
                else:
                    break  # off board

    def get_knight_moves(self, r, c, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        if self.white_to_move:
            ally_color = "w"
        else:
            ally_color = "b"

        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # Not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.white_to_move:
            enemy_color = "b"
        else:
            enemy_color = "w"

        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Valid empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece on square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break  # Friendly piece
                else:
                    break  # off board

    def get_queen_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        if self.white_to_move:
            enemy_color = "b"
        else:
            enemy_color = "w"

        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Valid empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece on square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break  # Friendly piece
                else:
                    break  # off board

    def get_king_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        if self.white_to_move:
            enemy_color = "b"
        else:
            enemy_color = "w"

        for d in directions:
            for i in range(1, 2):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Valid empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece on square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break  # Friendly piece
                else:
                    break  # off board


class Move:
    rank_to_row = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    file_to_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
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

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.col_to_file[c] + self.row_to_rank[r]
