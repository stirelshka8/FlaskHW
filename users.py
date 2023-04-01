from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify, request, Blueprint, session
from schema import validate_create_user
from http_errors import HttpError
from model import Session, User
from sqlalchemy import select

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.errorhandler(HttpError)
def error_handler(error):
    return jsonify({'message': error.message}), error.code


def user_get(sess, name):
    selected_user = sess.scalar(select(User).where(User.name == name))
    return selected_user


@bp.route('/register', methods=['POST'])
def user_register():
    validated_data = validate_create_user(request.json)
    validated_data['pwd'] = generate_password_hash(validated_data.get('pwd'))
    with Session as sess:
        stmt = user_get(sess, validated_data['name'])
        if stmt:
            return jsonify({'status': 'error', 'message': 'alrady exists'})
        user = User(**validated_data)
        sess.add(user)
        sess.commit()
    return jsonify({'status': 'user added'})


@bp.route('/login', methods=['POST'])
def user_login():
    session.clear()
    data = request.json
    with Session as sess:
        user = user_get(sess, data['name'])
        if check_password_hash(user.pwd, data['pwd']):
            session.update({'user': user.id})
            return jsonify({'status': 'authenticated'})
        raise HttpError(404, 'Not found')


@bp.route('/logout', methods=['POST'])
def user_logout():
    session.clear()
    return jsonify({'status': 'not authenticated'})


def is_authenticated(func):
    def wrapper(*args, **kwargs):
        if session.get('user'):
            res = func(*args, **kwargs)
            return res
        return {'status': 'error', 'message': 'please authorize'}

    return wrapper


def is_owner(stmt):
    return True if session.get('user') == stmt.owner_id else False
