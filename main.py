import datetime
from flask import Flask, render_template, request, url_for, redirect, abort
from data import db_session
from data.__all_models import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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
#     send_email("Тук-тук")


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
app.secret_key = b'fa22ca826F3+c02aef6cf_9572196a7$9c7e7dd3f2443a70e390#$0d3f7X0d4071ab8ec\n\xec]/'
app.permanent_session_lifetime = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)


@app.context_processor
def handle_context():
    return dict(os=os)


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html')


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/index')  # finished
@app.route('/')
def site():
    params = {
        "url": url_for('static', filename='css/style.css'),
        "lst": session.query(Item).filter(Item.type == "0").filter(Item.status == "1").all(),
        "colors": ["red", "blue", "orange", "aquamarine", "yellow", "tomato", "pink", "white", "purple"]
    }
    return render_template("home.html", **params)


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
    # params = {
    #     'props': ['Красный', 'Синий', 'Белый']
    # }
    if 'GET' == request.method:
        return render_template("form_ad.html", **params)

    for i in list(request.form.keys()):
        print(i, request.form.get(i))

    params = {"verdict": "Ваша форма отправлена успешно!"}
    return render_template("index_ads.html", **params)


@app.route("/cabinet")  # finished
def lk():
    if current_user.is_authenticated:
        cur_user_id = current_user.id
        params = {
            "lst": session.query(Item).filter(Item.owner == cur_user_id).all(),
            "colors": ["red", "blue", "orange", "aquamarine", "yellow", "tomato", "pink", "glive", "teal"]
        }
        return render_template("lk.html", **params)
    return redirect('/login')


@app.route("/login", methods=['GET', 'POST'])  # finished
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


@app.route("/register", methods=['GET', 'POST'])  # finished
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, msg="Пароли не совпадают")
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, msg="Такой пользователь уже есть")
        if form.tg.data[:13] != "https://t.me/":
            return render_template('register.html', form=form, msg="Неправильный формат ссылки на телеграм")
        register_user(form.name.data, form.email.data, form.password.data, form.tg.data)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/catdocs")  # finished
def catdocs():
    return render_template("catdocs.html")


@app.route("/donate")  # finished
def donate():
    return render_template("donate.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host='127.0.0.1')  # 0.0.0.0
