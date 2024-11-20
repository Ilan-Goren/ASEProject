class pyramid_board:
    def __init__(self, layers):
        self.layers = layers
        board_spaces = [(x + z, y + z, z) for z in range(layers) for x in range(0, ((2*layers)-1) - (2 * z), 2) for y in range(0, ((2*layers)-1) - (2 * z), 2)]
        self.cells = {space: 0 for space in board_spaces}

    def count_cells(self):
        return len(self.cells.keys())

    def convert_to_3D_array(self):
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
        #reset cells and layer count
        self.cells = {}
        self.layers = len(board_array)
        #populate cells with values from 3D array
        for z in range(self.layers):
            for y in range(self.layers - z):
                for x in range(self.layers - z):
                    self.cells[self.convert_array_coords_to_board_coords((x,y,z))] = board_array[z][y][x]

    def convert_board_coords_to_array_coords(self, board_coords):
        x,y,z = board_coords
        return ((x - z) / 2),((y - z) / 2),z

    def convert_array_coords_to_board_coords(self, array_coords):
        x,y,z = array_coords
        return ((x * 2) + z), ((y * 2) + z), z

    def is_region_free(self, region):
        for cell in region:
            # check if cell is a valid space on the board
            if cell not in self.cells:
                return False
            # check if cell is empty
            if self.cells[cell] != 0:
                return False
        return True

    def get_matching_empty_regions(self, region):
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


