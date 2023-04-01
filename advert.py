from schema import validate_create_item, ValidateGetItem
from flask import jsonify, request, Blueprint, session
from users import is_authenticated, is_owner
from model import Session, Advertisement
from flask.views import MethodView
from http_errors import HttpError

bp = Blueprint('advert', __name__, url_prefix='/advert')


def get_item(item_id, session, model):
    item = session.get(model, item_id)
    if not item:
        raise HttpError(404, 'Not found')
    return item


def add_item(data, session, model):
    new_item = model(**data)
    session.add(new_item)
    session.commit()


def patch_item(stmt, data, session):
    for key, val in data.items():
        setattr(stmt, key, val)
    session.commit()


def delete_item(stmt, session):
    session.delete(stmt)
    session.commit()


@bp.errorhandler(HttpError)
def error_handler(error):
    return jsonify({'message': error.message}), error.code


class AdvertView(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model

    def get(self, item_id):
        with Session as sess:
            stmt = get_item(item_id, sess, self.model)
            serialized = ValidateGetItem.from_orm(stmt).dict()
        return jsonify(serialized)

    @is_authenticated
    def post(self):
        with Session as sess:
            user = session.get('user')
            request.json['owner_id'] = user
            validated_data = validate_create_item(request.json)
            add_item(validated_data, sess, self.model)
        return jsonify({'method': 'POST', 'status': 'OK'})

    @is_authenticated
    def delete(self, item_id):
        with Session as sess:
            stmt = get_item(item_id, sess, self.model)
            if is_owner(stmt):
                delete_item(stmt, sess)
                return jsonify({'method': 'DELETE', 'resonse': 'ok'})
            return jsonify({'status': 'error', 'message': 'not owner'})

    @is_authenticated
    def patch(self, item_id):
        with Session as sess:
            data = request.json
            stmt = get_item(item_id, session, self.model)
            if is_owner(stmt):
                patch_item(stmt, data, sess)
                return jsonify({'method': 'PATCH', 'resonse': 'ok'})
            return jsonify({'status': 'error', 'message': 'not owner'})


bp.add_url_rule('/<int:item_id>', view_func=AdvertView.as_view(
    'advt_mod', Advertisement), methods=['GET', 'PATCH', 'DELETE'])
bp.add_url_rule('/', view_func=AdvertView.as_view(
    'advt_create', Advertisement), methods=['POST'])
