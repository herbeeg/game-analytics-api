class MatrixGenerator:
    def __init__(self, positions, size_x=16, size_y=8):
        self.positions = positions
        self.x = size_x
        self.y = size_y

    def generate(self):
        matrix = [['' for j in range(self.x)] for i in range(self.y)]
        """Creating empty matrix structure using list comprehension."""

        for pos in self.positions:
            matrix[pos['y']][pos['x']] = pos['id']

        filled_matrix = [[str(k) if '' != k else 't' for k in i] for i in matrix]

        return filled_matrix
