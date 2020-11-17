from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, jwt_required

from app.database import db
from app.matrix.generator import MatrixGenerator
from app.matrix.position import TurnPositions
from app.models.match import Match
from app.models.match_meta import MatchMeta

turn = Blueprint('turn', __name__)

@turn.route('/turn/update/<uuid>', methods=['POST'])
@jwt_required
def nextTurn(uuid):
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    if 'POST' == request.method:
        if not username:
            error = 'Invalid username identity.'
        else:
            match = db.session.query(Match).filter_by(uuid=uuid).first()

            if not match:
                return 404
            elif 0 == match.live:
                error = 'Cannot update matches that are not in progress.'
            elif match.user_id != claims['id']:
                error = 'Cannot update matches owned by other users.'

                return jsonify({
                    'message': error
                }), 401
            else:
                turn_meta = db.session.query(MatchMeta).filter_by(match_id=uuid, key='turns').first()

                if not turn_meta:
                    match_meta = MatchMeta(
                        uuid,
                        'turns',
                        request.json
                    )
                
                db.session.add(match_meta)
                db.session.commit()

                message = 'Turn completed.'

                return jsonify({
                    'message': message
                }), 200

    return jsonify({
        'message': error
    }), 400

@turn.route('/turn/view/<uuid>/<turn_number>', methods=['GET'])
@jwt_required
def viewTurn(uuid, turn_number):
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    turn_number = int(turn_number) - 1
    match = db.session.query(Match).filter_by(uuid=uuid).first()

    if not match:
        return 404
    elif match.user_id != claims['id']:
        error = 'Cannot view matches owned by other users.'

        return jsonify({
            'message': error
        }), 401
    else:
        turn_meta = db.session.query(MatchMeta).filter_by(match_id=uuid, key='turns').first()

        if not turn_meta:
            error = 'Match does not have any turns completed.'
        else:
            try:
                turn_meta = turn_meta.value['turns'][turn_number]

                positions = TurnPositions(turn_meta).parse()

                if str == type(positions):
                    error = positions

                    return jsonify({
                        'message': error
                    })
                
                matrix = MatrixGenerator(positions).generate()

                message = 'Turn data retrieved successfully.'

                return jsonify({
                    'data': turn_meta,
                    'matrix': matrix,
                    'message': message
                })
            except IndexError:
                error = 'Invalid turn number provided.'

    return jsonify({
        'message': error
    }), 400
