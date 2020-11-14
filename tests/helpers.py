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
        'turns': [
            {
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
        ]
    }

    return json.dumps(data)

def getProjectedMatrix():
    return [
        ['t','0','t','t','t','t','t','t','t','t','t','t','t','3','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t'],
        ['t','1','t','t','t','t','t','t','t','t','t','t','t','4','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t'],
        ['t','2','t','t','t','t','t','t','t','t','t','t','t','5','t'],
        ['t','t','t','t','t','t','t','t','t','t','t','t','t','t','t']
    ]
