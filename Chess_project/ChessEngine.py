class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","bR","--","--","--","--"],
            ["--","--","--","--","wR","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
            ]
        self.WhitetoMove = True
        self.moveLog = []
        self.moveFunctions = {"P":self.getPawnMoves , "R":self.getRookMoves , "N":self.getKnightMoves ,
                            "B":self.getBishopMoves ,"K":self.getKingMoves , "Q":self.getQueenMoves}

    # takes in the move object and executes it non the board
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.currPiece
        self.moveLog.append(move)
        print(move.getNotation())
        self.WhitetoMove = not self.WhitetoMove
    
    # undoing the move onboard
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            move.startRow, move.endRow = move.endRow, move.startRow
            move.startCol , move.endCol = move.endCol , move.startCol
            self.makeMove(move)
            self.moveLog.pop()
            self.WhitetoMove = not self.WhitetoMove

    def getValidMoves(self):
        return self.allPossibleMoves()
    
    def allPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'w' and self.WhitetoMove or turn == 'b' and not self.WhitetoMove):
                    # generate moves for this piece
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
    
        return moves

    # generate moves for the Pawn piece
    def getPawnMoves(self,r,c,moves):
        if self.WhitetoMove :
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if self.board[r-2][c] == "--" and r==6:
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0 :
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7 :
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        else :
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if self.board[r+2][c] == "--" and r==1:
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0 :
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7 :
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))
    
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
        pass

    # generates moves for the Bishop piece
    def getBishopMoves(self,r,c,moves):
        pass

    # generates moves for the King piece
    def getKingMoves(self,r,c,moves):
        pass

    # generates moves for the Queen piece
    def getQueenMoves(self,r,c,moves):
        pass
class Move():

    rankstoRow = {"1":7,"2":6,"3":5,"4":4,
                  "5":3,"6":2,"7":1,"8":0}
    rowtoRank  = {v:k for k,v in rankstoRow.items()}
    filestoCol = {"h":7,"g":6,"f":5,"e":4,
                  "d":3,"c":2,"b":1,"a":0}
    coltoFiles  = {v:k for k,v in filestoCol.items()}

    def __init__(self,startpos,endpos,board):
        self.startRow = startpos[0]
        self.startCol = startpos[1]
        self.endRow   = endpos[0]
        self.endCol   = endpos[1]
        self.currPiece = board[self.startRow][self.startCol]
        self.moveID = 1000*self.startRow + 100*self.startCol + 10*self.endRow + self.endCol

    def __eq__(self, other):
        if isinstance(other , Move):
            return self.moveID == other.moveID

    def getNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return  self.coltoFiles[c] + self.rowtoRank[r]


