class MatrixGenerator:
    """
    Populate a 2-dimensional list with values
    attributed to what that tile would
    represent in the battlefield
    state.
    """
    def __init__(self, positions, size_x=16, size_y=8):
        self.positions = positions
        self.x = size_x
        self.y = size_y

    def generate(self):
        """
        Character (x,y) positions are placed in 
        the battlefield state matrix as a 
        representation for the API user 
        to display on the frontend.

        Returns:
            list: 2-dimensional list of battlefield tile states
        """
        matrix = [['' for j in range(self.x)] for i in range(self.y)]
        """Creating empty matrix structure using list comprehension."""

        for pos in self.positions:
            matrix[pos['y']][pos['x']] = pos['id']
            """We use the character ID to represent itself on the battlefield."""

        filled_matrix = [[str(k) if '' != k else 't' for k in i] for i in matrix]
        """Fill the remaining empty list items with a terrain identifier."""

        return filled_matrix
