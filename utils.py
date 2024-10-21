def grid_to_board(x,y):
    """Convert numbered position to board position"""
    return get_column_letter(x)+str(y)


def board_to_grid(pos):
    """Convert numbered position to board position"""
    [x,y] = list(pos)
    return (get_column_number(x), int(y))

def get_column_letter(col_num):
    cols = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H'}
    return cols[col_num]

def get_column_number(col_num):
    cols = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8}
    return cols[col_num]