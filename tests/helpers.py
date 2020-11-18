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

def getSingleTurnData():
    data = {
        'player_1': {
            'characters': [
                {
                    'id': 0,
                    'health': {
                        'current': 30,
                        'max': 30
                    },
                    'action': 'move',
                    'position': {
                        'x': 1,
                        'y': 0
                    }
                },
                {
                    'id': 1,
                    'health': {
                        'current': 20,
                        'max': 20
                    },
                    'action': 'move',
                    'position': {
                        'x': 1,
                        'y': 3
                    }
                },
                {
                    'id': 2,
                    'health': {
                        'current': 40,
                        'max': 40
                    },
                    'action': 'move',
                    'position': {
                        'x': 1,
                        'y': 6
                    }
                }
            ]
        },
        'player_2': {
            'characters': [
                {
                    'id': 3,
                    'health': {
                        'current': 50,
                        'max': 50
                    },
                    'action': 'move',
                    'position': {
                        'x': 14,
                        'y': 0
                    }
                },
                {
                    'id': 4,
                    'health': {
                        'current': 30,
                        'max': 30
                    },
                    'action': 'move',
                    'position': {
                        'x': 14,
                        'y': 3
                    }
                },
                {
                    'id': 5,
                    'health': {
                        'current': 20,
                        'max': 20
                    },
                    'action': 'move',
                    'position': {
                        'x': 14,
                        'y': 6
                    }
                }
            ]
        }
    }

    return json.dumps(data)

def getSimulationTurnData(index):
    data = {
        'turns': [
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 1, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 1, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 1, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 14, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 14, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 14, 'y': 6}}
            ]}},
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 2, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 2, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 2, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 13, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 13, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 13, 'y': 6}}
            ]}},
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 3, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 3, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 3, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 12, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 12, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 12, 'y': 6}}
            ]}},
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 4, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 4, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 4, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 11, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 11, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 11, 'y': 6}}
            ]}},
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 5, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 5, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 5, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 10, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 10, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 10, 'y': 6}}
            ]}},
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 4, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 4, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 4, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 11, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 11, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 11, 'y': 6}}
            ]}},
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 3, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 3, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 3, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 12, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 12, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 12, 'y': 6}}
            ]}},
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 2, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 2, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 2, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 13, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 13, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 13, 'y': 6}}
            ]}},
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 1, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 1, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 1, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 14, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 14, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 14, 'y': 6}}
            ]}},
            {'player_1': {'characters': [
                {'id': 0, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 0, 'y': 0}},
                {'id': 1, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 0, 'y': 3}},
                {'id': 2, 'health': {'current': 40, 'max': 40}, 'action': 'move', 'position': {'x': 0, 'y': 6}}
            ]},
            'player_2': {'characters': [
                {'id': 3, 'health': {'current': 50, 'max': 50}, 'action': 'move', 'position': {'x': 15, 'y': 0}},
                {'id': 4, 'health': {'current': 30, 'max': 30}, 'action': 'move', 'position': {'x': 15, 'y': 3}},
                {'id': 5, 'health': {'current': 20, 'max': 20}, 'action': 'move', 'position': {'x': 15, 'y': 6}}
            ]}},
        ]
    }

    return json.dumps(data['turns'][index])

def getProjectedMatrix():
    return [
        ['t','0','t','t','t','t','t','t','t','t','t','t','t','t','3','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t','t'],
        ['t','1','t','t','t','t','t','t','t','t','t','t','t','t','4','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t','t'],
        ['t','2','t','t','t','t','t','t','t','t','t','t','t','t','5','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t','t']
    ]

def getSimplifiedPlayer1Data():
    return [
        [(1,0),(1,3),(1,6)],
        [(2,0),(2,3),(2,6)],
        [(3,0),(3,3),(3,6)],
        [(4,0),(4,3),(4,6)],
        [(5,0),(5,3),(5,6)],
        [(4,0),(4,3),(4,6)],
        [(3,0),(3,3),(3,6)],
        [(2,0),(2,3),(2,6)],
        [(1,0),(1,3),(1,6)],
        [(0,0),(0,3),(0,6)],
    ]

def getSimplifiedPlayer2Data():
    return [
        [(14,0),(14,3),(14,6)],
        [(13,0),(13,3),(13,6)],
        [(12,0),(12,3),(12,6)],
        [(11,0),(11,3),(11,6)],
        [(10,0),(10,3),(10,6)],
        [(11,0),(11,3),(11,6)],
        [(12,0),(12,3),(12,6)],
        [(13,0),(13,3),(13,6)],
        [(14,0),(14,3),(14,6)],
        [(15,0),(15,3),(15,6)],
    ]
