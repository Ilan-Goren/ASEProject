class pyramid_board:
    """
    Represents a 3D pyramid-shaped board.
    """
    def __init__(self, layers):
        """
        Initializes the pyramid board with the specified number of layers.

        Args:
            layers (int): The number of layers in the pyramid board.
        """
        self.layers = layers
        board_spaces = [(x + z, y + z, z) for z in range(layers) for x in range(0, ((2*layers)-1) - (2 * z), 2) for y in range(0, ((2*layers)-1) - (2 * z), 2)]
        self.cells = {space: 0 for space in board_spaces}

    def count_cells(self):
        """
        Counts the total number of cells in the pyramid board.

        Returns:
            int: The total number of cells.
        """
        return len(self.cells.keys())

    def convert_to_3D_array(self):
        """
        Converts the pyramid board to a 3D nested list representation.

        Returns:
            list[list[list[int]]]: A 3D array representing the board state.
        """
        #create an empty 3D array of the right shape
        board_array = [
            [[0 for x in range(z + 1)] for y in range(z + 1)]
            for z in range(self.layers - 1, -1, -1)
        ]
        #populate the array with values from the board cells
        for key in self.cells.keys():
            x,y,z = self.convert_board_coords_to_array_coords(key)
            board_array[int(z)][int(y)][int(x)] = self.cells[key]
        return board_array

    def convert_from_3D_array(self,board_array):
        """
        Converts a 3D nested list representation into the pyramid board dictionary format used for the solver.

        Args:
            board_array (list[list[list[int]]]): A 3D array representing the board state.
        """
        #reset cells and layer count
        self.cells = {}
        self.layers = len(board_array)
        #populate cells with values from 3D array
        for z in range(self.layers):
            for y in range(self.layers - z):
                for x in range(self.layers - z):
                    self.cells[self.convert_array_coords_to_board_coords((x,y,z))] = board_array[z][y][x]

    def convert_board_coords_to_array_coords(self, board_coords):
        """
        Converts board representation coordinates to 3D array coordinates.

        Args:
            board_coords (tuple[int, int, int]): A tuple representing the board coordinates (x, y, z).

        Returns:
            tuple[float, float, int]: A tuple representing the 3D array coordinates (x, y, z).
        """
        x,y,z = board_coords
        return ((x - z) / 2),((y - z) / 2),z

    def convert_array_coords_to_board_coords(self, array_coords):
        """
        Converts 3D array coordinates to board representation coordinates.

        Args:
            array_coords (tuple[float, float, int]): A tuple representing the array coordinates (x, y, z).

        Returns:
            tuple[int, int, int]: A tuple representing the board coordinates (x, y, z).
        """
        x,y,z = array_coords
        return ((x * 2) + z), ((y * 2) + z), z

    def is_region_free(self, region):
        """
        Checks if a given region of cells is free on the board.

        Args:
            region (list[tuple[int, int, int]]): A list of tuples representing cell coordinates (x, y, z).

        Returns:
            bool: True if the region is free, False otherwise.
        """
        for cell in region:
            # check if cell is a valid space on the board
            if cell not in self.cells:
                return False
            # check if cell is empty
            if self.cells[cell] != 0:
                return False
        return True

    def get_matching_empty_regions(self, region):
        """
        Finds all regions on the board that match the given region and are free.

        Args:
            region (list[tuple[int, int, int]]): A list of tuples representing cell coordinates (x, y, z).

        Returns:
            list[list[tuple[int, int, int]]]: A list of matching empty regions.
        """
        matching_empty_regions = []
        for z in range(self.layers):
            layer_size = (self.layers - z) * 2  # Side length of the square grid at layer z
            for x in range(layer_size):
                for y in range(layer_size):
                    translated_region = []
                    for i,j,k in region:
                        translated_region.append((x+i,y+j,z+k))
                    if self.is_region_free(translated_region):
                        matching_empty_regions.append(translated_region)
        return matching_empty_regions


