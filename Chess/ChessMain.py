import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()  # initiate PyGame
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()  # Game State
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()
    running = True
    square_selected = ()  # no square selected initially
    player_clicks = []  # track of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # x,y location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if square_selected == (row, col):  # user selected the same square twice
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)
                if len(player_clicks) == 2:  # after second click
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    if move in valid_moves:
                        gs.make_move(move)
                        print(move.get_chess_notation())
                        move_made = True
                    square_selected = ()
                    player_clicks = []  # reset player clicks
            elif e.type == p.KEYDOWN:  # Undo move
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_piece(screen, gs.board)


def draw_board(screen):
    """
    Draw squares on the board
    """
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_piece(screen, board):
    """
    Draw pieces on the board using current GameState.board
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
