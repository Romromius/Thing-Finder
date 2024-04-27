import datetime
from flask import Flask, render_template, request, url_for, redirect, abort

import api_resources
from data import db_session
from data.__all_models import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

import os
from telebot import TeleBot
import logging

db_session.global_init("db/TF_db.sqlite")
session = db_session.create_session()


# def send_email(msg):
#     sender = os.getenv("MAIL")
#     password = os.getenv("PASSWORD")
#
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#
#     server.login(sender, password)
#     server.sendmail(sender, sender, msg)
#
#     server.quit()
#     send_email("Тук-тук")


def register_user(name, email, password):
    """
    Функция регистрирует пользователя
    (данные с сайта)
    :param name: имя
    :param email: почту
    :param password: пароль
    :return: None
    """
    user = User()
    user.name = name
    user.email = email
    user.set_password(password)
    session.add(user)
    session.commit()


def add_item(photo, type, name, props):
    """
    :param photo:
    :param type:
    :param name:
    :param params:
    :return:
    """
    item = Item()
    item.owner = current_user.id
    item.name = name
    match type:
        case 'Пропажа':
            item.type = 0
        case 'Нахождение':
            item.type = 1
    item.status = 0
    session.add(item)
    session.commit()

    if photo:
        photo.save(f'static/img/{item.id}.png')

    for i in props:
        description = Description()
        description.item = item.id
        description.value = session.query(PropValue).filter(PropValue.value == i).first().id
        session.add(description)
        session.commit()

    checkout(item.id)


def checkout(item_id: int):
    item = session.get(Item, item_id)
    variants = item.seek_for_variants()
    logging.info('CHECKOUT FOR' + str(item_id) + str(variants))
    for i in variants:
        goal = session.get(Item, i)
        send_notification(session.get(User, goal.owner),
                          f'Найдено совпадение для объявления "{goal.name}".\n'
                          f'Вы ищите "{item.name}"?\nПроверьте личный кабинет и ответьте командой "/accept {item.id} {goal.id}" или проигнорируйте.')
        break


def send_notification(user: User, notification: str):
    bot = TeleBot('6748575861:AAFkjSEXI0hxtNhU-Z8orkBeS4pR4s9_kN4')
    if not user.tg:
        print(user.name, 'has no tg')
        return
    bot.send_message(int(user.tg), notification)


# \/----------------ОБРАБОТЧИКИ--------------\/
app = Flask('Lost_Watermelon')
app.secret_key = 'GLORY TO THE WATERMELON!!!'
app.permanent_session_lifetime = datetime.timedelta(days=61)
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@app.context_processor
def handle_context():
    return dict(os=os)


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html')


@app.errorhandler(500)
def not_found(error):
    params = {
        'error': error
    }
    return render_template('internal_error.html', **params)


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/index')  # finished
@app.route('/')
def site():
    params = {
        "url": url_for('static', filename='css/style.css'),
        "lst": session.query(Item).filter(Item.type == "0").filter(Item.status == "1").all(),
    }
    return render_template("home.html", **params)


@app.route("/form_ad", methods=['GET', 'POST'])
def form_ad():
    if current_user.is_authenticated:
        form = AdForm()
        if form.validate_on_submit():
            photo = request.files['photo']
            if form.name.data is not None:
                add_item(photo, form.type.data, form.name.data, form.props.data)
                return render_template("successfully.html")
            return render_template('form_ad.html', msg="Поле названия осталось пустым", form=form)
        return render_template("form_ad.html", form=form)
    return redirect('/login')


@app.route("/cabinet")  # finished
def lk():
    if current_user.is_authenticated:
        cur_user_id = current_user.id
        params = {
            "lst": session.query(Item).filter(Item.owner == cur_user_id).all(),
        }
        return render_template("lk.html", **params)
    return redirect('/login')


@app.route("/login", methods=['GET', 'POST']) 
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/cabinet")
        return render_template('login.html', msg="Неправильный логин или пароль", form=form)
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=['GET', 'POST'])  
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.password.data, form.password_again.data)
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, msg="Пароли не совпадают")
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, msg="Такой пользователь уже есть")
        register_user(form.name.data, form.email.data, form.password.data)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/catdocs")  
def catdocs():
    return render_template("catdocs.html")


@app.route("/donate")  
def donate():
    params = {"url_img": url_for(endpoint="static", filename="img/donate.png")}
    return render_template("donate.html", **params)


@app.route("/test_function")
def check_out():
    checkout(3)
    return render_template("successfully.html")


@app.route('/error')
def error():
    raise Exception


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    api.add_resource(api_resources.UsersResource, '/api/user')
    api.add_resource(api_resources.ItemResource, '/api/item')
    app.run(debug=False, port=port, host='0.0.0.0')
