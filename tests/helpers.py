import json

def getMatchData():
    return json.dumps({
        'title': 'Match 1',
        'size': {
            'x': 16,
            'y': 8
        },
        'player_1': {
            'name': 'Player 1',
            'characters': [
                {
                    'id': 0,
                    'position': {
                        'x': 0,
                        'y': 0
                    }
                },
                {
                    'id': 1,
                    'position': {
                        'x': 0,
                        'y': 3
                    }
                },
                {
                    'id': 2,
                    'position': {
                        'x': 0,
                        'y': 6
                    }
                }
            ]
        },
        'player_2': {
            'name': 'Player 2',
            'characters': [
                {
                    'id': 3,
                    'position': {
                        'x': 15,
                        'y': 0
                    }
                },
                {
                    'id': 4,
                    'position': {
                        'x': 15,
                        'y': 3
                    }
                },
                {
                    'id': 5,
                    'position': {
                        'x': 15,
                        'y': 6
                    }
                }
            ]
        }
    })