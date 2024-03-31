from data import db_session
from data.__all_models import *
import logging

logging.basicConfig(level=logging.DEBUG)

db_session.global_init('db/TF_db.sqlite')
session = db_session.create_session()
item = session.query(Item).first()
print(f'Предмет: {item.name}')
print('Изображение:', item.photo)
print('Приметы:')
for i in session.query(Desc).join(Prop).filter(Desc.item_id == item.id):
    print(f'> {session.query(Prop).filter(Prop.id == i.prop_id).first().name}:\t{i.value}')
