from . import bitmap_transformations

def generate_transformations_memo(polyominoes):
    transformations_memo = {}
    for p in polyominoes:
        piece_bitmap = bitmap_transformations.list_to_bitmap(p['shape'], p['width'])
        transformations = bitmap_transformations.generate_transformations(piece_bitmap, p['width'], p['height'])
        transformations_memo[p['id']] = transformations
    return transformations_memo


def can_place(bitmap_board, piece_bitmap, width, height, row, col, board_width, board_height):
    """
    Check if a piece can be placed on the bitmap board at a given row and column.
    """
    if row + height > board_height or col + width > board_width:
        return False

    for i in range(height):
        for j in range(width):
            bit_position = (height - i - 1) * width + (width - j - 1)
            if (piece_bitmap >> bit_position) & 1:
                board_bit_position = (row + i) * board_width + (col + j)
                if bitmap_board & (1 << board_bit_position):  # Check if the cell is occupied
                    return False
    return True

def can_place_optimized(board_bitmap, piece_bitmap, width, height, row, col, board_width, board_height):
    """
     Optimized check if a piece can be placed on the board_bitmap at a given row and column.
     Handles boundary checks and ensures the piece does not overlap with already placed pieces.
     """

    # Ensure the piece fits within board boundaries before trying to place
    if row < 0 or col < 0 or row + height > board_height or col + width > board_width:
        return False

    for i in range(height):
        # Calculate the start bit for the current row in the board
        board_row_start_bit = (row + i) * board_width + col

        if board_row_start_bit < 0 or (board_row_start_bit + width) > board_width * board_height:
            # Skip this placement if the bit range is out of bounds
            return False

        # Extract the board row as a bit mask, aligned with the current piece row
        board_row_bitmap = (board_bitmap >> board_row_start_bit) & ((1 << width) - 1)

        # Extract the corresponding piece row as a bit mask
        piece_row_bitmap = (piece_bitmap >> (i * width)) & ((1 << width) - 1)

        # Check for overlap: if any of the bits are 1 in both board and piece row, it's an invalid placement
        if (board_row_bitmap & piece_row_bitmap) != 0:
            return False

    return True

def can_place_with_offset(board_bitmap, piece_bitmap, width, height, row, col, board_width, board_height):
    """
    Check if a piece can be placed at the given (row, col) position on the board_bitmap,
    including any possible offsets of the piece within its height and width.
    """
    # Ensure the piece fits within the board boundaries with offset consideration
    # Ensure the piece fits within the board boundaries with positive and negative offset consideration
    for row_offset in range(-height + 1, height):  # Negative and positive offsets in the row
        for col_offset in range(-width + 1, width):  # Negative and positive offsets in the column
            if can_place_optimized(board_bitmap, piece_bitmap, width, height,
                                   row + row_offset, col + col_offset,
                                   board_width, board_height):
                return [row_offset, col_offset]
    return False

def place_piece(board, piece_bitmap, width, height, row, col, piece_id, bitmap_board):
    """
    Place the piece on the board at the given row and column, using the piece's bitmap.
    Also update the bitmap representation.
    """
    for i in range(height):
        for j in range(width):
            bit_position = (height - i - 1) * width + (width - j - 1)
            if (piece_bitmap >> bit_position) & 1:
                board[row + i][col + j] = piece_id  # Update list board
                # Update the bitmap board (set the bit)
                bitmap_board |= (1 << ((row + i) * len(board[0]) + (col + j)))
    return bitmap_board


def remove_piece(board, piece_bitmap, width, height, row, col, bitmap_board):
    """
    Remove the piece from the board at the given row and column.
    Also update the bitmap representation.
    """
    for i in range(height):
        for j in range(width):
            bit_position = (height - i - 1) * width + (width - j - 1)
            if (piece_bitmap >> bit_position) & 1:
                board[row + i][col + j] = 0  # Update list board
                # Update the bitmap board (clear the bit)
                bitmap_board &= ~(1 << ((row + i) * len(board[0]) + (col + j)))
    return bitmap_board

def list_to_bitmap_board(list_board, board_width, board_height):
    """
    Converts a list-based board representation to a bitmap representation.
    """
    bitmap_board = 0  # Initialize the bitmap to 0

    for row in range(board_height):
        for col in range(board_width):
            if list_board[row][col] != 0:  # Non-zero values represent placed pieces
                # Set the corresponding bit in the bitmap
                bit_position = (board_height - row - 1) * board_width + (board_width - col - 1)
                bitmap_board |= (1 << bit_position)

    return bitmap_board

def solve(list_board, bitmap_board, available_polyominoes, transformations_memo, board_width, board_height, placed_pieces, find_all, solutions):
    free_cells = [(r, c) for r in range(board_height) for c in range(board_width) if list_board[r][c] == 0]
    free_cells.sort(key=lambda x: (x[0], x[1]))  # Leftmost-uppermost cell first

    if not free_cells:
        solutions.append([row[:] for row in list_board])
        if not find_all:
            return True
        return False

    row, col = free_cells[0]

    for polyomino in available_polyominoes:
        for transformed_bitmap, transformed_width, transformed_height in transformations_memo[polyomino['id']]:
            if can_place(bitmap_board, transformed_bitmap, transformed_width, transformed_height, row, col, board_width, board_height):
                bitmap_board = place_piece(list_board, transformed_bitmap, transformed_width, transformed_height, row, col, polyomino['id'], bitmap_board)
                placed_pieces.append(polyomino['id'])
                remaining_polyominoes = [p for p in available_polyominoes if p['id'] != polyomino['id']]

                if solve(list_board, bitmap_board, remaining_polyominoes, transformations_memo, board_width, board_height, placed_pieces, find_all, solutions):
                    return True

                bitmap_board = remove_piece(list_board, transformed_bitmap, transformed_width, transformed_height, row, col, bitmap_board)
                placed_pieces.pop()

    return False

def solve_optimised(list_board, bitmap_board, available_polyominoes, transformations_memo, board_width, board_height, placed_pieces, find_all, solutions):
    free_cells = [(r, c) for r in range(board_height) for c in range(board_width) if list_board[r][c] == 0]
    free_cells.sort(key=lambda x: (x[0], x[1]))  # Leftmost-uppermost cell first

    if not free_cells:
        solutions.append([row[:] for row in list_board])
        if not find_all:
            return True
        return False

    row, col = free_cells[0]

    for polyomino in available_polyominoes:
        for transformed_bitmap, transformed_width, transformed_height in transformations_memo[polyomino['id']]:
            can_place_transformation = can_place_with_offset(bitmap_board, transformed_bitmap, transformed_width, transformed_height, row, col, board_width, board_height)
            if can_place_transformation:
                bitmap_board = place_piece(list_board, transformed_bitmap, transformed_width, transformed_height, row + can_place_transformation[0], col + can_place_transformation[1], polyomino['id'], bitmap_board)
                placed_pieces.append(polyomino['id'])
                remaining_polyominoes = [p for p in available_polyominoes if p['id'] != polyomino['id']]

                if solve(list_board, bitmap_board, remaining_polyominoes, transformations_memo, board_width, board_height, placed_pieces, find_all, solutions):
                    return True

                bitmap_board = remove_piece(list_board, transformed_bitmap, transformed_width, transformed_height, row + can_place_transformation[0], col + can_place_transformation[1], bitmap_board)
                placed_pieces.pop()

    return False


def find_first_solution(board, polyominoes, board_width, board_height):
    """
    Finds and returns the first possible solution for the polyomino puzzle.
    """
    solutions = []
    placed_pieces = []
    transformations_memo = generate_transformations_memo(polyominoes)
    solve_optimised(board, list_to_bitmap_board(board, board_width, board_height), polyominoes, transformations_memo, board_width, board_height, placed_pieces, find_all=False, solutions=solutions)

    if solutions:
        return solutions[0]  # Return the first solution found
    else:
        return None  # No solution found

def find_all_solutions(board, polyominoes, board_width, board_height):
    """
    Finds and returns all possible solutions for the polyomino puzzle.
    """
    solutions = []
    placed_pieces = []
    transformations_memo = generate_transformations_memo(polyominoes)
    solve(board, list_to_bitmap_board(board, board_width, board_height), polyominoes, transformations_memo, board_width, board_height, placed_pieces, find_all=True, solutions=solutions)
    return solutions