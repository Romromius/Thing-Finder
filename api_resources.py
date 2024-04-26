from flask_restful import abort, Resource, reqparse
from flask import *
from data.db_session import *
from data.__all_models import *


def abort_if_user_not_found(user_name):
    session = create_session()
    user = session.query(User).filter(User.name == user_name).first()
    if not user:
        abort(404, f"User {user_name} not found")


def abort_if_item_not_found(item_id):
    session = create_session()
    user = session.get(Item, item_id)
    if not user:
        abort(404, f"Item {item_id} not found")


class UsersResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user', type=str, required=True)
    def get(self):
        user_name = self.parser.parse_args()['user']
        abort_if_user_not_found(user_name)
        session = create_session()
        user = session.query(User).filter(User.name == user_name).first()
        return jsonify({'user': user.to_dict(only=('name', 'email', 'tg'))})


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('user', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    parser.add_argument('status', type=int, required=False)

    def get(self):
        args = self.parser.parse_args()

        item_id = args['id']
        user_name = args['user']
        password = args['password']

        abort_if_user_not_found(user_name)
        abort_if_item_not_found(item_id)
        session = create_session()
        user = session.query(User).filter(User.name == user_name).first()
        item = session.get(Item, item_id)
        if not user.check_password(password):
            abort(403, 'Wrong password')
        if item.owner != user.id and item.status == 0:
            abort(403, 'User has no access to this item')
        return jsonify({'params': item.to_dict(only=('name', 'type', 'status')), 'props': item.get_props()})

    def post(self):
        args = self.parser.parse_args()

        item_id = args['id']
        user_name = args['user']
        password = args['password']
        status = args['status']

        abort_if_user_not_found(user_name)
        abort_if_item_not_found(item_id)
        session = create_session()
        user = session.query(User).filter(User.name == user_name).first()
        item = session.get(Item, item_id)
        if not user.check_password(password):
            abort(403, 'Wrong password')
        if item.owner != user.id and item.status == 0:
            abort(403, 'User has no access to this item')
        item = session.get(Item, item_id)
        if status in [0, 1]:
            item.status = status
            session.commit()
        else:
            abort(400, 'Invalid status')
        return jsonify({'message': 'OK'})
