def solve_n_queens(n):
    #use a 2D array of size NxN to represent the board
    b = [[0 for _ in range(n)] for _ in range(n)]

    """
        Given a 2D array (board) representing a chess board and a set of coordinates,
        (col, row), checks if a the tile on those coordinates on the board is a 
        safe space to place a queens
    """
    def is_safe(board, col, row):
        """
            in the following steps we only check spaces to the
            left of the space we are checking (inclusively)
            as we always place pieces from left to right
        """
        #Check all spaces horizontally adjacent to the space for queens
        for i in range(row):
            if board[i][col] == 1:
                return False
        #Check all spaces vertically adjacent to the space for queens
        for i in range(col):
            if board[row][i] == 1:
                return False
        #Check all spaces on the upper left diagonal
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        #Check all spaces on the lowe left diagonal
        for i, j in zip(range(row, -1, -1), range(col, n)):
            if board[i][j] == 1:
                return False
        return True

    """
        Solves the N-queens problem given a board (and a row number*), 
        the function works by attempting to place a queen somewhere along
        the given row (*starting at 0) then recursively checks the next 
        row until it reaches the end of the board to find a solution
    """
    def solve(board, row=0):
        # if we have reached the end of the board then we have found a solution
        if row >= n:
            return True
        # else attempt to find a safe space for each column in the row
        for col in range(n):
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
    if solve(b, 0):
        return b
    # return None if there is no solution
    else:
        return None