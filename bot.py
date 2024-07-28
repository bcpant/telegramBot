import random
import telebot
from telebot import types

import GameMods
import dbUsers
import keyboard

from config import TOKEN
from config import dbPath

bot = telebot.TeleBot(TOKEN)
user_answers = {}


def play_immortal_mode(message):
    getWord = GameMods.BotGames(dbPath)
    user_answers[message.chat.id] = {
        'message_id': message.id,
        'true_answer': getWord.trueAnswer,
    }
    options = [getWord.trueAnswer, getWord.wrongAnswer1, getWord.wrongAnswer2, getWord.wrongAnswer3]
    random.shuffle(options)
    markup = types.InlineKeyboardMarkup(row_width=2)

    for option in options:
        callback_data = 'good' if option == getWord.trueAnswer else 'bad'
        item = types.InlineKeyboardButton(option, callback_data=callback_data)
        markup.add(item)
    bot.send_message(message.chat.id, f'Загаданное слово: *{getWord.askedWord}*', reply_markup=markup,
                     parse_mode='Markdown')


def play_three_lives_mode(message, lives=3, guessed_words=0):
    getWord = GameMods.BotGames(dbPath)
    user_answers[message.chat.id] = {
        'message_id': message.id,
        'true_answer': getWord.trueAnswer,
        'lives': lives,  # Сохранение количества жизней
        'guessed_words': guessed_words  # Сохранение количества угаданных слов
    }
    options = [getWord.trueAnswer, getWord.wrongAnswer1, getWord.wrongAnswer2, getWord.wrongAnswer3]
    random.shuffle(options)
    markup = types.InlineKeyboardMarkup(row_width=2)

    for option in options:
        callback_data = 'good' if option == getWord.trueAnswer else 'bad'
        item = types.InlineKeyboardButton(option, callback_data=callback_data)
        markup.add(item)
    bot.send_message(message.chat.id, f'Загаданное слово: *{getWord.askedWord}*', reply_markup=markup,
                     parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def welcome(message):
    user = dbUsers.Db(dbPath)
    print(message.from_user.id)
    if not user.user_exists(message.from_user.id):
        user.add_user(message.from_user.id, message.chat.id)
    user.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(keyboard.menuItem1, keyboard.menuItem2, keyboard.menuItem3)
    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!'.format(message.from_user, bot.get_me()),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess_hadl(message):
    if message.chat.type == 'private':
        if message.text == 'Бесконечный режим':
            play_immortal_mode(message)
        elif message.text == 'Три жизни':
            play_three_lives_mode(message)
        elif message.text == 'Статистика':
            db = dbUsers.Db(dbPath)
            rightAnswers = db.get_true_srvc(message.from_user.id)
            wrongAnswers = db.get_wrong_srvc(message.from_user.id)
            survRec = db.get_lives_mode(message.from_user.id)
            totalCount = rightAnswers + wrongAnswers
            if totalCount != 0:
                nonRoundRightProc = (rightAnswers / (rightAnswers + wrongAnswers)) * 100
                rightProc = round(nonRoundRightProc, 2)
            else:
                rightProc = 0
            chat_id = message.chat.id
            stats_message = (
                f'🏁*Общая статистика*\n'
                f'*------------------------------------*\n'
                f'🔢Слов проверено: {totalCount}\n'
                f'✅Правильных ответов: {rightAnswers}\n'
                f'❌Неправильных ответов: {wrongAnswers}\n'
                f'✍️Процент правильных ответов: {float(rightProc)}%\n'
                f'*------------------------------------*\n'
                f'❤️❤️❤️ Рекорд: {survRec}'
            )
            markup = types.InlineKeyboardMarkup(row_width=2)
            item = types.InlineKeyboardButton('Обнулить статистику', callback_data='refreshStats')
            markup.add(item)
            bot.send_message(chat_id, stats_message, reply_markup=markup, parse_mode='Markdown')
            db.close()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global db
    try:
        if call.message:
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            print(user_id)
            user_data = user_answers.get(chat_id, {})
            lives = user_data.get('lives', None)
            guessed_words = user_data.get('guessed_words', 0)
            db = dbUsers.Db(dbPath)

            # Убираем старую клавиатуру
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

            if call.data == 'good':
                guessed_words += 1
                reply_message = (
                    f'Правильно!\n'
                )
                bot.send_message(chat_id, reply_message)
                db.add_true_survansw(user_id=user_id)
                if lives:
                    play_three_lives_mode(call.message, lives=lives, guessed_words=guessed_words)
                else:
                    play_immortal_mode(call.message)
            elif call.data == 'bad':
                correct_answer = user_data.get('true_answer')
                db.add_wrong_surwansw(user_id=user_id)
                if lives:
                    reply_message = (
                        f'Вы ошиблись, верный перевод: {correct_answer}\n'
                        f'Осталось {lives - 1} ❤️\n'
                    )
                    bot.send_message(chat_id, reply_message)
                else:
                    reply_message = (
                        f'Вы ошиблись, верный перевод: {correct_answer}\n'
                    )
                    bot.send_message(chat_id, reply_message)
                if lives:
                    lives -= 1
                    if lives <= 0:
                        if db.livesModeRecord(user_id, guessed_words):
                            bot.send_message(chat_id, f'Игра окончена.\n'
                                                  f'Слов отгадано: {guessed_words}\n'
                                                  f'Поздравляю! Вы установили новый рекорд!')
                        else:
                            bot.send_message(chat_id, f'Игра окончена.\n'
                                                      f'Слов отгадано: {guessed_words}\n')
                    else:
                        play_three_lives_mode(call.message, lives=lives, guessed_words=guessed_words)
                else:
                    play_immortal_mode(call.message)
            elif call.data == 'refreshStats':
                db.refresh_the_stats(user_id=chat_id)
                bot.send_message(chat_id, 'Статистика обнулена.')
    except Exception as e:
        print(repr(e))
    finally:
        db.close()

bot.polling(non_stop=True)
