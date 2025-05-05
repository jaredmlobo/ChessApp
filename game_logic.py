import numpy as np
import pandas as pd
from pieces import *
from utils import *
import warnings


class chess_board(pd.DataFrame):
    """ Object Replicating a physical chess board, houses and moves pieces"""

    def __init__(self, df = None) -> None:
        
        if isinstance(df, pd.DataFrame): 
            transfer = df.to_dict()
            super().__init__(transfer)

        else:
            super().__init__(columns=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], index=reversed(range(1,9)))

            self.loc[1] = [rook('w'), knight('w'), bishop('w'), queen('w'), king('w'), bishop('w'), knight('w'), rook('w')]
            self.loc[2] = [pawn('w')]
            # board.loc[3] = [rook('w'), '',pawn('b'),'',king('w'),'', '', rook('w')]
            self.loc[7] = [pawn('b')]
            self.loc[8] = [rook('b'), knight('b'), bishop('b'), queen('b'), king('b'), bishop('b'), knight('b'), rook('b')]

            self.fillna('', inplace=True)

        
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=UserWarning)
            self.last_move = None, None


    def get_square(self, *arg):
        """
        Return the piece (or blank) at a given position
        """
        try:
            if len(arg) == 1:
                [col,y] = list(arg[0])
            else: 
                col = get_column_letter(arg[0])
                y = arg[1]
            return self.loc[int(y), col]
        except (IndexError, KeyError): 
            return None
    
    
    def set_square(self, pos, piece = ''):
        """
        Set a given positon to be a given piece
        """
        [col,y] = list(pos)
        self.loc[int(y),col] = piece
    
    def get_moves(self, pos, game, show = False):
        """
        Get the valid moves for the piece at position pos
        """
        # check if the position provided is a valid piece
        piece = self.get_square(pos)
        if piece == None or piece == '':
            print('Not a piece')
            return []
        # if valid, get the functinally allowed moves for that piece
        else:
            x,y = board_to_grid(pos)
            moves = piece.find_moves(self, x,y)

        print(moves)
        moves = [pos2 for pos2 in moves if self.check_move_for_checks(game, pos, pos2)]
        print(moves)

        for i in range(len(moves)):
            #convert moves output back to board notation 
            x,y = moves[i] 
            pos2 = grid_to_board(x,y)
            moves[i] = pos2

        if show: 
            board_copy = self.copy()
            for x,y in moves:
                board_copy.set_square(pos, 'X' + str(board_copy.loc[y][x]))

            print(board_copy)

        return moves
    
    
    def move(self, game, pos1, pos2, show = False):
        """
        Attempt to move the piece on position pos1 to pos2
        """

        moves = self.get_moves(pos1, game)
        # print(moves)
        if (pos2) not in moves:
            print('invalid move')
            return False
        else:
            self.move_piece(pos1, pos2)
            

        if isinstance(piece, (rook, king)):
            piece.moved = True
        
        if show:
            board_copy = self.copy()
            print(board_copy)

        self.last_move = (pos1,pos2)
        
        return True
    

    def move_piece(self, pos1, pos2):
        """Function to physically move the piece on the board (regardless if legal or not)"""
        x1,y1 = board_to_grid(pos1)
        x2, y2 = board_to_grid(pos2)
        col2 = get_column_letter(x2)

        piece = self.get_square(pos1)

        #pawn promotion
        if isinstance(piece, pawn) and ((piece.color == 'w' and y2 == 1) or (piece.color == 'b' and y2 == 8)):
            self.set_square(pos2, queen(piece.color))
            self.set_square(pos1)

        # en pessant
        elif isinstance(piece, pawn) and (x2 != x1) and self.get_square(pos2) =='':
            self.set_square(pos2, piece) 
            self.set_square(pos1)
            self.set_square(col2 + str(y1))

        else:
            self.set_square(pos2, piece) 
            self.set_square(pos1)

            # if castling: move the rook
            if isinstance(piece, king) and abs(x2-x1) == 2:
                # king side castle
                if x2 == 7: 
                    self.set_square('F'+str(y2), self.get_square('H'+str(y1)))
                    self.set_square('H'+str(y1))
                # queen side castle
                elif x2 == 3:
                    self.set_square('D'+str(y2), self.get_square('A'+str(y1)))
                    self.set_square('A'+str(y1))

    
    def get_attacks(self, color):
        color_attacks = set()
        for y, row in self.iterrows():
            for x,piece in row.items():
                x = get_column_number(x)
                if piece != '' and piece.color == color:
                    # print('checking attacks '+ str(x)+ str(y)+str(piece))

                    attacks = piece.find_moves(self,x,y, attacks_only=True)
                    # print(attacks)
                    color_attacks.update(attacks)

        return color_attacks
    
    
    def check_move_for_checks(self, game, pos1, pos2):
        """checks to make sure king is not put in check by a move"""
        # format pos2
        pos2 = grid_to_board(pos2[0], pos2[1])
        
        color = self.get_square(pos1).color
        board_copy = self.board_copy()
        board_copy.move_piece(pos1, pos2)
        # print(board_copy)

        if color == 'w': 
            look_for_checks = board_copy.get_attacks('b')
        else:
            look_for_checks = board_copy.get_attacks('w')
        # print("move checking: ",x2,y2)
        # print('look_for_checks', look_for_checks)
        for (x,y) in look_for_checks:
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

    def get_moves(self, pos, show = False):
        """
        Get the possible moves for the piece at position pos
        """
        return self.board.get_moves(pos, self, show)

    def move(self, pos1, pos2, show = False):
        """
        Attempt to move the piece on pos1 to pos2
        """
        piece = self.board.get_square(pos1)
        if piece != '' and piece.color != self.turn:
            print('Wrong turn')
            return
        
        # try to move piece
        success = self.board.move(self, pos1, pos2, show)

        # look for new checks if move was completed
        if success:

            if self.turn == 'w':
                self.turn = 'b'
                look_for_checks = self.board.get_attacks('w')
            else:
                self.turn = 'w'
                look_for_checks = self.board.get_attacks('b')

            for x,y in look_for_checks:
                piece = self.board.get_square(x,y)
                if isinstance(piece, king) and piece.color == self.turn:
                    self.status = 'check'
    
    def execute_move_list(self, move_list):
        """
        Execute a provided list of moves on the game
        """
        for pos1, pos2 in move_list:
            self.move(pos1, pos2)

def play_chess():
    """
    Function to handle running the game in the command line
    Is this the best way to do this?
    """
    new_game = game()
    print(new_game.board)
    while True:
        user_input = input(f"{new_game.turn} player turn: Enter command (Action-inputs)")
        print(user_input)
        parts = user_input.split('-') 
        action = parts[0]
        print(action)

        if action == 'quit':
            break
        elif action == 'move':
            x1,y1,x2,y2 = parts[1].split(',')
            new_game.move(int(x1),int(y1),int(x2),int(y2))
            print(new_game.board)


print(__name__)
if __name__ == '__main__':
    play_chess()