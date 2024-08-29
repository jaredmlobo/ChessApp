import numpy as np
import pandas as pd
from pieces import *

class chess_board(pd.DataFrame):
    
    def __init__(self, df = None) -> None:
        
        if isinstance(df, pd.DataFrame): 
            transfer = df.to_dict()
            super().__init__(transfer)

        else:
            super().__init__(columns=[1,2,3,4,5,6,7,8], index=reversed(range(8)))
            self.rename({0:8, 1:7, 2:6, 3:5, 5:3, 6:2, 7:1}, inplace=True)
            self.loc[8] = [rook('w'), knight('w'), bishop('w'), queen('w'), king('w'), bishop('w'), knight('w'), rook('w')]
            self.loc[7] = [pawn('w')]
            # board.loc[3] = [rook('w'), '',pawn('b'),'',king('w'),'', '', rook('w')]
            self.loc[2] = [pawn('b')]
            self.loc[1] = [rook('b'), knight('b'), bishop('b'), queen('b'), king('b'), bishop('b'), knight('b'), rook('b')]

            self.fillna('', inplace=True)

    def get_square(self, x, y):
        if x<1 or x>8 or y<1 or y>8:
            return None
        return self.loc[y][x]
    
    def get_moves(self, x, y, game, show = False):
        piece = self.get_square(x,y)
        print('piece = ', piece)
        if piece == None or piece == '':
            return []
        else:
            moves = piece.find_moves(self, x, y)

        for x2,y2 in moves:
            if self.check_move_for_checks(game, x, y, x2, y2) == False:
                moves.remove((x2, y2))

        if show: 
            board_copy = self.copy()
            for x,y in moves:
                board_copy.loc[y,x] = 'X' + str(board_copy.loc[y][x])

            display(board_copy)

        return moves
    
    def move(self, game, x1, y1, x2, y2, show = False):

        moves = self.get_moves(x1,y1, game)
        print(moves)
        if (x2,y2) not in moves:
            print('invalid move')
            return False
        else:
            print('valid move')
            self.move_piece(x1, y1, x2, y2)
            

        if isinstance(piece, (rook, king)):
            piece.moved = True
        
        if show:
            board_copy = self.copy()
            display(board_copy)
        
        return True

    def move_piece(self, x1, y1, x2, y2):
        """Function to physically move the piece on the board (regardless if legal or not)"""
        piece = self.get_square(x1,y1)
        if isinstance(piece, pawn) and ((piece.color == 'w' and y2 == 1) or (piece.color == 'b' and y2 == 8)):
            self.loc[y2,x2] = queen(piece.color)
            self.loc[y1,x1] = ''
        # en pessant
        elif isinstance(piece, pawn) and (x2 != x1) and self.get_square(x2,y2) =='':
            self.loc[y2,x2] = self.loc[y1,x1] 
            self.loc[y1,x1] = ''
            self.loc[y1,x2] = ''
        else:
            self.loc[y2,x2] = self.loc[y1,x1] 
            self.loc[y1,x1] = ''

            # castling
            if isinstance(piece, king) and abs(x2-x1) == 2:
                if x2 == 7: 
                    self.loc[y2,6] = self.loc[y1,8]
                    self.loc[y1,8] = ''
                elif x2 == 3:
                    self.loc[y2,4] = self.loc[y1,1]
                    self.loc[y1,1] = ''
    
    def get_attacks(self, color):
        color_attacks = set()
        for y, row in self.iterrows():
            for x,piece in row.items():
                if piece != '' and piece.color == color:
                    print('checking attacks '+ str(x)+ str(y)+str(piece))

                    attacks = piece.find_moves(self,x,y, attacks_only=True)
                    print(attacks)
                    color_attacks.update(attacks)

        return color_attacks
    
    def check_move_for_checks(self, game, x1, y1, x2, y2):
        """checks to make sure king is not put in check by a move"""
        color = self.get_square(x1,y1).color
        board_copy = self.board_copy()
        board_copy.move_piece(x1, y1, x2, y2)
        print(board_copy)

        if color == 'w': 
            look_for_checks = board_copy.get_attacks(game, 'b')
        else:
            look_for_checks = board_copy.get_attacks(game, 'w')
        print("move checking: ",x2,y2)
        print('look_for_checks', look_for_checks)
        for x,y in look_for_checks:
            piece = self.get_square(x,y)
            
            if isinstance(piece, king) and piece.color == color:
                return False
            
        return True
    
    def board_copy(self):
        new_board_df = self.copy(deep=True)
        new_board = chess_board(new_board_df)

        return new_board

class game:

    def __init__(self) -> None:

        self.board = chess_board()
        self.status = 'none'
        self.turn = 'w'
        self.last_move = -99, -99, -99, -99

    def get_moves(self, x, y, show = False):
        return self.board.get_moves(x, y, self, show)

    def move(self, x1, y1, x2, y2, show = False):
        piece = self.board.get_square(x1, y1)
        if piece != '' and piece.color != self.turn:
            print('Wrong turn')
            return
        
        # try to move piece
        success = self.board.move(self, x1, y1, x2, y2, show)

        # look for new checks if move was completed
        if success:

            if self.turn == 'w':
                self.turn = 'b'
                look_for_checks = self.board.get_attacks(self, 'w')
            else:
                self.turn = 'w'
                look_for_checks = self.board.get_attacks(self, 'b')
            self.last_move = (x1,y1,x2,y2)

            for x,y in look_for_checks:
                piece = self.board.get_square(x,y)
                if isinstance(piece, king) and piece.color == self.turn:
                    self.status = 'check'
    
    # def checkout_move(self, x1, y1, x2, y2):
    #     board_copy = self.board.copy()
    #     board_copy.move(x1, y1, x2, y2)
