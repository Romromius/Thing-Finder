import _io
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, SelectField, FileField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import DataRequired

from sqlalchemy import *
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
import os

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase, create_session


# Base = declarative_base()

def jaccard_similarity(set1: set, set2: set) -> float:
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    tg = Column(String, unique=True)
    name = Column(String, unique=True)
    hashed_password = Column(String)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Item(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    type = Column(Integer)
    status = Column(Boolean, default=0)

    def seek_for_variants(self):
        variants = {}
        session = create_session()
        for item in session.query(Item).filter(Item.type != self.type, Item.id != self.id):
            if jaccard_similarity(set(self.get_props()), set(item.get_props())) > 0.1:
                variants[item.name] = jaccard_similarity(set(self.get_props()), set(item.get_props()))

        del session
        return {k: v for k, v in sorted(variants.items(), key=lambda x: x[1], reverse=True)}

    def get_props(self):
        session = create_session()
        fancy_props = []
        for description in session.query(Description).filter(Description.item == self.id):
            prop_value = session.query(PropValue).filter_by(id=description.value).first()
            if prop_value:
                fancy_props.append(prop_value.value)
        del session
        return fancy_props

    def set_image(self, file: bytes):
        with open(f'static/item_images/{self.id}.png', 'wb') as f:
            f.write(file)

    def add_prop(self, prop_id):
        session = create_session()
        description = Description()
        description.item = self.id
        description.value = session.query(PropValue).filter(PropValue.id == prop_id).first().id
        session.add(description)
        session.commit()

    def get_owner(self) -> User:
        session = create_session()
        return session.get(User, self.owner)


class Property(SqlAlchemyBase):
    __tablename__ = "prop_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Description(SqlAlchemyBase):
    __tablename__ = "descriptions"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(Integer, ForeignKey('items.id'))
    value = Column(String, ForeignKey('prop_values.id'))


class PropValue(SqlAlchemyBase):
    __tablename__ = "prop_values"

    id = Column(Integer, primary_key=True)
    type = Column(Integer, ForeignKey('prop_types.id'))
    value = Column(String)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    tg = StringField('Телеграм', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class AdForm(FlaskForm):
    type = SelectField('Тип объявления', choices=['1', '0'], validators=[DataRequired()])
    name = StringField('Название предмета', validators=[DataRequired()])
    amount = SelectField('Количество', choices=['none', 'Один', 'Несколько', 'Множество'], validators=[DataRequired()])
    color = SelectField('Цвет', choices=['none', 'Разноцветный', 'Красный', 'Синий', 'Зеленый', 'Желтый', 'Оранжевый',
                                         'Фиолетовый', 'Розовый', 'Темно-синий', 'Темно-красный', 'Темно-зеленый',
                                         'Бордовый', 'Коричневый', 'Черный', 'Белый'], validators=[DataRequired()])
    material = SelectField('Материал', choices=['none', 'Дерево', 'Металл', 'Пластмасса', 'Стекло', 'Ткань', 'Резина'],
                           validators=[DataRequired()])
    defects = SelectField('Дефекты', choices=['none', 'Нет', 'Царапины', 'Трещины', 'Вмятины', 'Изношенный'], validators=[DataRequired()])
    case = SelectField('В чехле', choices=['none', 'Нет', 'Да'], validators=[DataRequired()])
    prod = SelectField('Производитель', choices=['none', 'Россия', 'Сша', 'Япония', 'Китай', 'Другое'], validators=[DataRequired()])
    Form = SelectField('Форма', choices=['none', 'Круглый', 'Квадратный', 'Прямоугольный', 'Полукруглый', 'Цилиндр'], validators=[DataRequired()])
    size = SelectField('Размер', choices=['none', 'мельчайший', 'маленький', 'средний', 'большой', 'огромный'], validators=[DataRequired()])
    strength = SelectField('Прочность', choices=['none', 'хрупчайший', 'хрупкий', 'нормальный', 'бронированный'], validators=[DataRequired()])
    other = SelectField('Другое', choices=['none', 'неприятный запах', 'приятный запах', 'грязный', 'опасный', 'живой', 'старый'], validators=[DataRequired()])
    submit = SubmitField('Отправить')

