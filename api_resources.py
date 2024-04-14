from flask_restful import reqparse, abort, Api, Resource
from flask import *
from data.db_session import *
from data.__all_models import *


def abort_if_user_not_found(user_name):
    session = create_session()
    user = session.query(User).filter(User.name == user_name).first()
    if not user:
        # abort(404, message=f"User {user_name} not found")
        abort(404, f"User {user_name} not found")


def abort_if_item_not_found(item_id):
    session = create_session()
    user = session.get(Item, item_id)
    if not user:
        abort(404, message=f"Item {item_id} not found")


class UsersResource(Resource):
    def get(self, user_name):
        abort_if_user_not_found(user_name)
        session = create_session()
        user = session.query(User).filter(User.name == user_name).first()
        return jsonify({'user': user.to_dict(only=('name', 'email', 'tg'))})


class ItemResource(Resource):
    def get(self, item_id, user_name, password):
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
