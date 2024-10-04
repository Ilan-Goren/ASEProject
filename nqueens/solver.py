def solve_nqueens(N):
    board = [[0 for _ in range(N)] for _ in range(N)]

    def isSafe(board, col, row):
        for i in range(row):
            if board[i][col] == 1:
                return False
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, N)):
            if board[i][j] == 1:
                return False
        return True

    def solve(board, row=0):
        if row >= N:
            return True
        for col in range(N):
            if isSafe(board, col, row):
                board[row][col] = 1
                if solve(board, row + 1):
                    return True
                board[row][col] = 0
        return False

    if solve(board, 0):
        return board
    else:
        return None