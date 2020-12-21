class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
            ]
        self.WhitetoMove = True
        self.moveLog = []
        self.moveFunctions = {"P":self.getPawnMoves , "R":self.getRookMoves , "N":self.getKnightMoves ,
                            "B":self.getBishopMoves ,"K":self.getKingMoves , "Q":self.getQueenMoves}
        self.CheckMate = False
        self.StaleMate = False
        self.whiteKingpos = (7,4)
        self.blackKingpos = (0,4)
        # Enpassant Square 
        self.enpassantSquare = ()
        # Manage the castling right
        self.currentCastlingrights = CastlingRights(True,True,True,True)
        self.castlingrightlogs = [CastlingRights(True,True,True,True)] # adding the initial state



    # takes in the move object and executes it non the board
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.currPiece
        self.moveLog.append(move)
        # print(move.getNotation())
        if (move.pawnPromotion):
            self.board[move.endRow][move.endCol] = move.currPiece[0] + "Q"
        self.WhitetoMove = not self.WhitetoMove
        if move.currPiece == "wK":
            self.whiteKingpos = (move.endRow,move.endCol)
        elif move.currPiece == "bK":
            self.blackKingpos = (move.endRow,move.endCol)

        if move.currPiece[1] == "P" and abs(move.startRow - move.endRow) == 2 :
            self.enpassantSquare = ((move.startRow + move.endRow)//2 , move.endCol)
        else :
            self.enpassantSquare = ()

        # Handling the enpassnat moves:
        if move.enpassantMove :
            self.board[move.startRow][move.endCol] = "--"
            self.enpassantSquare = ()

        # Handling Castling moves
        self.updateCastlingRights(move)
        self.castlingrightlogs.append(CastlingRights(self.currentCastlingrights.wks,self.currentCastlingrights.wqs,self.currentCastlingrights.bks,self.currentCastlingrights.bqs))
        #self.castlingrightlogs.append(CastlingRights(True,True,True,True))
        if move.castlingMove :
            if (move.endCol - move.startCol == 2) :
                if self.WhitetoMove :
                    self.board[7][7] = "--"
                    self.board[move.startRow][move.endCol - 1] = "wR"
                else :
                    self.board[0][7] = "--"
                    self.board[move.startRow][move.endCol - 1] = "bR"
            else :
                if self.WhitetoMove :
                    self.board[7][0] = "--"
                    self.board[move.startRow][move.endCol + 1] = "wR"
                else :
                    self.board[0][0] = "--"
                    self.board[move.startRow][move.endCol + 1] = "bR"



    # undoing the move onboard
    def undoMove(self):
        if len(self.moveLog) != 0:
            
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.currPiece
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            if move.currPiece == "wK":
                self.whiteKingpos = (move.startRow,move.startCol)   
            elif move.currPiece == "bK":
                self.blackKingpos = (move.startRow,move.startCol)
            
            # undo enpassant moves
            if move.enpassantMove :
                if self.WhitetoMove :
                    self.board[move.startRow][move.endCol] = "wP"
                else :
                    self.board[move.startRow][move.endCol] = "bP"
            
            # undo castling moves
            if move.castlingMove:
                if (move.endCol - move.startCol == 2) :
                    if self.WhitetoMove :
                        self.board[7][7] = "wR"
                        self.board[move.startRow][move.endCol - 1] = "--"
                    else :
                        self.board[0][7] = "bR"
                        self.board[move.startRow][move.endCol - 1] = "--"
                else :
                    if self.WhitetoMove :
                        self.board[7][0] = "wR"
                        self.board[move.startRow][move.endCol + 1] = "--"
                    else :
                        self.board[0][0] = "bR"
                        self.board[move.startRow][move.endCol + 1] = "--"
            self.castlingrightlogs.pop()
            self.currentCastlingrights = self.castlingrightlogs[-1]

            self.WhitetoMove = not self.WhitetoMove

        
    def updateCastlingRights(self,move):
        if move.currPiece == "wK":
            self.currentCastlingrights.wks = False
            self.currentCastlingrights.wqs = False
        if move.currPiece == "bK":
            self.currentCastlingrights.bks = False
            self.currentCastlingrights.bqs = False
        if move.currPiece == "wR":
            if move.startCol == 7:
                self.currentCastlingrights.wks = False
            else:
                self.currentCastlingrights.wqs = False
        if move.currPiece == "bR":
            if move.startCol == 7:
                self.currentCastlingrights.bks = False
            else:
                self.currentCastlingrights.bqs = False

    def isCheck(self):
        if self.WhitetoMove:
            return self.isunderAttack(self.whiteKingpos[0],self.whiteKingpos[1])
        else:
            return self.isunderAttack(self.blackKingpos[0],self.blackKingpos[1])

    def isunderAttack(self,r,c):
        self.WhitetoMove = not self.WhitetoMove
        oppMoves = self.allPossibleMoves()
        self.WhitetoMove = not self.WhitetoMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getValidMoves(self):
        temp_enpassantSquare = self.enpassantSquare
        temp_castlingState   = CastlingRights(self.currentCastlingrights.wks,self.currentCastlingrights.wqs,self.currentCastlingrights.bks,self.currentCastlingrights.bqs)
        moves = self.allPossibleMoves()
        if self.WhitetoMove:
            self.getCastlingMoves(self.whiteKingpos[0],self.whiteKingpos[1],moves)
        else :
            self.getCastlingMoves(self.blackKingpos[0],self.blackKingpos[1],moves) 
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            self.WhitetoMove = not self.WhitetoMove
            if self.isCheck():
                moves.remove(moves[i])
            self.WhitetoMove = not self.WhitetoMove
            self.undoMove()

        if len(moves) == 0:
            if self.isCheck():
                self.CheckMate = True
            else:
                self.StaleMate = True
        else:
            self.CheckMate = False
            self.StaleMate = False

        self.enpassantSquare = temp_enpassantSquare
        self.currentCastlingrights = temp_castlingState

        return moves

    
    
    def allPossibleMoves(self):      
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if((turn == 'w' and self.WhitetoMove) or (turn == 'b' and not self.WhitetoMove)):
                    # generate moves for this piece
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)

        return moves

    # generate moves for the Pawn piece
    def getPawnMoves(self,r,c,moves):
        if self.WhitetoMove :
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6:
                    if self.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0 :
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                if (r-1,c-1) == self.enpassantSquare :
                    moves.append(Move((r,c),(r-1,c-1),self.board,enpassantMove=True))
            if c+1 <= 7 :
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                if (r-1,c+1) == self.enpassantSquare :
                    moves.append(Move((r,c),(r-1,c+1),self.board,enpassantMove=True))
        else :
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if (r==1):  
                    if self.board[r+2][c] == "--":
                        moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0 :
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                if (r+1,c-1) == self.enpassantSquare :
                    moves.append(Move((r,c),(r+1,c-1),self.board,enpassantMove=True))
            if c+1 <= 7 :
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                if (r+1,c+1) == self.enpassantSquare :
                    moves.append(Move((r,c),(r+1,c+1),self.board,enpassantMove=True))
    
    # generates moves for the Rook piece
    def getRookMoves(self,r,c,moves):

        # validating moves to move  along a row
        i = 1
        while  c+i<8:
            if self.board[r][c+i]=="--" :
                moves.append(Move((r,c),(r,c+i),self.board))
                i+=1
            else:
                break
        if c+i < 8:
            if (self.board[r][c+i][0] == "b" and self.WhitetoMove ) or (self.board[r][c+i][0] == "w" and not self.WhitetoMove):
                moves.append(Move((r,c),(r,c+i),self.board))
        i = 1
        while c-i>=0:
            if self.board[r][c-i]=="--" :
                moves.append(Move((r,c),(r,c-i),self.board))
                i+=1
            else:
                break
        if c-i >= 0:
            if (self.board[r][c-i][0] == "b" and self.WhitetoMove ) or (self.board[r][c-i][0] == "w" and not self.WhitetoMove):
                moves.append(Move((r,c),(r,c-i),self.board))

        # validating moves to move  along a column
        i = 1
        while  r+i<8:
            if self.board[r+i][c]=="--" :
                moves.append(Move((r,c),(r+i,c),self.board))
                i+=1
            else:
                break
        if r+i < 8:
            if (self.board[r+i][c][0] == "b" and self.WhitetoMove ) or (self.board[r+i][c][0] == "w" and not self.WhitetoMove):
                moves.append(Move((r,c),(r+i,c),self.board))
        i = 1
        while r-i>=0:
            if self.board[r-i][c]=="--" :
                moves.append(Move((r,c),(r-i,c),self.board))
                i+=1
            else:
                break
        if r-i >= 0:
            if (self.board[r-i][c][0] == "b" and self.WhitetoMove ) or (self.board[r-i][c][0] == "w" and not self.WhitetoMove):
                moves.append(Move((r,c),(r-i,c),self.board))

    # generates moves for the Knight piece
    def getKnightMoves(self,r,c,moves):
        positions = {(r+2,c+1),(r+2,c-1),(r-2,c+1),(r-2,c-1),(r+1,c+2),(r+1,c-2),(r-1,c+2),(r-1,c-2)} 
        for pos in positions:
            if pos[0]>=0 and pos[0]<8 and pos[1]>=0 and pos[1]<8:
                if self.board[pos[0]][pos[1]] == "--":
                    moves.append(Move((r,c),(pos[0],pos[1]),self.board))
                if (self.board[pos[0]][pos[1]][0] == "b" and self.WhitetoMove ) or (self.board[pos[0]][pos[1]][0] == "w" and not self.WhitetoMove):
                    moves.append(Move((r,c),(pos[0],pos[1]),self.board))
  
            

    # generates moves for the Bishop piece
    def getBishopMoves(self,r,c,moves):
        

        i = 1
        while r+i<8 and c+i<8:
            if self.board[r+i][c+i] == "--":
                moves.append(Move((r,c),(r+i,c+i),self.board))
                i+=1
            else:
                break
        if r+i<8 and c+i<8:
            if (self.board[r+i][c+i][0] == "b" and self.WhitetoMove ) or (self.board[r+i][c+i][0] == "w" and not self.WhitetoMove):
                moves.append(Move((r,c),(r+i,c+i),self.board)) 
        
        i=1
        while r-i>=0 and c-i>=0:
            if self.board[r-i][c-i] == "--":
                moves.append(Move((r,c),(r-i,c-i),self.board))
                i+=1
            else:
                break
        if r-i>=0 and c-i>=0:
            if (self.board[r-i][c-i][0] == "b" and self.WhitetoMove ) or (self.board[r-i][c-i][0] == "w" and not self.WhitetoMove):
                moves.append(Move((r,c),(r-i,c-i),self.board)) 

        #########################################
        i = 1
        while r+i<8 and c-i>=0:
            if self.board[r+i][c-i] == "--":
                moves.append(Move((r,c),(r+i,c-i),self.board))
                i+=1
            else:
                break
        if r+i<8 and c-i>=0:
            if (self.board[r+i][c-i][0] == "b" and self.WhitetoMove ) or (self.board[r+i][c-i][0] == "w" and not self.WhitetoMove):
                moves.append(Move((r,c),(r+i,c-i),self.board)) 
        
        i=1
        while r-i>=0 and c+i<8:
            if self.board[r-i][c+i] == "--":
                moves.append(Move((r,c),(r-i,c+i),self.board))
                i+=1
            else:
                break
        if r-i>=0 and c+i<8:
            if (self.board[r-i][c+i][0] == "b" and self.WhitetoMove ) or (self.board[r-i][c+i][0] == "w" and not self.WhitetoMove):
                moves.append(Move((r,c),(r-i,c+i),self.board))
    # generates moves for the King piece
    def getKingMoves(self,r,c,moves):
        positions = {(r+1,c+1),(r+1,c-1),(r-1,c+1),(r-1,c-1),(r+1,c),(r-1,c),(r,c+1),(r,c-1)} 
        for pos in positions:
            if pos[0]>=0 and pos[0]<8 and pos[1]>=0 and pos[1]<8:
                if self.board[pos[0]][pos[1]] == "--":
                    moves.append(Move((r,c),(pos[0],pos[1]),self.board))
                if (self.board[pos[0]][pos[1]][0] == "b" and self.WhitetoMove ) or (self.board[pos[0]][pos[1]][0] == "w" and not self.WhitetoMove):
                    moves.append(Move((r,c),(pos[0],pos[1]),self.board))
        

    def getCastlingMoves(self,r,c,moves):
        if self.isCheck():
            return
        if ((self.currentCastlingrights.bks and not self.WhitetoMove) or (self.currentCastlingrights.wks and self.WhitetoMove)):
            if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
                if (not self.isunderAttack(r,c+1)) and (not self.isunderAttack(r,c+2)):
                    moves.append(Move((r,c),(r,c+2),self.board,castlingMove = True))

        if ((self.currentCastlingrights.bqs and not self.WhitetoMove) or (self.currentCastlingrights.wqs and self.WhitetoMove)):
            if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
                if (not self.isunderAttack(r,c-1)) and (not self.isunderAttack(r,c-2)):
                    moves.append(Move((r,c),(r,c-2),self.board,castlingMove = True))

    # generates moves for the Queen piece
    def getQueenMoves(self,r,c,moves):
        # using the same functions as for bishop and rook because the moves are same
        self.getBishopMoves(r,c,moves) 
        self.getRookMoves(r,c,moves)


# class which stores the castling rights for the particular state of the game
class CastlingRights():
    def __init__(self,wks,wqs,bks,bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs



class Move():

    rankstoRow = {"1":7,"2":6,"3":5,"4":4,
                  "5":3,"6":2,"7":1,"8":0}
    rowtoRank  = {v:k for k,v in rankstoRow.items()}
    filestoCol = {"h":7,"g":6,"f":5,"e":4,
                  "d":3,"c":2,"b":1,"a":0}
    coltoFiles  = {v:k for k,v in filestoCol.items()}

    def __init__(self,startpos,endpos,board,enpassantMove = False,castlingMove = False):
        self.startRow = startpos[0]
        self.startCol = startpos[1]
        self.endRow   = endpos[0]
        self.endCol   = endpos[1]
        self.currPiece = board[self.startRow][self.startCol]
        self.moveID = 1000*self.startRow + 100*self.startCol + 10*self.endRow + self.endCol
        self.pieceCaptured = board[self.endRow][self.endCol]
    
        # PAWN PROMOTION
        self.pawnPromotion = False
        if ((self.currPiece == "wP" and self.endRow == 0 ) or (self.currPiece == "bP" and self.endRow == 7)):
            self.pawnPromotion = True

        # ENPASSANT MOVE
        self.enpassantMove = enpassantMove 
        
        # CASTLING MOVE
        self.castlingMove = castlingMove


    def __eq__(self, other):
        if isinstance(other , Move):
            return self.moveID == other.moveID

    def getNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return  self.coltoFiles[c] + self.rowtoRank[r]


