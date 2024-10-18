from . import bitmap_transformations

def can_place(board, piece_bitmap, width, height, row, col, board_width, board_height):
    """
    Check if a piece can be placed on the board at a given row and column.
    Ensure the piece fits within the board and does not overlap with existing pieces.
    """
    # Ensure piece fits within board boundaries
    if row + height > board_height or col + width > board_width:
        return False

    for i in range(height):
        for j in range(width):
            # Check if the bit in piece_bitmap is 1 and if it overlaps with any non-zero cell on the board
            bit_position = (height - i - 1) * width + (width - j - 1)
            if (piece_bitmap >> bit_position) & 1:
                if board[row + i][col + j] != 0:  # Overlapping with another piece
                    return False

    return True


def place_piece(board, piece_bitmap, width, height, row, col, piece_id):
    """
    Place the piece on the board at the given row and column, using the piece's bitmap.
    """
    for i in range(height):
        for j in range(width):
            # Check if the bit in piece_bitmap is 1
            bit_position = (height - i - 1) * width + (width - j - 1)
            if (piece_bitmap >> bit_position) & 1:
                board[row + i][col + j] = piece_id  # Place the piece on the board
    print(board)


def remove_piece(board, piece_bitmap, width, height, row, col):
    """
    Remove the piece from the board at the given row and column.
    """
    for i in range(height):
        for j in range(width):
            # Check if the bit in piece_bitmap is 1
            bit_position = (height - i - 1) * width + (width - j - 1)
            if (piece_bitmap >> bit_position) & 1:
                board[row + i][col + j] = 0  # Remove the piece from the board


def solve(board, available_polyominoes, board_width, board_height, placed_pieces, find_all, solutions):
    """
    Generalized recursive function to solve the polyomino puzzle with proper tracking of placed pieces.
    """
    found_solution = True
    for row in range(board_height):
        for col in range(board_width):
            if board[row][col] == 0:  # Free cell found
                found_solution = False

                # Try to place each available polyomino in this free cell
                for polyomino in available_polyominoes:
                    # Generate all transformations (rotations and flips) of the polyomino
                    transformations = bitmap_transformations.generate_transformations(
                        bitmap_transformations.list_to_bitmap(polyomino["shape"], polyomino["width"]),
                        polyomino["width"],
                        polyomino["height"])

                    for transformed_bitmap, transformed_width, transformed_height in transformations:
                        # Convert the transformed shape into a bitmap
                        transformed_shape = bitmap_transformations.bitmap_to_list(transformed_bitmap, transformed_width, transformed_height)

                        # Check if we can place this transformation at (row, col)
                        if can_place(board, transformed_bitmap, transformed_width, transformed_height, row, col,
                                     board_width, board_height):
                            # Place the piece on the board
                            place_piece(board, transformed_bitmap, transformed_width, transformed_height, row, col,
                                        polyomino['id'])
                            placed_pieces.append(polyomino['id'])  # Track placed pieces

                            # Remove the polyomino from available pieces
                            remaining_polyominoes = [p for p in available_polyominoes if p['id'] != polyomino['id']]

                            # Recurse to place the next piece (depth-first search)
                            if solve(board, remaining_polyominoes, board_width, board_height, placed_pieces, find_all,
                                     solutions):
                                return True  # Return if the first solution was found

                            # Backtrack: Remove the piece and try the next option
                            remove_piece(board, transformed_bitmap, transformed_width, transformed_height, row, col)
                            placed_pieces.pop()  # Remove the polyomino from the placed pieces list

                return False  # No valid placement was found, backtrack

    # If no free cells are left, we've found a solution
    if found_solution:
        # Deep copy the current board state to avoid referencing issues
        solutions.append([row[:] for row in board])

        # If we only want the first solution, stop the recursion here
        if not find_all:
            return True  # Signal that we found the first solution and stop

    return False  # Continue searching if we want all solutions


def find_first_solution(board, polyominoes, board_width, board_height):
    """
    Finds and returns the first possible solution for the polyomino puzzle.
    """
    solutions = []
    placed_pieces = []
    solve(board, polyominoes, board_width, board_height, placed_pieces, find_all=False, solutions=solutions)

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
    solve(board, polyominoes, board_width, board_height, placed_pieces, find_all=True, solutions=solutions)
    return solutions