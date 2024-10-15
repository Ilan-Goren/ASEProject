def is_safe(board, col, row):
    """
        in the following steps we only check spaces to the
        left of the space we are checking (inclusively)
        as we always place pieces from left to right
    """
    N = len(board[0])
    #Check all spaces horizontally adjacent to the space for queens
    for i in range(row):
        if board[i][col] == 1:
            return False
    #Check all spaces vertically adjacent to the space for queens, **is this needed?
    for i in range(col):
        if board[row][i] == 1:
            return False
    #Check all spaces on the upper left diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    #Check all spaces on the lowe left diagonal
    for i, j in zip(range(row, -1, -1), range(col, N)):
        if board[i][j] == 1:
            return False
    return True

def create_empty_board(n):
    return [[0 for i in range(n)] for i in range(n)]

def check_solution(board):
    N = len(board)
    for col in range(N):
        count = sum(board[row][col] for row in range(N))
        if count != 1:
            return False

    return True 


def solve_n_queens(N):
    #use a 2D array of size NxN to represent the board
    board = [[0 for _ in range(N)] for _ in range(N)]

    """
        Solves the N-queens problem given a board (and a row number*), 
        the function works by attempting to place a queen somewhere along
        the given row (*starting at 0) then recursively checks the next 
        row until it reaches the end of the board to find a solution
    """
    def solve(board, row=0):
        # if we have reached the end of the board then we have found a solution
        if row >= N:
            return True
        # else attempt to find a safe space for each column in the row
        for col in range(N):
            if is_safe(board, col, row):
                # update the col,row on the board with a 1 to represent a placed queen
                board[row][col] = 1
                # continue attempting to solve with this placed queen
                if solve(board, row + 1):
                    return True
                # backtrack if solution not found
                board[row][col] = 0
        # if we haven't returned true by now then there is no solution
        return False

    # use the helper functions to solve for the given board
    if solve(board, 0):
        return board
    # return None if there is no solution
    else:
        return None