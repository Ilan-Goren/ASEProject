from . import matrix_polyominoes, matrix_transformations, matrix_solver

class Polysphere:
    def __init__(self):
        self.pieces = {
            'A': [[1, 1, 1],
                [1, 0, 1]],

            'B': [[0, 0, 1, 1],
                [1, 1, 1, 0]],

            'C': [[0, 1, 0],
                [1, 1, 0],
                [0, 1, 1]],

            'D': [[0, 1, 0],
                [1, 1, 1]],

            'E': [[0, 1, 0, 0],
                [1, 1, 1, 1]],

            'F': [[0, 1, 1],
                [1, 1, 1]],

            'G': [[0, 1, 1],
                [1, 1, 0]],

            'H': [[1, 1],
                [1, 0],
                [1, 0]],

            'I': [[1, 1, 1],
                [0, 0, 1],
                [0, 0, 1]],

            'J': [[1, 0, 0, 0],
                [1, 1, 1, 1]],

            'K': [[1, 0],
                [1, 1]],

            'L': [[1, 1, 0],
                [0, 1, 1],
                [0, 0, 1]],
        }
        self.pieces_left = self.pieces.copy()
        self.board_size = (5, 11)
        self.board = [[0 for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
        self.piece_positions = {}
        self.allSolutions = []

    def place_piece(self, piece_key, positions):
        """Place the piece on the board at the specified list of positions."""
        piece = self.pieces[piece_key]

        if not self.is_valid_placement(piece, positions):
            print(f"Invalid placement for {piece_key} at {positions}")
            return False

        # Check for already placed positions
        if piece_key in list(self.piece_positions.keys()):
            print(f"{piece_key} already placed at {positions}")
            return False
        
        self.piece_positions[piece_key] = []

        # Place the piece on the board and update piece_positions
        for pos in positions:
            row, col = pos
            self.board[row][col] = piece_key  # Mark the position on the board

            # Add the position to piece_positions for tracking
            self.piece_positions[piece_key].append(pos)

        print(f'Board after placing key {self.board}')

        self.pieces_left.pop(piece_key)
        print(f"Placed {piece_key} at {self.piece_positions[piece_key]}")
        return True

    def remove_piece(self, piece_key):
        """Remove the piece from the board."""
        if piece_key not in list(self.piece_positions.keys()):
            print(f"Piece {piece_key} not in piece posistions")
            return  False# No such piece on the board

        # Get the positions occupied by the piece
        occupied_positions = self.piece_positions[piece_key]

        # Clear the positions on the board
        for pos in occupied_positions:
            row, col = pos
            self.board[row][col] = 0  # Mark as empty

        # Remove the piece from piece_positions
        print(f"Removed {piece_key} at {self.piece_positions[piece_key]}")
        del self.piece_positions[piece_key]

        self.pieces_left[piece_key] = self.pieces[piece_key]
        return True
    def is_board_filled(self):
        """Check if no pieces are left and returns True else False"""
        if not self.pieces_left:
            return True
        return False
    
    def is_board_empty(self):
        """Check if no pieces are placed on board"""
        for row in self.board:
            for col in row:
                if col:
                    return False
        return True
    
    def is_valid_placement(self, piece, positions):
        """Check if the piece can be placed on the board at the given positions."""
        for pos in positions:
            row, col = pos
            # Check if the current position is out of bounds
            if row < 0 or row >= self.board_size[0] or col < 0 or col >= self.board_size[1]:
                return False
            
            # Check if the cell is already filled
            if self.board[row][col] == 1:
                return False
                
        # If all positions are valid, return True
        return True

    
    def rotate_piece(self, piece_key):
        """Rotate the specified piece 90 degrees."""
        if piece_key not in self.pieces_left.keys() or piece_key in self.piece_positions.keys():
            print(f"Rotation {piece_key} Error")
            return False
        
        # Get the current piece matrix
        piece = self.pieces_left[piece_key]

        # Rotate the piece 90 degrees clockwise and store in pieces
        self.pieces_left[piece_key] = [list(reversed(col)) for col in zip(*piece)]
        print(f"Success: Rotation {piece_key} complete")

        return True
    
    def flip_piece(self, piece_key):
        """Rotate the specified piece horizontally."""
        if piece_key not in self.pieces_left.keys() or piece_key in self.piece_positions.keys():
            print(f"Flip {piece_key} Error")
            return False
        
        # Get the current piece matrix
        piece = self.pieces_left[piece_key]

        # Flip the piece vertically by reversing the order of the rows
        self.pieces_left[piece_key] = piece[::-1]
        print(f"Success: Flip {piece_key} complete")

        return True
    
    def reset_board(self):
        ''' Reset the all class variables'''
        self.board = [[0 for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
        self.pieces_left = self.pieces.copy()
        self.piece_positions = {}
        self.allSolutions = []
        return
    
    def solvePartialConfig(self):
        ''' Solve function for partial configurations '''
        alreadyPlaced = internalConversionFromLetterToID(self.board)

        alreadyPlacedIDs = {id - 1 for row in alreadyPlaced for id in row if id}
        polys = []
        for i in range(12):
            if i in alreadyPlacedIDs:
                continue
            polys.append(matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[i]["tiles"], i + 1))
        id_conversions = []
        solver = matrix_solver.MatrixSolver()
        solution = solver.solve_packing(polys,11, 5, alreadyPlaced, id_conversions)
        if not solution:
            return False
        solution = solver.revert_ids(id_conversions, solution)
        solution = internalConversionFromIDToLetter(solution)
        print(f"Solved after conversion to Letters: {solution}")
        self.board = solution

        piece_pos = getPiecesPositionsFromBoard(self.board)
        self.piece_positions = piece_pos.copy()
        self.pieces_left = {}
        return True
    
    def solveAllPartialConfig(self):
        alreadyPlaced = internalConversionFromLetterToID(self.board)
        alreadyPlacedIDs = {id - 1 for row in alreadyPlaced for id in row if id}
        polys = []
        for i in range(12):
            if i in alreadyPlacedIDs:
                continue
            polys.append(matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[i]["tiles"], i + 1))

        s = matrix_solver.MatrixSolver()
        id_conversions = []

        for rows in s.generate_packing_solutions(polys, 11, 5, alreadyPlaced, id_conversions):
            # Have to now print packing separately from the solver solving function now it's a generator
            sol = s.print_packing(rows, 11, 5)

            sol_reverted = s.revert_ids(id_conversions, sol)
            if sol_reverted != None:
                sol_reverted = internalConversionFromIDToLetter(sol_reverted)
                self.allSolutions.append(sol_reverted)

        if not self.allSolutions:
            return False
        return True
    
    def solveEmptyBoard(self):
        polys = []
        for p in matrix_polyominoes.POLYOMINOES:
            poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
            polys.append(poly)
        s = matrix_solver.MatrixSolver()
        solution = s.solve_packing(polys,11,5)
        solution = internalConversionFromIDToLetter(solution)
        self.board = solution
        piece_pos = getPiecesPositionsFromBoard(self.board)
        self.piece_positions = piece_pos.copy()
        self.pieces_left = {}
        return True
    


##########################################################################################
#                                  HELPER FUNCTIONS                                      #
##########################################################################################
    
def internalConversionFromLetterToID(board):
    ''' Function changes placed pieces from letters to ID '''
    rep = { 'A' : 1, 'B': 2, 'C' : 3, 'D' : 4, 'E' : 5, 'F' : 6, 
            'G': 7, 'H': 8, 'I': 9, 'J' : 10, 'K' : 11, 'L' : 12}
    new_board = [[0 for _ in range(11)] for _ in range(5)] # New Board to return

    for row_index, row in enumerate(board):
        for cell_index, cell in enumerate(row):
            if cell in rep:
                new_board[row_index][cell_index] = rep[cell]
    return new_board

def internalConversionFromIDToLetter(board):
    ''' Function changes placed pieces from ID to letters '''
    rep = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 
           7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L'}
    new_board = [[0 for _ in range(11)] for _ in range(5)] # New Board to return

    for row_index, row in enumerate(board):
        for cell_index, cell in enumerate(row):
            if cell in rep:
                new_board[row_index][cell_index] = rep[cell]
    return new_board


def getPiecesPositionsFromBoard(board):
    piecesPos = {}
    for row_index, row_data in enumerate(board):
        for col_index, col_data in enumerate(row_data):
            if col_data not in piecesPos.keys():
                piecesPos[col_data] = [(row_index, col_index)]
            else:
                piecesPos[col_data].append((row_index, col_index))

    return piecesPos


def get_all_solutions(solutions):
    polys = []
    for p in matrix_polyominoes.POLYOMINOES:
        poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
        polys.append(poly)

    s = matrix_solver.MatrixSolver()
    id_conversions = []
    solution_count = 0

    for rows in s.generate_packing_solutions(polys, 11, 5, None, id_conversions):
        # Have to now print packing separately from the solver solving function now it's a generator
            sol = s.print_packing(rows, 11, 5)

            sol_reverted = s.revert_ids(id_conversions, sol)

            if sol_reverted != None:
                solution_count += 1
                sol_reverted = internalConversionFromIDToLetter(sol_reverted)
                solutions.append(sol_reverted)
                
                # print("list representation of solution " + str(solution_count) + ":")
                # print(sol_reverted)
            

