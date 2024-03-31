from sqlalchemy import *
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


Base = declarative_base()


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Item(SqlAlchemyBase):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo = Column(String)
    status = Column(Boolean)


class Prop(SqlAlchemyBase):
    __tablename__ = "props"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Desc(SqlAlchemyBase):
    __tablename__ = "descriptions"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    prop_id = Column(Integer, ForeignKey('props.id'))
    value = Column(String)
