from flask import Blueprint
from flask_jwt_extended import jwt_required

match = Blueprint('match', __name__)

@match.route('/match/new', methods=['POST'])
@jwt_required
def newMatch():
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    if 'POST' == request.method:
        if not username:
            error = 'Invalid username identity.'
        else:
            try:
                new_match = Match(
                    claims['id'],
                    0,
                    request.json['title']
                )
                db.session.add(new_match)
                db.session.commit()

                match_data = db.session.query(Match).filter_by(user_id=claims['id']).order_by(Match.created_at.desc()).one()

                try:
                    uuid = match_data.uuid

                    match_meta = MatchMeta(
                        uuid,
                        'player_1',
                        request.json['player_1']
                    )
                    db.session.add(match_meta)
                    db.session.commit()

                    match_meta = MatchMeta(
                        uuid,
                        'player_2',
                        request.json['player_2']
                    )
                    db.session.add(match_meta)
                    db.session.commit()

                    message = 'New match setup successfully.'
   
                    return jsonify({
                        'uuid': match_data.uuid,
                        'message': message
                    }), 200
                except AttributeError:
                    error = 'Malformed uuid column data.'

                    return jsonify({
                        'message': error
                    }), 400
                except KeyError:
                    error = 'Malformed match metadata provided.'

                    return jsonify({
                        'message': error
                    }), 400
            except KeyError:
                error = 'Malformed match data provided.'

                return jsonify({
                    'message': error
                }), 400

        return jsonify({
            'message': error
        }), 400

@match.route('/match/start/<uuid>', methods=['GET'])
@jwt_required
def startMatch(uuid):
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    match = db.session.query(Match).filter_by(uuid=uuid).first()

    if not match:
        return 404
    elif match.user_id != claims['id']:
        error = 'Cannot start matches owned by other users.'

        return jsonify({
            'message': error
        }), 401
    else:
        try:
            match.live = 1
            db.session.commit()

            uri = f'/match/view/{match.uuid}'
            message = 'Match started successfully.'

            return jsonify({
                'match_uri': uri,
                'message': message
            }), 200
        except AttributeError:
            error = 'Match could not be started.'

            return jsonify({
                'message': error
            }), 400

    return jsonify({
        'message': error
    }), 400

@match.route('/match/end/<uuid>', methods=['GET'])
@jwt_required
def endMatch(uuid):
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    match = db.session.query(Match).filter_by(uuid=uuid).first()

    if not match:
        return 404
    elif 0 == match.live:
        error = 'Cannot end matches that are not in progress.'
    elif match.user_id != claims['id']:
        error = 'Cannot end matches owned by other users.'

        return jsonify({
            'message': error
        }), 401
    else:
        try:
            match.live = 0
            db.session.commit()

            timing_meta = {
                'elapsed_time': int(datetime.datetime.utcnow().timestamp()) - match.created_at
            }

            match_meta = MatchMeta(
                uuid,
                'timing',
                timing_meta
            )
            db.session.add(match_meta)
            db.session.commit()

            uri = f'/match/view/{match.uuid}'
            message = 'Match ended successfully.'

            return jsonify({
                'match_uri': uri,
                'message': message
            }), 200
        except AttributeError:
            error = 'Match could not be ended.'

            return jsonify({
                'message': error
            }), 400

    return jsonify({
        'message': error
    }), 400
