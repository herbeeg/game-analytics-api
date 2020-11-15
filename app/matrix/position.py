class TurnPositions:
    def __init__(self, meta):
        self.meta = meta

    def parse(self):
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
