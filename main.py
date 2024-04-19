import datetime

from flask import Flask, render_template, request, url_for, redirect
from data import db_session
from data.__all_models import *
import smtplib
from email.mime.multipart import MIMEMultipart
import os

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
    # send_email("ququ")


def register_user(name, email, password, tg):
    """
    функция регистрирует пользователя
    (данные с сайта)
    :param name: имя
    :param email: почту
    :param password: пароль
    :param tg: ссылку тг
    :return: None
    """
    user = User()
    user.name = name
    user.email = email
    user.tg = tg
    user.set_password(password)
    session.add(user)
    session.commit()


# \/----------------ОБРАБОТЧИКИ--------------\/
app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


@app.route('/index')  # ON FINISH LINE
@app.route('/')
def site():
    params = {
        "url": url_for('static', filename='css/style.css'),
        "lst": session.query(Item).filter(Item.type == "0").filter(Item.status == "1").all(),
        "colors": ["red", "blue", "orange", "aquamarine", "yellow", "tomato", "pink", "glive", "teal"]
    }
    return render_template("index_ads.html", **params)


@app.route("/form_ad", methods=['GET', 'POST'])  # NEED A BUTTON
def form_ad():
    params = {
        'amount': ['один', 'несколько', 'множество'],
        'color': ['разноцветный', 'красный', 'синий', 'зеленый', 'желтый', 'оранжевый',
                  'фиолетовый', 'розовый', 'темно-синий', 'темно-красный', 'темно-зеленый',
                  'бордовый', 'коричневый', 'черный', 'белый'],
        'material': ['дерево', 'металл', 'пластмасса', 'стекло', 'ткань', 'резина'],
        'defects': ['нет', 'царапины', 'трещины', 'вмятины', 'изношенный'],
        'case': ['нет', 'да'],
        'prod': ['Россия', 'Сша', 'Япония', 'Китай', 'другое'],
        'form': ['круглый', 'квадратный', 'прямоугольный', 'полукруглый', 'цилиндр'],
        'size': ['мельчайший', 'маленький', 'средний', 'большой', 'огромный'],
        'strength': ['хрупчайший', 'хрупкий', 'нормальный', 'бронированный'],
        'other': ['неприятный запах', 'приятный запах', 'грязный', 'опасный', 'живой', 'старый']
    }
    if 'GET' == request.method:
        return render_template("form_ad.html", **params)

    for i in list(request.form.keys()):
        print(i, request.form.get(i))

    params = {"verdict": "Ваша форма отправлена успешно!"}
    return render_template("index_ads.html", **params)


@app.route("/lk")  # NEED A COOKIE
def lk():
    const = "4"
    params = {
        "lst": session.query(Item).filter(Item.owner == const).all(),
        "colors": ["red", "blue", "orange", "aquamarine", "yellow", "tomato", "pink", "glive", "teal"]
        }
    return render_template("lk.html", **params)


@app.route("/login", methods=['GET', 'POST'])  # NEED A REALIZATION
def login():
    params = {}
    if 'GET' == request.method:
        return render_template("login.html", **params)

    ...
    return redirect("/lk")


@app.route("/register", methods=['GET', 'POST'])  # finished
def register():
    params = {
        "name": "ok",
        "email": "ok",
        "pass": "ok",
        "tg": "ok",
        "botcheck": "ok"
    }
    if 'GET' == request.method:
        return render_template("register.html", **params)

    for i in list(request.form.keys()):
        print(i, request.form.get(i))

    if request.form.get("name") in [i.name for i in session.query(User).all()]:
        params["name"] = "!"
    if request.form.get("email") in [i.email for i in session.query(User).all()]:
        params["email"] = "!"
    if request.form.get("pass1") != request.form.get("pass2"):
        params["pass"] = "!"
    if request.form.get("tg")[:13] != "https://t.me/":
        params["tg"] = "!"
    if request.form.get("botcheck") is None:
        params["botcheck"] = "!"

    for ok in params.values():
        if ok != "ok":
            return render_template("register.html", **params)

    register_user(request.form.get("name"), request.form.get("email"), request.form.get("pass1"),
                  request.form.get("tg"))

    return redirect("/login")


@app.route("/catdocs")  # finished
def catdocs():
    return render_template("catdocs.html")


@app.route("/donate")  # finished
def donate():
    return render_template("donate.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host='127.0.0.1')  # 0.0.0.0
