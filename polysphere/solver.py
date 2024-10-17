from . import transformations

class PuzzleSolver:
    def __init__(self, board, pieces):
        self.board = board  # 5x11 grid
        self.pieces = pieces  # List of polyomino pieces
        self.solutions = []
        self.found_first_solution = False


    def can_place(self, piece, x, y):
        """Check if the polyomino can be placed at the position (x, y)."""
        for dx, dy in piece:
            if not self.is_valid_position(x + dx, y + dy):
                return False
        return True

    def is_valid_position(self, x, y):
        """Check if the position is valid and empty on the board."""
        return 0 <= x < len(self.board) and 0 <= y < len(self.board[0]) and self.board[x][y] == 0


    def place_piece(self, piece, x, y, name):
        """Place a polyomino on the board."""
        for dx, dy in piece:
            self.board[x + dx][y + dy] = name # Mark the position as filled

    def remove_piece(self, piece, x, y):
        """Remove a polyomino from the board."""
        for dx, dy in piece:
            self.board[x + dx][y + dy] = 0  # Unmark the position

    def is_small_empty_region(self):
        """Check if there is any contiguous empty space smaller than the minimum polyomino size."""
        rows = len(self.board)
        cols = len(self.board[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        min_piece_size = 3

        def flood_fill(x, y):
            """Flood fill to find the size of a contiguous region of 0s."""
            stack = [(x, y)]
            region_size = 0

            while stack:
                cx, cy = stack.pop()
                if visited[cx][cy] or self.board[cx][cy] != 0:
                    continue

                visited[cx][cy] = True
                region_size += 1

                # Add neighboring cells to the stack
                for nx, ny in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]:
                    if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and self.board[nx][ny] == 0:
                        stack.append((nx, ny))

            return region_size

        # Iterate over the board to find contiguous regions of 0s
        for i in range(rows):
            for j in range(cols):
                if self.board[i][j] == 0 and not visited[i][j]:
                    region_size = flood_fill(i, j)
                    if region_size < min_piece_size:
                        return True  # Early termination if we find a small region

        return False

    def get_empty_regions(self):
        """Returns a list of all contiguous empty regions on the board."""
        rows = len(self.board)
        cols = len(self.board[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        empty_regions = []

        def flood_fill(x, y):
            stack = [(x, y)]
            region = []

            while stack:
                cx, cy = stack.pop()
                if visited[cx][cy] or self.board[cx][cy] != 0:
                    continue

                visited[cx][cy] = True
                region.append((cx, cy))

                for nx, ny in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]:
                    if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and self.board[nx][ny] == 0:
                        stack.append((nx, ny))

            return region

        for i in range(rows):
            for j in range(cols):
                if self.board[i][j] == 0 and not visited[i][j]:
                    region = flood_fill(i, j)
                    empty_regions.append(region)

        return empty_regions

    def get_smallest_empty_region(self):
        """Returns the smallest contiguous empty region."""
        empty_regions = self.get_empty_regions()
        if not empty_regions:
            return None
        return min(empty_regions, key=len)

    def solve(self, piece_index=0, find_first=False):
        """Recursive solver that tries to place each polyomino in all transformations."""
        if piece_index == len(self.pieces):
            print("solution found!")
            self.solutions.append([row[:] for row in self.board])

            # If we're just finding the first solution, return immediately
            if find_first:
                self.found_first_solution = True
            return

        # Before trying to place the next piece, check for small empty regions
        if self.is_small_empty_region():
            print("empty region too small, backtracking!")
            return  # Backtrack if a small empty region is found

        # Get all transformations for the current piece
        piece_transformations = transformations.generate_transformations(self.pieces[piece_index]["shape"])
        smallest_region = self.get_smallest_empty_region()

        if smallest_region:
            for x, y in smallest_region:
                for transformation in piece_transformations:
                    if self.can_place(transformation, x, y):
                        self.place_piece(transformation, x, y, self.pieces[piece_index]["name"])
                        print("board :")
                        print(self.board)
                        self.solve(piece_index + 1, find_first)
                        if self.found_first_solution:
                            return
                        self.remove_piece(transformation, x, y)

    def get_solutions(self):
        """Start solving the puzzle and return all solutions."""
        self.solve()
        return self.solutions

    def get_first_solution(self):
        """Find the first solution."""
        self.solve(find_first=True)
        return self.solutions[0] if self.solutions else None