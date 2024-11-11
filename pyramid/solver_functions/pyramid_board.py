
class pyramid_board:
    def __init__(self, layers):
        self.layers = layers
        board_spaces = [(x + z, y + z, z) for z in range(layers) for x in range(0, 9 - (2 * z), 2) for y in range(0, 9 - (2 * z), 2)]
        self.cells = {space: 1 for space in board_spaces}

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
                    print((x,y,z))
                    self.cells[self.convert_array_coords_to_board_coords((x,y,z))] = board_array[z][y][x]

    def convert_board_coords_to_array_coords(self, board_coords):
        x,y,z = board_coords
        return ((x - z) / 2),((y - z) / 2),z

    def convert_array_coords_to_board_coords(self, array_coords):
        x,y,z = array_coords
        return ((x * 2) + z), ((y * 2) + z), z