import asyncio

from telebot import TeleBot
from data.db_session import *
from data.__all_models import *

token = '6748575861:AAFkjSEXI0hxtNhU-Z8orkBeS4pR4s9_kN4'
global_init('db/TF_db.sqlite')

bot = TeleBot(token)


def extract_arg(arg):
    return arg.split()[1:]


def send_notification(username: str, notification: str):
    session = create_session()
    user = session.query(User).filter(User.name == username).first()
    bot.send_message(user.tg, notification)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Здравствуйте! Вам доступны следующие команды: '/register <ваш ник> <ваш пароль>', '/unregister'")
    session = create_session()
    user = session.query(User).filter(User.tg == message.from_user.id).first()
    if user:
        bot.send_message(message.from_user.id, f'{user.name}!')
    else:
        bot.send_message(message.from_user.id, 'Вы не зарегистрированы.')


@bot.message_handler(commands=['register'])
def register(message):
    session = create_session()
    status = extract_arg(message.text)
    try:
        if len(status) != 2:
            raise IndexError
        user = session.query(User).filter(User.name == status[0]).first()
        if not user:
            bot.send_message(message.from_user.id, 'Пользователь не найден. Вы верно ввели имя пользователя?')
            return
        if not user.check_password(status[1]):
            bot.send_message(message.from_user.id, 'Неверный пароль.')
            return
        user.tg = message.from_user.id
        session.commit()
        bot.delete_message(message.from_user.id, message.id)
        bot.send_message(message.from_user.id, 'Вы авторизованы.')
    except IndexError:
        bot.send_message(message.from_user.id, 'Аргументы указаны неверно.')


@bot.message_handler(commands=['unregister'])
def unregister(message):
    session = create_session()
    user = session.query(User).filter(User.tg == message.from_user.id).first()
    if not user:
        bot.send_message(message.from_user.id, 'Вы и так не зарегистрированы.')
        return
    user.tg = None
    session.commit()
    bot.send_message(message.from_user.id, 'Вы деавторизованы. Прощайте 😢😭😩')


@bot.message_handler(commands=['accept'])
def accept(message):
    session = create_session()
    id1, id2 = extract_arg(message.text)[0], extract_arg(message.text)[1]
    try:
        item1 = session.query(Item).get(id1)
        item2 = session.query(Item).get(id2)
        email = item1.get_owner().email
        item1.status = 1
        item2.status = 1
        session.commit()
        bot.send_message(message.from_user.id, f'вот почта owner, свяжитесь с ним! {email}.')
    except Exception:
        bot.send_message(message.from_user.id, 'Один из id не найден в таблице! Повторите.')


@bot.message_handler(commands=['test'])
def te(message):
    send_notification('Romromius', 'Hello')


def run_bot():
    print('running', bot.user.first_name)
    bot.infinity_polling()

run_bot()
