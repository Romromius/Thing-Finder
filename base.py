from data import db_session
from data.__all_models import *
import logging

logging.basicConfig(level=logging.DEBUG)

db_session.global_init('db/TF_db.sqlite')
session = db_session.create_session()
items = session.query(Item).all()
for i in items:
    print(i.name)
    print('Приметы:')
    [print('>', j) for j in i.get_props()]
    print('-----\n')

items[3].set_image(open('png-clipart-ryuko-matoi-senketsu-scissors-blade-paper-scissors-technic-scissors.png', 'rb').read())
