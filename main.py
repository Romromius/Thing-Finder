from data import db_session

db_session.global_init('db/TF_db.sqlite')
session = db_session.create_session()
