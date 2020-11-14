import pygame
import ChessEngine

WIDTH  = 512
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH//DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["wP","wR","wN","wB","wQ","wK","bP","bR","bK","bB","bQ","bN"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("chess_pieces/"+piece+".png"),(SQ_SIZE,SQ_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock  = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    validMoves = gs.getValidMoves()
    moveMade = False
    playerClicks = [] # has the list of player clicks for the current move
    sqSelected   = () # has the coordinates of the currently selected square
    # Game running variable
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_u:
                    gs.undoMove()
                    moveMade = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                row = location[1]//SQ_SIZE
                col = location[0]//SQ_SIZE
                if sqSelected == (row,col):
                    # unselecting the square
                    sqSelected   = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 1:
                    if gs.board[row][col] == "--":
                        sqSelected   = ()
                        playerClicks = []
                # if two clicks were performed (WITHOUT VALIDATION)
                if len(playerClicks)==2:

                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    if move in validMoves:
                        moveMade = True
                        gs.makeMove(move)

                    sqSelected = ()
                    playerClicks = []
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()

def drawGameState(screen,gs):
    # draws the Chess board
    drawBoard(screen)
    # draws pieces on the board according to 
    drawPieces(screen,gs.board)



def drawBoard(screen):
    colors = [pygame.Color("white"),pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            pygame.draw.rect(screen,color,pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
            

if __name__ == "__main__":
    main()
