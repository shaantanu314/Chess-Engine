import pygame
import ChessEngine

WIDTH  = 512
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = 64
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

                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            moveMade = True
                            gs.makeMove(validMoves[i])
                            sqSelected = ()
                            playerClicks = []
                            if move.pawnPromotion:
                                gs.board[move.endRow][move.endCol] = move.currPiece[0] + "Q"
                                # CHOOSE THE PIECE FOR PAWN PROMOTION:
                                
                                # promote_to = input("SELECT ON OF THE FOLLOWING FOR PAWN PROMOTION:\n 1) Q for Queen \n 2) R for Rook\n 3) B for Bishop\n 4) N for Knight\n")
                                # print(promote_to)
                    if not moveMade :
                        playerClicks = [sqSelected]
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen,gs,sqSelected,validMoves)
        clock.tick(MAX_FPS)
        pygame.display.flip()

def drawGameState(screen,gs,sqSelected,validMoves):
    # draws the Chess board
    drawBoard(screen,sqSelected,validMoves)
    # draws pieces on the board according to 
    drawPieces(screen,gs.board)



def drawBoard(screen,sqSelected,validMoves):
    colors = [pygame.Color("white"),pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            pygame.draw.rect(screen,color,pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    
    # Highlighting the seleted square effect
    if len(sqSelected):
        if (sqSelected[0]+sqSelected[1])%2 == 1:
            pygame.draw.rect(screen,(211,205,71),pygame.Rect(sqSelected[1]*SQ_SIZE,sqSelected[0]*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        elif (sqSelected[0]+sqSelected[1])%2 == 0:
            pygame.draw.rect(screen,(211,205,71),pygame.Rect(sqSelected[1]*SQ_SIZE,sqSelected[0]*SQ_SIZE,SQ_SIZE,SQ_SIZE))

        # Highlighting all possible movesa for the selected square:    
        for move in validMoves :
            if (move.startRow , move.startCol ) == sqSelected :
                pygame.draw.rect(screen,(26,232,60),pygame.Rect(move.endCol*SQ_SIZE+1,move.endRow*SQ_SIZE+1,SQ_SIZE-2,SQ_SIZE-2))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
            

if __name__ == "__main__":
    main()
