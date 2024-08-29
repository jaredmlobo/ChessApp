class piece:

    def __init__(self, color, ) -> None:
        self.color = color

    def __str__(self):
        piece_dict = {'bking':'♔', 
                'bqueen': '♕', 
                'brook': '♖', 
                'bbishop':'♗', 
                'bknight' : '♘', 
                'bpawn':'♙', 
                'wking': '♚',
                'wqueen': '♛',
                'wrook':'♜', 
                'wbishop':'♝', 
                'wknight': '♞',
                'wpawn' : '♟' 
                }
        return piece_dict[self.get_piece_type()]

    def get_piece_type(self):
        return self.color + self.__class__.__name__
    
    def valid_horizontal_moves(self, board, x, y, lim = None, attacks_only=False):
        """Gets valid horizontal moves in left/right direction

        Parameters
        ----------
        self : piece object (rook, queen, or king)
            chess piece moves are evaluated on
        board : board
            chess board object 
        x : int 
            x position of the piece
        y : int
            y position of the piece

        Returns
        -------
        list
            a list of tuples of (x, y) positions of valid moves
        """
        moves = []

        right_lim = 8-x
        left_lim = x-1

        def right_func(x, y, i):
            return x+i, y
        def left_func(x, y, i):
            return x-i, y

        if lim:
            right_lim, left_lim, = lim, lim
        
        moves.extend(self.valid_moves_helper(board, x, y, right_func, right_lim, attacks_only=attacks_only))
        moves.extend(self.valid_moves_helper(board, x, y, left_func, left_lim, attacks_only=attacks_only))

        return moves
    
    def valid_vertical_moves(self, board, x, y, lim = None, attacks_only=False):
        """Gets valid vertical moves in up/down direction

        Parameters
        ----------
        self : piece object (rook, queen, or king)
            chess piece moves are evaluated on
        board : board
            chess board object 
        x : int 
            x position of the piece
        y : int
            y position of the piece

        Returns
        -------
        list
            a list of tuples of (x, y) positions of valid moves
        """
        moves = []

        up_lim = 8-y
        down_lim = y-1

        def up_func(x, y, i):
            return x, y + i
        def down_func(x, y, i):
            return x, y - i
        
        if lim:
            up_lim, down_lim, = lim, lim
        
        moves.extend(self.valid_moves_helper(board, x, y, up_func, up_lim, attacks_only=attacks_only))
        moves.extend(self.valid_moves_helper(board, x, y, down_func, down_lim, attacks_only=attacks_only))

        return moves
    
    def valid_diagonal_moves(self, board, x, y, lim= None, attacks_only=False):
        """Gets valid diagonal moves in left/right direction

        Parameters
        ----------
        self : piece object (bishop, queen, or king)
            chess piece moves are evaluated on
        board : board
            chess board object 
        x : int 
            x position of the piece
        y : int
            y position of the piece

        Returns
        -------
        list
            a list of tuples of (x, y) positions of valid moves
        """
        moves = []

        up_right_lim = min(8-x, 8-y)
        down_right_lim = min(8-x, y-1)
        up_left_lim = min(x-1, 8-y)
        down_left_lim = min(x-1, y-1)

        def up_right_func(x, y, i):
            return x + i, y + i
        def down_right_func(x, y, i):
            return x + i, y - i
        def up_left_func(x, y, i):
            return x - i, y + i
        def down_left_func(x, y, i):
            return x - i, y - i
        
        if lim:
            up_right_lim, down_right_lim, up_left_lim, down_left_lim = lim, lim, lim, lim
        
        moves.extend(self.valid_moves_helper(board, x, y, up_right_func, up_right_lim, attacks_only=attacks_only))
        moves.extend(self.valid_moves_helper(board, x, y, down_right_func, down_right_lim, attacks_only=attacks_only))
        moves.extend(self.valid_moves_helper(board, x, y, up_left_func, up_left_lim, attacks_only=attacks_only))
        moves.extend(self.valid_moves_helper(board, x, y, down_left_func, down_left_lim, attacks_only=attacks_only))

        return moves

    def valid_moves_helper(self, board, x, y, xy_func, lim, attacks_only = None, pawn_take = False):
        """Gets valid moves in a provided direction up to a specified limit

        Parameters
        ----------
        self : piece object (rook, bishop, queen, or king)
            chess piece moves are evaluated on
        board : board
            chess board object 
        x : int 
            x position of the piece
        y : int
            y position of the piece
        xy_func : function
            function that returns the next square location in a direction given the current square
        lim : int
            1 + the limit of squares to check in a given direction  

        Returns
        -------
        list
            a list of tuples of (x, y) positions of valid moves
        """
        moves = []

        block_color = self.color


        for i in range(1, lim+1):
            xi, yi = xy_func(x, y, i)
            new_square = board.get_square(xi, yi)
            if new_square == None:
                break
            # print('Square {},{}'.format(xi, yi))
            
                # if new_square != '' and new_square.color != block_color:
                #     moves.append((xi, yi))
                break
            # print("   ", new_square, block_color)
            if new_square == '':
                if pawn_take == True:
                    if attacks_only == True:
                        moves.append((xi, yi))
                        # print('pawn attack line')
                    break
                # print('empty sq move')
                moves.append((xi, yi))
            elif new_square.color == block_color:
                # print(new_square, pawn_take, attacks_only)
                if attacks_only == True:
                    moves.append((xi, yi))
                    # print('attack line protect')
                break
            else:
                if isinstance(board.get_square(x,y), pawn) and pawn_take == False:
                    # print('pawn')
                    break
                # print('take')
                moves.append((xi, yi))
                break

        return moves
    
class knight(piece):

    def __init__(self, color) -> None:
        super().__init__(color)

    def find_moves(self, board, x, y, attacks_only=False):
        moves = []

        move_directions = [(1,2),(2,1),(1,-2),(-2,1),(-1,2),(2,-1),(-1,-2),(-2,-1)]

        for move in move_directions:
            x_new, y_new = x+move[0], y+move[1]
            new_square = board.get_square(x_new, y_new)

            if (new_square != None) and ((new_square == '') or ((new_square.color != self.color) or attacks_only)):
                moves.append((x_new, y_new))
        
        return moves
    

class king(piece):

    def __init__(self, color) -> None:
        super().__init__(color)
        self.moved = False

    def find_moves(self, board, x, y, attacks_only = False):
        moves = []

        moves.extend(self.valid_horizontal_moves(board, x, y, lim = 1, attacks_only=attacks_only))
        moves.extend(self.valid_vertical_moves(board, x, y, lim = 1, attacks_only=attacks_only))
        moves.extend(self.valid_diagonal_moves(board, x, y, lim = 1, attacks_only=attacks_only))

        if attacks_only == False:

            if self.color == 'w': 
                attack_color = 'b'
            else: 
                attack_color = 'w'
            squares_in_check = board.get_attacks(attack_color)
            # print('check squares: ', squares_in_check)
            
            # check for castling
            if self.moved == False:
                    
                corner_piece1 = board.get_square(1,y)
                corner_piece8 = board.get_square(8,y)

                if ((isinstance(corner_piece1, rook)) and 
                    (corner_piece1.moved == False) and 
                    (board.get_square(6,y) == '') and 
                    (board.get_square(7,y) == '') and
                    ((6,y) not in squares_in_check) and
                    ((7,y) not in squares_in_check)):
                        moves.append((7,y))

                if ((isinstance(corner_piece8, rook)) and 
                    (corner_piece8.moved == False) and 
                    (board.get_square(3,y) == '') and 
                    (board.get_square(4,y) == '') and
                    (board.get_square(2,y) == '') and
                    ((3,y) not in squares_in_check) and
                    ((4,y) not in squares_in_check)):
                        moves.append((3,y))

            moves = [i for i in moves if i not in squares_in_check]

        # print(moves)


        #### Castling rules ####
        # Neither the king nor the rook has previously moved.
        # There are no pieces between the king and the rook.
        # The king is not currently in check.
        # The king does not pass through or finish on a square that is attacked by an enemy piece.

        return moves
        
class queen(piece):

    def __init__(self, color) -> None:
        super().__init__(color)

    def find_moves(self, board, x, y, attacks_only=False):
        moves = []

        moves.extend(self.valid_horizontal_moves(board, x, y, attacks_only=attacks_only))
        moves.extend(self.valid_vertical_moves(board, x, y, attacks_only=attacks_only))
        moves.extend(self.valid_diagonal_moves(board, x, y, attacks_only=attacks_only))

        return moves
        
class pawn(piece):

    def __init__(self, color) -> None:
        super().__init__(color)

    def find_moves(self, board, x, y, attacks_only = False):
        moves = []

        if self.color == 'w':
            direction = -1
            start = 7
        else:
            direction = 1
            start = 2
        if y == start:
            forward_lim = 2
        else:
            forward_lim = 1
        
        def forward_right_func(x, y, i):
            return x + i, (y + i*direction)
        def forward_left_func(x, y, i):
            return x - i, (y + i*direction)
        
        moves.extend(self.valid_moves_helper(board, x, y, forward_right_func, 1, pawn_take = True, attacks_only=attacks_only))
        moves.extend(self.valid_moves_helper(board, x, y, forward_left_func, 1, pawn_take = True, attacks_only=attacks_only))

        # for checking where the pawn protects
        if attacks_only == False:

            def forward(x, y, i):
                return x, (y + i*direction)

            moves.extend(self.valid_moves_helper(board, x, y, forward, forward_lim))

        # en pessant 
        last_x1, last_y1, last_x2, last_y2 = game.last_move
        if isinstance(board.get_square(last_x2,last_y2), pawn) and abs(last_y2-last_y1) == 2 and last_y2 == y:
            moves.extend([(last_x1, int((last_y1 + last_y2)/2))])
        return moves
        
class rook(piece):

    def __init__(self, color) -> None:
        super().__init__(color)
        self.moved = False

    def find_moves(self, board, x, y, attacks_only=False):
        moves = []

        moves.extend(self.valid_horizontal_moves(board, x, y, attacks_only=attacks_only))
        moves.extend(self.valid_vertical_moves(board, x, y, attacks_only=attacks_only))

        return moves
        
class bishop(piece):

    def __init__(self, color) -> None:
        super().__init__(color)

    def find_moves(self, board, x, y, attacks_only=False):
        moves = []

        moves.extend(self.valid_diagonal_moves(board, x, y, attacks_only=attacks_only))

        return moves