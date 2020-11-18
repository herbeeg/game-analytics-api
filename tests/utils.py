import json

def register(client, email, username, password, activation_key):
    return client.post(
        '/register',
        data=json.dumps({
            'email': email,
            'username': username,
            'password': password,
            'activation_key': activation_key
        }),
        content_type='application/json'
    )

def login(client, email, password):
    return client.post(
        '/login',
        data=json.dumps({'email': email, 'password': password}),
        content_type='application/json'
    )

def logout(client):
    return client.get(
        '/logout',
        follow_redirects=False
    )

def profile(client, user_id, access_token):
    return client.get(
        f'/profile/{user_id}',
        headers={
            'Authorization': 'Bearer ' + access_token
        },
        follow_redirects=False
    )

def newMatch(client, data, access_token):
    return client.post(
        '/match/new',
        data=data,
        headers={
            'Authorization': 'Bearer ' + access_token
        },
        content_type='application/json'
    )

def startMatch(client, uuid, access_token):
    return client.get(
        f'/match/start/{uuid}',
        headers={
            'Authorization': 'Bearer ' + access_token
        },
        follow_redirects=False
    )

def endMatch(client, uuid, access_token):
    return client.get(
        f'/match/end/{uuid}',
        headers={
            'Authorization': 'Bearer ' + access_token
        },
        follow_redirects=False
    )

def nextTurn(client, uuid, data, access_token):
    return client.post(
        f'/turn/update/{uuid}',
        data=data,
        headers={
            'Authorization': 'Bearer ' + access_token
        },
        content_type='application/json'
    )

def viewTurn(client, uuid, turn_number, access_token):
    return client.get(
        f'/turn/view/{uuid}/{turn_number}',
        headers={
            'Authorization': 'Bearer ' + access_token
        },
        follow_redirects=False
    )

def viewHistory(client, user_id, access_token):
    return client.get(
        f'/profile/{user_id}/history',
        headers={
            'Authorization': 'Bearer ' + access_token
        },
        follow_redirects=False
    )
