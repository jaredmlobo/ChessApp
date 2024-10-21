def grid_to_board(x,y):
    """Convert numbered position to board position"""
    return get_column_letter(x)+str(y)


def board_to_grid(pos):
    """Convert numbered position to board position"""
    [x,y] = list(pos)
    return (get_column_number(x), int(y))

def get_column_letter(col_num):
    cols = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h'}
    return cols[col_num]

def get_column_number(col_num):
    cols = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
    return cols[col_num]