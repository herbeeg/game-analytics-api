class TurnPositions:
    """
    Convert turn metadata stored in the database
    to a list of character positions that can 
    be turned into a positional matrix
    returned to the API requester.
    """
    def __init__(self, meta):
        """
        Store metadata.

        Args:
            meta (list): Metadata returned from the database
        """
        self.meta = meta

    def parse(self):
        """
        Extract positional data from the turn meta.

        Returns:
            list: List of positional key values
        """
        positions = []
        players = [
            'player_1',
            'player_2'
        ]

        for player in players:
            for character in self.meta[player]['characters']:
                try:
                    positions.append({
                        'id': character['id'],
                        'x': character['position']['x'],
                        'y': character['position']['y']
                    })
                except KeyError:
                    return 'Invalid metadata provided.'

        return positions
