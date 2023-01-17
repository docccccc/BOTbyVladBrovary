import re
import sqlite3, random, os, datetime, time
import uuid

import telebot
from telebot import *
import config, menu, func, db, os
from telebot import types

from dbmng import curer

dictKunaEvent = {}


def start_bot():
    print(
        f'\n----------------------------------------------\nБот успешно запущен!!!\n Время запуска: {datetime.datetime.now()}\n')
    product_dict = {}
    db.db()
    bot = telebot.TeleBot(config.BOT_TOKEN)
    print(bot.get_me())

    @bot.message_handler(commands=['start'])
    def handler_start(message):

        chat_id = message.chat.id
        name = message.from_user.username
        ref_code = message.text[7:]
        func.first_start(chat_id, name, ref_code)

        if func.is_kur(message.chat.id):
            bot.send_message(chat_id=chat_id,
                             text=f'Рад приветствовать тебя дружище в БОТе от ✅ Your Dealer ✅\nЯ работаю 24/7, чтобы ТЫ имел возможность приобрести наш товар в любое время суток 😉\n\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n🔮 Для покупки товара сначала нужно 💰Пополнить баланс💰\n📌 Перед пополнением проверь наличие товара, выбрав количество (0.5г или 1г), в случае если товара не будет, но деньги будут положены на баланс БОТа, придется ждать пополнения готовыми кладами📌\n⛔️Вывод средств - недоступен⛔️\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n\n📱И немного полезных ссылок нашего магазина 📱\n🥳 Отзывы - @your_dealer_reviews 🥳\n📰 Новости - @your_dealer_news 📰\n❗️Если возникнут проблемы, обращайся к оператору❗️',
                             reply_markup=menu.kur_main_menu)
        elif func.is_adm(message.chat.id):
            bot.send_message(chat_id=chat_id,
                             text=f'Рад приветствовать тебя дружище в БОТе от ✅ Your Dealer ✅\nЯ работаю 24/7, чтобы ТЫ имел возможность приобрести наш товар в любое время суток 😉\n\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n🔮 Для покупки товара сначала нужно 💰Пополнить баланс💰\n📌 Перед пополнением проверь наличие товара, выбрав количество (0.5г или 1г), в случае если товара не будет, но деньги будут положены на баланс БОТа, придется ждать пополнения готовыми кладами📌\n⛔️Вывод средств - недоступен⛔️\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n\n📱И немного полезных ссылок нашего магазина 📱\n🥳 Отзывы - @your_dealer_reviews 🥳\n📰 Новости - @your_dealer_news 📰\n❗️Если возникнут проблемы, обращайся к оператору❗️',
                             reply_markup=menu.adm_main_menu)
        else:
            bot.send_message(chat_id=chat_id,
                             text=f'Рад приветствовать тебя дружище в БОТе от ✅ Your Dealer ✅\nЯ работаю 24/7, чтобы ТЫ имел возможность приобрести наш товар в любое время суток 😉\n\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n🔮 Для покупки товара сначала нужно 💰Пополнить баланс💰\n📌 Перед пополнением проверь наличие товара, выбрав количество (0.5г или 1г), в случае если товара не будет, но деньги будут положены на баланс БОТа, придется ждать пополнения готовыми кладами📌\n⛔️Вывод средств - недоступен⛔️\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n\n📱И немного полезных ссылок нашего магазина 📱\n🥳 Отзывы - @your_dealer_reviews 🥳\n📰 Новости - @your_dealer_news 📰\n❗️Если возникнут проблемы, обращайся к оператору❗️',
                             reply_markup=menu.main_menu)

    @bot.message_handler(commands=['adm', 'admmenu', 'adm_menu'])
    def wrapper(message):
        if func.is_adm(message.chat.id):
            bot.send_message(chat_id=message.chat.id, text=f'Добро пожаловать, ADMIN', reply_markup=menu.adm_menu)

    @bot.message_handler(commands=['kur', 'kurmenu', 'kur_menu'])
    def wrapper(message):
        if func.is_kur(message.chat.id):
            bot.send_message(chat_id=message.chat.id, text=f'Добро пожаловать, Курьер', reply_markup=menu.kur_menu)

    @bot.message_handler(content_types=['text'])
    def text_wrapper(message):
        if message.text == '1':
            conn, cursor = db.connect()

            for i in "qwerty":
                last = cursor.execute('select max(person_id) from address').fetchone()[0]
                cursor.execute('insert into address values(?,1,?)', (i, last + 1,))
                conn.commit()
            cursor.close()
            conn.close()
        elif message.text == 'adm':
            if func.is_adm(message.chat.id):
                bot.send_message(chat_id=message.chat.id, text=f'Добро пожаловать, ADMIN', reply_markup=menu.adm_menu)
        elif message.text == 'kur':
            if func.is_kur(message.chat.id):
                bot.send_message(chat_id=message.chat.id, text=f'Добро пожаловать, Курьер', reply_markup=menu.kur_menu)

        if dictKunaEvent[message.chat.id] == "sending_code":
            chat_id = message.chat.id
            code = message.text
            dictKunaEvent[message.chat.id] = ""
            check = func.check_kuna_code(code)
            if check[0] == 1:
                func.add_balance(chat_id, check[1])
                bot.send_message(chat_id, 'Вы успешно пополнили баланс на {} USD'.format(check[1]),
                                 reply_markup=menu.main_menu)
                func.write_to_adm(chat_id, check[1])
            else:
                bot.send_message(chat_id, f'⚠️ Оплата не была найдена!', reply_markup=menu.main_menu)

    @bot.callback_query_handler(func=lambda call: True)
    def handler_call(call):
        message_id = call.message.message_id
        chat_id = call.message.chat.id

        if call.data == 'profile':
            user = func.get_user(chat_id)
            pokupki = 'Корзина пуста...'
            if len(db.get_values('*', 'user_id', chat_id, base='purchases')) > 0:
                pokupki = '\n'
                for i in db.get_values('*', 'user_id', chat_id, base='purchases'):
                    pokupki = pokupki + i[1][:19] + ' - ' + i[2] + '\n'
            try:
                if func.is_adm(chat_id):
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"""
                🤵<b>Логин:</b> @{user[1]}\n<b>⏳Дата регистрации:</b> {user[2][:19]}\n<b>💰Ваш баланс</b> = {float(user[5]):.2f} {db.get_value('money_value')}
                \n<b>👜Ваши покупки:</b> {pokupki}""", reply_markup=menu.adm_main_menu, parse_mode='HTML')
                elif func.is_kur(chat_id):
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"""
                🤵<b>Логин:</b> @{user[1]}\n<b>⏳Дата регистрации:</b> {user[2][:19]}\n<b>💰Ваш баланс</b> = {float(user[5]):.2f} {db.get_value('money_value')}
                \n<b>👜Ваши покупки:</b> {pokupki}""", reply_markup=menu.kur_main_menu, parse_mode='HTML')
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"""
                🤵<b>Логин:</b> @{user[1]}\n<b>⏳Дата регистрации:</b> {user[2][:19]}\n<b>💰Ваш баланс</b> = {float(user[5]):.2f} {db.get_value('money_value')}
                \n<b>👜Ваши покупки:</b> {pokupki}""", reply_markup=menu.main_menu, parse_mode='HTML')

            except Exception as e:
                print(e)
        if call.data == 'info':
            try:
                if func.is_adm(chat_id):
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=db.get_value('info_message'),
                                          reply_markup=menu.adm_main_menu)
                elif func.is_kur(chat_id):
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=db.get_value('info_message'),
                                          reply_markup=menu.kur_main_menu)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=db.get_value('info_message'),
                                          reply_markup=menu.main_menu)
            except:
                pass
        if call.data == 'stat':
            user = func.get_user(chat_id)
            now = datetime.datetime.now()
            month_count = db.get_valuedata(
                "select count(*) from purchases where date like '" + now.strftime("%Y-%m") + "%'")
            day_count = db.get_valuedata(
                "select count(*) from purchases where date like '" + now.strftime("%Y-%m-%d") + "%'")
            week_count = db.get_valuedata(db.getLastWeekCount())
            user_count = db.get_value(text='count(*)', base='users')
            kur_count = db.get_value(text='count(*)', base='kur_id')
            adm_count = db.get_value(text='count(*)', base='adm_id')
            sell_count = db.get_value(text='count(*)', base='purchases')
            adress_count = db.get_value(text='count(*)', base='address')
            oplata_count = db.get_value(text='count(*)', base='check_id')
            activcat_count = db.get_value(text='count(*)', base='catalog')
            try:
                if func.is_adm(chat_id):
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"""
                		\n\n➖➖➖➖🟢<b>Статистика магазина</b>🟢➖➖➖➖
                		\n➖🤵<b>Пользователей в боте =</b> {user_count}\
                		\n➖<b>⭕️Администраторов =</b> {adm_count}\
                		\n➖<b>📭Курьеров =</b> {kur_count}\
                		\n\n➖➖➖➖🟢<b>Бухгалтерия</b>🟢➖➖➖➖
                		\n➖<b>🎁Товара в наличии =</b> {adress_count}\
                		\n➖<b>✅Всего продаж =</b> {sell_count}\
                		\n➖<b>✅Продажи за день =</b> {day_count}\
                		\n➖<b>✅Продажи за неделю =</b> {week_count}\
                		\n➖<b>✅Продажи за месяц =</b> {month_count}\
                		\n➖<b>💵Всего пополнений</b> = {oplata_count}\
                		\n➖➖➖➖➖➖➖➖➖➖
                		\n➖<b>✅Активных категорий =</b> {activcat_count}\
                		\n➖➖➖➖➖➖➖➖➖➖""", reply_markup=menu.adm_main_menu, parse_mode='HTML')
                elif func.is_kur(chat_id):
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"""
                		\n\n➖➖➖➖🟢<b>Статистика магазина</b>🟢➖➖➖➖
                		\n➖🤵<b>Пользователей в боте =</b> {user_count}\
                		\n➖<b>⭕️Администраторов =</b> {adm_count}\
                		\n➖<b>📭Курьеров =</b> {kur_count}\
                		\n➖➖➖➖➖➖➖➖➖➖
                		\n➖<b>🎁Товара в наличии =</b> {adress_count}\
                		\n➖<b>✅Активных категорий =</b> {activcat_count}\
                		\n➖➖➖➖➖➖➖➖➖➖""", reply_markup=menu.kur_main_menu, parse_mode='HTML')
            except:
                pass

        if call.data == 'nal':
            user = func.get_user(chat_id)
            now = datetime.datetime.now()
            try:
                tovari = db.get_values_long(
                    "select p.name, count(a.product_id), p.product_id from address as a inner join product as p where a.product_id = p.product_id group by a.product_id")
                tvrstr = ""

                for tovar, kolichestvo, product_id in tovari:
                    tvrstr += f"{tovar} = {kolichestvo}\n"
                    nalichie = db.get_values_long(
                        f"select link, count(product_id) from address where product_id = {product_id} group by link")

                    for n, k in nalichie:
                        tvrstr += f"📗 {n} ({k})\n"

                    tvrstr += "\n"

                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                 text=f"📒 <b>Товар в наличии:</b>\n\n<b>{tvrstr}</b>",
                                 reply_markup=menu.adm_main_menu, parse_mode='HTML')
            except:
                pass


        if call.data == 'naluser':
            try:
                    tovari = db.get_values_long(
                        "select p.name, count(a.product_id) from address as a inner join product as p where a.product_id = p.product_id group by a.product_id")
                    tvrstr = ""

                    for tovar, kolichestvo in tovari:
                        tvrstr += f"📗 {tovar} = {kolichestvo}\n"

                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                     text=f"📒 <b>Товар в наличии:</b>\n\n<b>{tvrstr}</b>",
                                     reply_markup=menu.main_menu, parse_mode='HTML')
            except:
                pass


        if call.data == 'nalkur':
            try:
                    tovari = db.get_values_long(
                        "select p.name, count(a.product_id) from address as a inner join product as p where a.product_id = p.product_id group by a.product_id")
                    tvrstr = ""

                    for tovar, kolichestvo in tovari:
                        tvrstr += f"📗 {tovar} = {kolichestvo}\n"

                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                     text=f"📒 <b>Товар в наличии:</b>\n\n<b>{tvrstr}</b>",
                                     reply_markup=menu.kur_main_menu, parse_mode='HTML')
            except:
                pass
        if call.data == 'balance':
            if db.get_value('need_qiwi') == 1 or db.get_value('need_easypay') == 1 or db.get_value(
                    'need_global24') == 1 or db.get_value('need_promo') == 1:
                try:
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='💲 Выберите способ пополнения: ',
                                          reply_markup=menu.replenish_balance())
                except:
                    pass
            else:
                try:
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='Администрация не добавила способов пополнения баланса...',
                                          reply_markup=menu.adm_main_menu if func.is_adm(chat_id) else menu.main_menu)
                except:
                    pass
        if call.data == 'exit_to_menu':
            bot.clear_step_handler(call.message)

            if func.is_adm(chat_id):
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text='Рад приветствовать тебя дружище в БОТе от ✅ Your Dealer ✅\nЯ работаю 24/7, чтобы ТЫ имел возможность приобрести наш товар в любое время суток 😉\n\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n🔮 Для покупки товара сначала нужно 💰Пополнить баланс💰\n📌 Перед пополнением проверь наличие товара, выбрав количество (0.5г или 1г), в случае если товара не будет, но деньги будут положены на баланс БОТа, придется ждать пополнения готовыми кладами📌\n⛔️Вывод средств - недоступен⛔️\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n\n📱И немного полезных ссылок нашего магазина 📱\n🥳 Отзывы - @your_dealer_reviews 🥳\n📰 Новости - @your_dealer_news 📰\n❗️Если возникнут проблемы, обращайся к оператору❗️', reply_markup=menu.adm_main_menu,
                                      parse_mode='HTML')
            elif func.is_kur(chat_id):
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text='Рад приветствовать тебя дружище в БОТе от ✅ Your Dealer ✅\nЯ работаю 24/7, чтобы ТЫ имел возможность приобрести наш товар в любое время суток 😉\n\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n🔮 Для покупки товара сначала нужно 💰Пополнить баланс💰\n📌 Перед пополнением проверь наличие товара, выбрав количество (0.5г или 1г), в случае если товара не будет, но деньги будут положены на баланс БОТа, придется ждать пополнения готовыми кладами📌\n⛔️Вывод средств - недоступен⛔️\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n\n📱И немного полезных ссылок нашего магазина 📱\n🥳 Отзывы - @your_dealer_reviews 🥳\n📰 Новости - @your_dealer_news 📰\n❗️Если возникнут проблемы, обращайся к оператору❗️', reply_markup=menu.kur_main_menu,
                                      parse_mode='HTML')
            else:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text='Рад приветствовать тебя дружище в БОТе от ✅ Your Dealer ✅\nЯ работаю 24/7, чтобы ТЫ имел возможность приобрести наш товар в любое время суток 😉\n\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n🔮 Для покупки товара сначала нужно 💰Пополнить баланс💰\n📌 Перед пополнением проверь наличие товара, выбрав количество (0.5г или 1г), в случае если товара не будет, но деньги будут положены на баланс БОТа, придется ждать пополнения готовыми кладами📌\n⛔️Вывод средств - недоступен⛔️\n‼️‼️‼️ ВАЖНО, ПРИМИ  ВО ВНИМАНИЕ ‼️‼️‼️\n\n📱И немного полезных ссылок нашего магазина 📱\n🥳 Отзывы - @your_dealer_reviews 🥳\n📰 Новости - @your_dealer_news 📰\n❗️Если возникнут проблемы, обращайся к оператору❗️', reply_markup=menu.main_menu,
                                      parse_mode='HTML')

        if call.data == 'qiwi_money':
            try:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=func.qiwi_money(chat_id),
                                      reply_markup=menu.qiwi_money)
            except:
                pass

        if call.data == 'kuna_code':
            try:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=func.kuna_code(chat_id),
                                      reply_markup=menu.kuna_code)
                dictKunaEvent[chat_id] = "sending_code"
            except:
                pass

        if call.data == 'aperon_code':
            wallet = func.aperon_code(chat_id)
            try:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=func.aperon_code(chat_id),
                                      reply_markup=menu.aperon_code)
            except:
                pass

        if call.data == 'check_aperon_money':
            check = func.check_aperon_money(chat_id)

            if check[0] == 1:
                func.add_balance(chat_id, check[1])
                func.print_good_payment(message_id, chat_id, call.id, check[1])
                func.write_to_adm(chat_id, check[1])
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=f'⚠️ Оплата не была найдена!',
                                          show_alert=True)

        if call.data == 'check_qiwi_money':
            check = func.check_qiwi_money(chat_id)

            if check[0] == 1:
                func.add_balance(chat_id, check[1])
                func.print_good_payment(message_id, chat_id, call.id, check[1])
                func.write_to_adm(chat_id, check[1])
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=f'⚠️ Оплата не была найдена!',
                                          show_alert=True)

        if call.data == 'easypay_money':
            try:
                msg = db.get_value('easypay_text').format(
                    number=random.choice(db.get_values('value', base='easypay')[0]))
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=msg,
                                      reply_markup=menu.adm_main_menu if func.is_adm(chat_id) else menu.main_menu)

                msg2 = bot.send_message(chat_id=chat_id,
                                        text="После успешного перевода средств на кошелек\nВведите  ID транзакции и сумму платежа  'Через пробел'\nПример:   ( 892413078 1 )",
                                        reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg2, func.easypay_first)
            except:
                pass

        if call.data == 'global24_money':
            try:
                msg = db.get_value('global24_text').format(
                    number=random.choice(db.get_values('value', base='global24')[0]))
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=msg,
                                      reply_markup=menu.adm_main_menu if func.is_adm(chat_id) else menu.main_menu)

                msg2 = bot.send_message(chat_id=chat_id,
                                        text="После успешного перевода средств на кошелек\nВведите  ID транзакции и сумму платежа  'Через пробел'\nПример:   ( 892413078 1 )",
                                        reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg2, func.global24_first)
            except Exception as e:
                print(e)

        if call.data == 'easypay_check':
            check = func.easypay_check(chat_id)
            if check[0] == 1:
                func.print_good_payment(message_id, chat_id, call.id, check[1])
                func.write_to_adm(chat_id, check[1])
                func.add_balance(chat_id, check[1])
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=f'⚠️ Оплата не была найдена!',
                                          show_alert=True)
        if call.data == 'global24_check':
            check = func.global24_check(chat_id)
            if check[0] == 1:
                func.print_good_payment(message_id, chat_id, call.id, check[1])
                func.write_to_adm(chat_id, check[1])
                func.add_balance(chat_id, check[1])
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=f'⚠️ Оплата не была найдена!',
                                          show_alert=True)

        if call.data == 'promo':
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='💎 Активация ваучера',
                                      reply_markup=menu.adm_main_menu if func.is_adm(chat_id) else menu.main_menu)
                msg = bot.send_message(chat_id, text='💎 Введите ваучер:', reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.promo)
            except:
                pass

        if call.data == 'ref_system':
            ref_code = db.get_value('ref_code', 'user_id', chat_id, 'users')
            if str(ref_code) == str(chat_id):
                keyboard = menu.ref_system_standart
            else:
                keyboard = menu.ref_system
            try:
                msg = f"""📈Реферальная система:
                        \n<i>❔Если человек, присоединившийся к боту по вашей ссылке , пополнит баланс, то вы получите:</i><b> {db.get_value('referral_percent')}%</b>
                        \n<i>💲Ваш доход с реферальной системы составляет:</i> <b>{db.get_value('ref_earn', 'user_id', chat_id, 'users')} {db.get_value('money_value')}</b>\n\n📋Ваша реферальная ссылка: <b><a>https://t.me/{db.get_value('BOT_URL')}?start={db.get_value('ref_code', 'user_id', chat_id, 'users')}</a></b>"""
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=msg, reply_markup=keyboard,
                                      parse_mode='HTML')
            except:
                pass

        if call.data == 'change_ref_code':
            msg = bot.send_message(chat_id, text='✏ Какую ссылку вы хотите иметь? ', reply_markup=menu.cansel_button)
            bot.register_next_step_handler(msg, func.change_ref_code)

        if call.data == 'drop_ref_code':
            try:
                code = db.get_value('ref_code', 'user_id', chat_id, 'users')
                db.set_ref_code(chat_id, code)
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text='🟢🔄 <b>Восстановлена стандартная реферальная ссылка</b> 🔄🟢',
                                      reply_markup=menu.adm_main_menu if func.is_adm(chat_id) else menu.main_menu,
                                      parse_mode='HTML')
            except:
                pass

        if call.data == 'faq':
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text='🟢⁉️ <b>Посмотрите инструкцию пополнения, для определенного метода</b> ⁉️🟢',
                                      reply_markup=menu.faq, parse_mode='HTML')
            except:
                pass

        if call.data == 'help_easypay':
            try:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text='📒 Инструкция по пополнению баланса EasyPay\n1️⃣  Нажмите Пополнить баланс\n2️⃣  Перевeдите через терминал нужную вам сумму на выданный кошелек\n3️⃣  Нажмите Я оплатил\n4️⃣  Введите данные, как на скрине!\nhttps://ibb.co/Hd4pR9m',
                    reply_markup=menu.adm_main_menu if func.is_adm(chat_id) else menu.main_menu
                )
            except:
                pass

        if call.data == 'help_global24':
            try:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text='📒 Инструкция по пополнению баланса Global24 через терминал City24\n1️⃣  Нажмите Пополнить баланс\n2️⃣  Переводите через терминал нужную вам сумму на выданный кошелек\n3️⃣  Нажмите Я оплатил\n4️⃣  Введите данные, как на скрине!\nhttps://ibb.co/ChQKKYT',
                    reply_markup=menu.adm_main_menu if func.is_adm(chat_id) else menu.main_menu
                )
            except:
                pass

        if call.data == 'shop':
            keyboard1 = types.InlineKeyboardMarkup(row_width=1)
            parent_catalog = db.get_values('*', 'catalog_id', 'parent_catalog_id', 'catalog')
            if len(parent_catalog) == 1:
                id = parent_catalog[0][0]
                catalog = db.get_values_long(
                    f'select * from catalog where parent_catalog_id={id} and catalog_id not in (select catalog_id from catalog where parent_catalog_id=catalog_id)')
                for i in catalog:
                    back = 'catalog' + str(i[0])
                    keyboard1.add(types.InlineKeyboardButton(text=i[1], callback_data=back))
            else:
                for i in parent_catalog:
                    back = "parent" + str(i[0])
                    keyboard1.add(types.InlineKeyboardButton(text=i[1], callback_data=back))
            try:
                keyboard1.add(types.InlineKeyboardButton(text='↩️ Назад в меню', callback_data='exit_to_menu'))
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='🏙 Выбери доступный район 🏙',
                                      reply_markup=keyboard1)
            except Exception as e:
                print(e)

        if call.data in func.parent_list():
            print(call.data)
            id = call.data.replace('parent', '')
            keyboard2 = types.InlineKeyboardMarkup(row_width=1)
            catalog = db.get_values_long(
                f'select * from catalog where parent_catalog_id={id} and catalog_id not in (select catalog_id from catalog where catalog_id=parent_catalog_id)')

            for i in catalog:
                back = 'catalog' + str(i[0])
                keyboard2.add(types.InlineKeyboardButton(text=i[1], callback_data=back))
            try:
                keyboard2.add(types.InlineKeyboardButton(text='В меню', callback_data='exit_to_menu'))
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='🏡 Выбирай район из доступных',
                                      reply_markup=keyboard2)
            except Exception as e:
                print(e)

        if call.data in func.catalog_list():
            name = call.data.replace('catalog', '')

            keyboard3 = types.InlineKeyboardMarkup(row_width=1)
            id = db.get_value('catalog_id', 'catalog_id', name, 'catalog')
            catalog = db.get_values_long(f'select * from catalog where parent_catalog_id={id}')
            if len(catalog) == 0:
                product = db.get_values('*', 'catalog_id', id, 'product')
                if len(product) > 0:
                    for i in product:
                        back = 'product_' + str(i[0]) + '_' + str(i[1])
                        keyboard3.add(types.InlineKeyboardButton(text=i[2], callback_data=back))
            else:

                for i in catalog:
                    back = 'catalog' + str(i[0])
                    keyboard3.add(types.InlineKeyboardButton(text=i[1], callback_data=back))
                product = db.get_values('*', 'catalog_id', id, 'product')
                if len(product) > 0:
                    for i in product:
                        back = 'product_' + str(i[0]) + '_' + str(i[1])
                        keyboard3.add(types.InlineKeyboardButton(text=i[2], callback_data=back))
            try:
                keyboard3.add(types.InlineKeyboardButton(text='В меню', callback_data='exit_to_menu'))
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='🧐 Что сегодня будем брать? 🧐 \n📍Ниже на карте обведена зона с готовыми кладами😉\nМы не делаем кладов в джунглях за терминалом, новусом и т.п. 🏃 Все клады в пешей доступности! 🏃\n\nhttps://ibb.co/Z2pkTqt',
                                      reply_markup=keyboard3)
            except Exception as e:
                print(e)

        if call.data in func.product_list():
            name = call.data.replace('product_', '')
            name = name.split('_')
            product = \
                db.get_values_long(
                    f'select * from product where product_id={int(name[0])} and catalog_id={int(name[1])}')[
                    0]
            count = len(db.get_values_long(f'select * from address where product_id={product[0]}'))
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='💰 Купить', callback_data='buy' + call.data),
                         types.InlineKeyboardButton(text='↩️ В меню', callback_data='exit_to_menu'))
            if count > 0:
                text = f'➡️ Название: {product[2]}\n{product[3]}\n➡️ Стоимость: {product[4]} {db.get_value("money_value", base="config")}'
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Товара нет в наличии!', show_alert=True)
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)
            except:
                pass

        if call.data in func.buy_product_list():
            product = func.BuyProduct(chat_id)
            product.product_id = call.data.replace('buyproduct_', '').split('_')[0]
            product.catalog_id = call.data.replace('buyproduct_', '').split('_')[1]
            product.count_max = len(db.get_values_long(f'select * from address where product_id={product.product_id}'))
            product.price = db.get_value_long(
                f'select cost from product where catalog_id={product.catalog_id} and product_id={product.product_id}')
            product.name = db.get_value_long(
                f'select name from product where product_id={product.product_id} and catalog_id={product.catalog_id}')
            product_dict[call.message.chat.id] = product
            # msg = bot.send_message(chat_id=chat_id,text=f'Введите кол-во товара(максимум {product.count_max})',reply_markup=menu.cansel_button)
            try:
                call.message.text = '1'
                buy_first(call.message)
                # bot.register_next_step_handler(msg,buy_first)
            except:
                pass

        # ADMIN MENU
        if call.data == 'exit_to_adm_menu':
            if func.is_adm(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                          text='<b>♻️ Вы вернулись в админ меню!</b>', reply_markup=menu.adm_menu,
                                          parse_mode='HTML')
                except Exception as e:
                    print(e)

        if call.data == 'exit_to_kur_menu':
            if func.is_kur(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                          text='<b>♻️ Вы вернулись в меню Курьера!</b>', reply_markup=menu.kur_menu,
                                          parse_mode='HTML')
                except Exception as e:
                    print(e)

        if call.data == 'shop_config':
            if func.is_adm(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='<b>⚙️ Настройка магазина</b>',
                                          reply_markup=menu.shop_config, parse_mode='HTML')
                except:
                    pass

        if call.data == 'shop_config1':
            if func.is_kur(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='<b>⚙️♻️ Настройка магазина</b>',
                                          reply_markup=menu.shop_config1, parse_mode='HTML')
                except:
                    pass

        if call.data == 'users_config':
            if func.is_adm(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                          text='<b>👨‍🦰 Вы перешли к настройке пользователей!</b>',
                                          reply_markup=menu.users_config, parse_mode='HTML')
                except:
                    pass

        if call.data == 'payments_config':
            if func.is_adm(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                          text='<b>💵 Настройки платежных систем</b>',
                                          reply_markup=menu.payments_config, parse_mode='HTML')
                except Exception as e:
                    print(e)

        if call.data == 'top_ref':
            if func.is_adm(call.message.chat.id):
                conn, cursor = db.connect()
                users = list(cursor.execute('select * from users where ref_earn>0 order by ref_earn').fetchall())

                if len(users) == 0:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Нет прибыли с рефералов...',
                                          reply_markup=menu.adm_menu)
                else:
                    text = '<b>Топ рефералов:</b>\n'
                    for i in users:
                        text = text + i[1] + ' (' + str(i[0]) + ') ' + ' - <i>' + i[7] + ' ' + db.get_value(
                            'money_value') + '</i>\n'
                    bot.send_message(chat_id, text, reply_markup=menu.cansel_button, parse_mode='HTML')

        if call.data == 'top_ref':
            if func.is_kur(call.message.chat.id):
                conn, cursor = db.connect()
                users = list(cursor.execute('select * from users where ref_earn>0 order by ref_earn').fetchall())

                if len(users) == 0:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Нет прибыли с рефералов...',
                                          reply_markup=menu.kur_menu)
                else:
                    text = '<b>Топ рефералов:</b>\n'
                    for i in users:
                        text = text + i[1] + ' (' + str(i[0]) + ') ' + ' - <i>' + i[7] + ' ' + db.get_value(
                            'money_value') + '</i>\n'
                    bot.send_message(chat_id, text, reply_markup=menu.cansel_button, parse_mode='HTML')

        if call.data == 'on_off_payments':
            if func.is_adm(call.message.chat.id):

                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                          text='▶Включение\\выключение плат.систем',
                                          reply_markup=menu.on_off_payments())
                except Exception as e:
                    print(e)

        if call.data == 'qiwi_config':
            if func.is_adm(call.message.chat.id):
                db.set_payments_value()
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='▶Включение\\выключение плат.систем',
                                      reply_markup=menu.on_off_payments())

        if call.data == 'easy_config':
            if func.is_adm(call.message.chat.id):
                db.set_payments_value('need_easypay')
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='▶Включение\\выключение плат.систем',
                                      reply_markup=menu.on_off_payments())

        if call.data == 'global_config':
            if func.is_adm(call.message.chat.id):
                db.set_payments_value('need_global24')
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='▶Включение\\выключение плат.систем',
                                      reply_markup=menu.on_off_payments())

        if call.data == 'promo_config':
            if func.is_adm(call.message.chat.id):
                db.set_payments_value('need_promo')
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='▶Включение\\выключение плат.систем',
                                      reply_markup=menu.on_off_payments())

        if call.data == 'add_remove_payments':
            if func.is_adm(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                          text='📎Добавление\\удаление кошельков',
                                          reply_markup=menu.add_remove_payments)
                except:
                    pass

        if call.data == 'add_replenish_number':
            if func.is_adm(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                          text='📎Добавление\\удаление кошельков',
                                          reply_markup=menu.add_replenish_number)
                except:
                    pass

        if call.data == 'add_qiwi':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id, text='➕Введите номер кошелька: ', reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, add_qiwi1)

        if call.data == 'add_easy':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id, text='➕Введите номер кошелька: ', reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.add_easy)

        if call.data == 'add_global':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id, text='➕Введите номер кошелька: ', reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.add_global)

        if call.data == 'remove_replenish_number':
            if func.is_adm(call.message.chat.id):
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='✖Удаление кошельков: ',
                                      reply_markup=menu.remove_replenish_number)

        if call.data == 'remove_qiwi':
            if func.is_adm(call.message.chat.id):
                wallets = db.get_values('number', base='qiwi')
                text = 'Кошельки:\n'
                for i in wallets:
                    text = text + str(i[0]) + '\n'
                text = text + '\n✖Введите номер кошелька, который нужно удалить!'
                msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.remove_qiwi)

        if call.data == 'remove_easy':
            if func.is_adm(call.message.chat.id):
                wallets = db.get_values('value', base='easypay')
                text = 'Кошельки:\n'
                for i in wallets:
                    text = text + str(i[0]) + '\n'
                text = text + '\n\n✖Введите номер кошелька, который нужно удалить!'
                msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.remove_easy)

        if call.data == 'remove_global':
            if func.is_adm(call.message.chat.id):
                wallets = db.get_values('value', base='global24')
                text = 'Кошельки:\n'
                for i in wallets:
                    text = text + str(i[0]) + '\n'
                text = text + '\n\n✖Введите номер кошелька, который нужно удалить!'
                msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.remove_global)

        if call.data == 'cansel_button':
            bot.delete_message(chat_id=chat_id, message_id=message_id)
            bot.clear_step_handler(call.message)

        if call.data == 'add_promo':
            if func.is_adm(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='💎 Добавление промокодов!',
                                          reply_markup=menu.adm_menu)
                    msg = bot.send_message(chat_id=chat_id, text='➕Введите промокод:', reply_markup=menu.cansel_button)
                    bot.register_next_step_handler(msg, func.add_promo1)
                except:
                    pass

        if call.data == 'promo_money':
            if func.is_adm(call.message.chat.id):
                try:
                    msg = bot.send_message(chat_id=chat_id, text='➕Введите сумму ваучера: ',
                                           reply_markup=menu.cansel_button)
                    bot.register_next_step_handler(msg, func.add_promo2)
                except Exception as e:
                    print(e)

        if call.data == 'promo_discount':
            if func.is_adm(call.message.chat.id):
                try:
                    msg = bot.send_message(chat_id=chat_id, text='➕Введите скидку от ваучера(например 13%): ',
                                           reply_markup=menu.cansel_button)
                    bot.register_next_step_handler(msg, func.add_promo_discount)
                except:
                    pass

        if call.data == 'set_discount':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id,
                                       text='➕Введи ID\ссылку пользователя и размер скидки(через пробел): ',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.set_discount1)

        if call.data == 'set_balance':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='➕Введи ID\ссылку пользователя и баланс(через пробел): ',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.set_balance1)

        if call.data == 'add_adm':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='➕Введи ID\ссылку пользователя, кому выдать админку ',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.add_adm)

        if call.data == 'remove_adm':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='➕Введи ID\ссылку пользователя, у кого забрать админку ',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.remove_adm)

        if call.data == 'add_kur':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='➕Введи ID\ссылку пользователя, кому выдать Курьера ',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.add_kur)

        if call.data == 'remove_kur':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='➕Введи ID\ссылку пользователя, у кого забрать Курьера ',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.remove_kur)

        if call.data == 'sending_msg':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='<b>💬 Введите текст рассылки! 💬</b>',
                                       reply_markup=menu.cansel_button, parse_mode='HTML')
                bot.register_next_step_handler(msg, sending_msg1)

        if call.data == 'sending_msg_kur':
            if func.is_kur(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='<b>💬 Введите текст рассылки! 💬</b>',
                                       reply_markup=menu.cansel_button, parse_mode='HTML')
                bot.register_next_step_handler(msg, sending_msg1)

        # Admin_menu shop_settings
        if call.data == 'set_money_value':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id,
                                       text=f'Какую валюту будем устанавливать?\nСейчас у нас - {db.get_value("money_value")}',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.set_money_value)

        if call.data == 'set_info_message':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id,
                                       text=f'Какое описание устанавливать?\nСейчас у нас: \n{db.get_value("info_message")}',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.set_info_message)

        if call.data == 'set_ref_percent':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id,
                                       text=f'Какой процент устанавливать?(только цифры)\nСейчас у нас - {db.get_value("referral_percent")}%',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.set_ref_percent)

        if call.data == 'add_parent_category':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id,
                                       text=f'Введите название категории',
                                       reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.add_parent_category, call, msg.message_id)

        if call.data == 'add_category':
            if func.is_adm(call.message.chat.id):
                parent_categorys = db.get_values_long('select * from catalog where catalog_id=parent_catalog_id')
                print(parent_categorys)
                if len(parent_categorys) > 0:
                    keyboard = types.InlineKeyboardMarkup()
                    for i in parent_categorys:
                        back = '@#!$' + i[1] + '_' + str(i[2])
                        keyboard.add(types.InlineKeyboardButton(text=i[1], callback_data=back))
                    keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit_to_adm_menu'))
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                              text='Выберите старшую категорию, куда добавлять:', reply_markup=keyboard)
                    except:
                        pass
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text=f'Нет ни одной старшей категории!!!',
                                              show_alert=True)
        if call.data in func.list_add_category():
            name = call.data.replace('@#!$', '').split('_')[0]
            id = call.data.replace('@#!$', '').split('_')[1]
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Админ меню',
                                      reply_markup=menu.adm_menu)
            except Exception as e:
                print(e)
            msg = bot.send_message(chat_id=chat_id, text='Введите название категории для добавления:',
                                   reply_markup=menu.cansel_button)
            bot.register_next_step_handler(msg, func.add_category, name, id, call.id, msg.message_id)

        if call.data == 'add_sub_category':
            if func.is_adm(call.message.chat.id):
                limit = 50
                sub_cat_count = db.get_valuedata('select count(*) from catalog where catalog_id!=parent_catalog_id')
                categorys = db.get_values_long(
                    f'select * from catalog where catalog_id!=parent_catalog_id limit {limit}')
                if len(categorys) > 0:
                    keyboard = types.InlineKeyboardMarkup()
                    for i in categorys:
                        back = '@@#@' + i[1] + '_' + str(i[0])
                        parent = db.get_value('name', 'catalog_id', i[2], 'catalog')
                        keyboard.add(types.InlineKeyboardButton(text=i[1] + f'({parent})', callback_data=back))

                    if sub_cat_count > limit:
                        keyboard.add(types.InlineKeyboardButton(
                            text=f'➡️ Следующие {sub_cat_count - limit if sub_cat_count < 101 else limit}',
                            callback_data=f'add_sub_category_{limit}'))
                    keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit_to_adm_menu'))
                    try:

                        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Куда добавляем?',
                                              reply_markup=keyboard)
                    except Exception as ex:
                        print(ex)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text=f'Нет ни одной категории!!!',
                                              show_alert=True)

        if re.search("add_sub_category_\d+", call.data) is not None:
            if func.is_adm(call.message.chat.id):
                offset = int(str(call.data).replace("add_sub_category_", ""))
                limit = offset + 50
                sub_cat_count = db.get_valuedata('select count(*) from catalog where catalog_id!=parent_catalog_id')
                categorys = db.get_values_long(
                    f'select * from catalog where catalog_id!=parent_catalog_id limit 50 offset {offset}')
                if len(categorys) > 0:
                    keyboard = types.InlineKeyboardMarkup()
                    for i in categorys:
                        back = '@@#@' + i[1] + '_' + str(i[0])
                        parent = db.get_value('name', 'catalog_id', i[2], 'catalog')
                        keyboard.add(types.InlineKeyboardButton(text=i[1] + f'({parent})', callback_data=back))

                    if sub_cat_count > limit:
                        keyboard.add(types.InlineKeyboardButton(
                            text=f'➡️ Следующие {sub_cat_count - limit if sub_cat_count <= ((limit // 50) + 1) * 50 else 50}',
                            callback_data=f'add_sub_category_{limit}'))

                    keyboard.add(types.InlineKeyboardButton(
                        text=f'⬅️ Предыдущие 50',
                        callback_data=f'add_sub_category_{offset - 50}' if offset - 50 > 0 else 'add_sub_category'))
                    keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit_to_adm_menu'))
                    try:

                        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Куда добавляем?',
                                              reply_markup=keyboard)
                    except Exception as ex:
                        print(ex)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text=f'Нет ни одной категории!!!',
                                              show_alert=True)

        if call.data in func.list_add_sub_category():
            name = call.data.replace('@@#@', '').split('_')[0]
            id = call.data.replace('@@#@', '').split('_')[1]
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Админ меню',
                                      reply_markup=menu.adm_menu)
            except Exception as e:
                print(e)
            msg = bot.send_message(chat_id=chat_id, text='Введите название подкатегории для добавления:',
                                   reply_markup=menu.cansel_button)
            bot.register_next_step_handler(msg, func.add_category, name, id, call.id, msg.message_id)

        if call.data == 'add_product_to_category':
            if func.is_adm(call.message.chat.id):
                limit = 50
                catergory_count = db.get_valuedata('select count(*) from catalog where catalog_id!=parent_catalog_id')
                catalog = db.get_values_long(f'select * from catalog where catalog_id!=parent_catalog_id limit {limit}')
                if len(catalog) > 0:
                    keyboard = types.InlineKeyboardMarkup()
                    for i in catalog:
                        parent = db.get_value('name', 'catalog_id', i[2], 'catalog')
                        back = '&&@#' + i[1] + '_' + str(i[0])
                        keyboard.add(types.InlineKeyboardButton(text=i[1] + f'({parent})', callback_data=back))

                    if catergory_count > limit:
                        keyboard.add(types.InlineKeyboardButton(
                            text=f'➡️ Следующие {catergory_count - limit if catergory_count < 101 else limit}',
                            callback_data=f'add_product_to_category_{limit}'))

                    keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit_to_adm_menu'))
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Куда добавляем?',
                                              reply_markup=keyboard)
                    except:
                        pass
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text=f'Нет ни одной категории!!!',
                                              show_alert=True)

        if re.search("add_product_to_category_\d+", str(call.data)) is not None:
            if func.is_adm(call.message.chat.id):
                offset = int(str(call.data).replace("add_product_to_category_", ""))
                limit = offset + 50
                catergory_count = db.get_valuedata('select count(*) from catalog where catalog_id!=parent_catalog_id')
                catalog = db.get_values_long(
                    f'select * from catalog where catalog_id!=parent_catalog_id limit 50 offset {offset}')
                if len(catalog) > 0:
                    keyboard = types.InlineKeyboardMarkup()
                    for i in catalog:
                        parent = db.get_value('name', 'catalog_id', i[2], 'catalog')
                        back = '&&@#' + i[1] + '_' + str(i[0])
                        keyboard.add(types.InlineKeyboardButton(text=i[1] + f'({parent})', callback_data=back))

                    if catergory_count > limit:
                        keyboard.add(types.InlineKeyboardButton(
                            text=f'➡️ Следующие {catergory_count - limit if catergory_count <= ((limit // 50) + 1) * 50 else 50}',
                            callback_data=f'add_product_to_category_{limit}'))

                    keyboard.add(types.InlineKeyboardButton(
                        text=f'⬅️ Предыдущие 50',
                        callback_data=f'add_product_to_category_{offset - 50}' if offset - 50 > 0 else 'add_product_to_category'))

                    keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit_to_adm_menu'))
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Куда добавляем?',
                                              reply_markup=keyboard)
                    except:
                        pass
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text=f'Нет ни одной категории!!!',
                                              show_alert=True)

        if call.data in func.list_add_product_to_category():
            id = call.data.replace('&&@#', '').split('_')[1]
            try:
                if func.is_adm(message.chat.id):
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Админ меню',
                                          reply_markup=menu.adm_menu)
                elif func.is_kur(message.chat.id):
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Меню Курьера',
                                          reply_markup=menu.kur_menu)
            except Exception as e:
                print(e)
            msg = bot.send_message(chat_id=chat_id, text='Введите название товара:',
                                   reply_markup=menu.cansel_button)
            bot.register_next_step_handler(msg, add_product_first, id, call.id, msg.message_id)

        if call.data == 'add_product':
            limit = 50
            product_count = db.get_value('count(*)', base='product')
            products = db.get_values_long(f"select * from product limit {limit}")
            if len(products) > 0:
                keyboard = types.InlineKeyboardMarkup()
                for i in products:
                    back = '~~#@' + i[2] + '_' + str(i[0])
                    keyboard.add(types.InlineKeyboardButton(text=i[2], callback_data=back))

                if product_count > limit:
                    keyboard.add(types.InlineKeyboardButton(
                        text=f'➡️ Следующие {product_count - limit if product_count < 101 else limit}',
                        callback_data=f'add_product_{limit}'))

                keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit_to_adm_menu'))
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Куда добавить?',
                                          reply_markup=keyboard)
                except Exception as ex:
                    print(ex)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text=f'Нет ни одного товара!!!',
                                          show_alert=True)

        if re.search("add_product_\d+", str(call.data)) is not None:
            offset = int(str(call.data).replace("add_product_", ""))
            limit = offset + 50
            product_count = db.get_value('count(*)', base='product')
            products = db.get_values_long(f"select * from product limit 50 offset {offset}")
            if len(products) > 0:
                keyboard = types.InlineKeyboardMarkup()
                for i in products:
                    back = '~~#@' + i[2] + '_' + str(i[0])
                    keyboard.add(types.InlineKeyboardButton(text=i[2], callback_data=back))

                if product_count > limit:
                    keyboard.add(types.InlineKeyboardButton(
                        text=f'➡️ Следующие {product_count - limit if product_count <= ((limit // 50) + 1) * 50 else 50}',
                        callback_data=f'add_product_{limit}'))

                keyboard.add(types.InlineKeyboardButton(
                    text=f'⬅️ Предыдущие 50',
                    callback_data=f'add_product_{offset - 50}' if offset - 50 > 0 else 'add_product'))

                keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit_to_adm_menu'))
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Куда добавить?',
                                          reply_markup=keyboard)
                except Exception as ex:
                    print(ex)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text=f'Нет ни одного товара!!!',
                                          show_alert=True)

        if call.data in func.list_of_add_product():
            id = call.data.replace('~~#@', '').split('_')[1]
            msg = bot.send_message(chat_id=chat_id, text='Введите ссылку, которую отправлять при покупке товара (Массовое добавление товаров: вводите каждую ссылку с новой строки):',
                                   reply_markup=menu.cansel_button)
            post = {
                "chat_id": chat_id,
                "token": uuid.uuid1()
            }
            curer.insert_one(post)
            bot.register_next_step_handler(msg, func.add_product, id)

        if call.data == 'add_product_to_category_kur':
            if func.is_kur(call.message.chat.id):
                catalog = db.get_values_long('select * from catalog where catalog_id!=parent_catalog_id')
                if len(catalog) > 0:
                    keyboard = types.InlineKeyboardMarkup()
                    for i in catalog:
                        parent = db.get_value('name', 'catalog_id', i[2], 'catalog')
                        back = '&&@#' + i[1] + '_' + str(i[0])
                        keyboard.add(types.InlineKeyboardButton(text=i[1] + f'({parent})', callback_data=back))
                    keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit_to_kur_menu'))
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Куда добавляем?',
                                              reply_markup=keyboard)
                    except:
                        pass
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text=f'Нет ни одной категории!!!',
                                              show_alert=True)

        if call.data == 'add_product_kur':
            products = db.get_values('*', base='product')
            if len(products) > 0:
                keyboard = types.InlineKeyboardMarkup()
                for i in products:
                    back = '~~#@' + i[2] + '_' + str(i[0])
                    keyboard.add(types.InlineKeyboardButton(text=i[2], callback_data=back))
                keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit_to_kur_menu'))
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Куда добавить?',
                                          reply_markup=keyboard)
                except:
                    pass

    def add_product_first(message, id, call_id, message_id):
        product = func.Add_Product()
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=message_id)
        max = db.get_value_long('select max(product_id) from product')
        if max is None or max == '0':
            max = 0
        max += 1
        product.product_id = int(max)
        product.catalog_id = id
        product.call_id = call_id
        product.name = message.text
        msg = bot.send_message(chat_id=message.chat.id, text='Введите описание к товару:',
                               reply_markup=menu.cansel_button)
        product.message_id = msg.message_id
        bot.register_next_step_handler(msg, add_product_second, product)

    def add_product_first_kur(message, id, call_id, message_id):
        product = func.Add_Product_kur()
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=message_id)
        max = db.get_value_long('select max(product_id) from product')
        if max is None or max == '0':
            max = 0
        max += 1
        product.product_id = int(max)
        product.catalog_id = id
        product.call_id = call_id
        product.name = message.text
        msg = bot.send_message(chat_id=message.chat.id, text='Введите описание к товару:',
                               reply_markup=menu.cansel_button)
        product.message_id = msg.message_id
        bot.register_next_step_handler(msg, add_product_second, product)

    def add_product_second(message, product):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=product.message_id)
        product.descriptions = message.text
        msg = bot.send_message(chat_id=message.chat.id, text='Введите цену:',
                               reply_markup=menu.cansel_button)
        product.message_id = msg.message_id
        bot.register_next_step_handler(msg, add_product_third, product)

    def add_product_second_kur(message, product_kur):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=product.message_id)
        product.descriptions = message.text
        msg = bot.send_message(chat_id=message.chat.id, text='Введите цену:',
                               reply_markup=menu.cansel_button)
        product.message_id = msg.message_id
        bot.register_next_step_handler(msg, add_product_third_kur, product)

    def add_product_third(message, product):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=product.message_id)
        if func.isfloat(message.text):
            product.cost = float(message.text)
            conn, cursor = db.connect()
            cursor.execute('insert into product values(?,?,?,?,?)',
                           (product.product_id, product.catalog_id, product.name, product.descriptions, product.cost,))
            conn.commit()
            #
            try:
                bot.answer_callback_query(callback_query_id=product.call_id, text=f'Добавил товар {product.name}',
                                          show_alert=True)
            except:
                bot.send_message(chat_id=message.chat.id, text=f'Добавил товар: {product.name}',
                                 reply_markup=menu.main_menu)
        else:
            try:
                bot.answer_callback_query(callback_query_id=product.call_id, text=f'Неверная цена продукта!',
                                          show_alert=True)
            except Exception as e:
                print(e)
                bot.send_message(chat_id=message.chat.id, text=f'Неверная цена продукта!',
                                 reply_markup=menu.main_menu)

    def buy_first(message):
        product = product_dict[message.chat.id]
        product.count = int(message.text)
        sum = float(product.price) * int(product.count)
        discount = db.get_value('discount', 'user_id', product.user_id, 'users')
        try:
            if int(message.text) in range(1, int(product.count_max) + 1):
                if func.check_balance(message.chat.id, sum, discount):
                    bought = ''
                    conn, cursor = db.connect()
                    for i in db.get_values_long(
                            f'select link from address where product_id={product.product_id} limit {product.count}'):
                        bought = bought + i[0] + '\n'
                        cursor.execute('insert into purchases values(?,?,?)',
                                       (message.chat.id, datetime.datetime.now(), i[0],))
                        conn.commit()
                    cursor.close()
                    conn.close()
                    func.ref_cur(sum)
                    if func.is_kur(message.chat.id):
                        bot.send_message(chat_id=message.chat.id,
                                         text=f'Вы купили {product.name}\nКол-во: {product.count}\n{bought}',
                                         reply_markup=menu.kur_main_menu)
                    elif func.is_adm(message.chat.id):
                        bot.send_message(chat_id=message.chat.id,
                                         text=f'Вы купили {product.name}\nКол-во: {product.count}\n{bought}',
                                         reply_markup=menu.adm_main_menu)
                    else:
                        bot.send_message(chat_id=message.chat.id,
                                         text=f'Вы купили {product.name}\nКол-во: {product.count}\n{bought}',
                                         reply_markup=menu.main_menu)
                    username = message.chat.username
                    func.remove_balance(message.chat.id, sum, discount)
                    db.remove_product(product.product_id, product.count)
                    adm_id = list(db.get_values('value',base='adm_id'))
                    bot.send_message(chat_id=config.CHAT_GROUP_ID,text=f'❇️ Куплен товар {product.name}\n📕 Кол-во: {product.count}\n📕 Общая стоимость: {sum} {db.get_value("money_value")}\n📕 Товар: {bought}\n📕 Покупатель: @{username}')
                else:
                    bot.send_message(chat_id=message.chat.id,
                                     text='Недостаточно средств, пополни баланс и совершай покупки.',
                                     reply_markup=menu.adm_main_menu if func.is_adm(
                                         message.chat.id) else menu.main_menu)
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text='❌ Неверное кол-во',
                                 reply_markup=menu.adm_main_menu if func.is_adm(message.chat.id) else menu.main_menu)
        except Exception as e:
            print(e)
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Что-то пошло не по плану',
                             reply_markup=menu.adm_main_menu if func.is_adm(message.chat.id) else menu.main_menu)

    class Add_qiwi():
        def __init__(self):
            self.number = None
            self.token = None

    qiwi = Add_qiwi()

    def add_qiwi1(message):
        if func.is_adm(message.chat.id):
            qiwi.number = message.text
            msg = bot.send_message(chat_id=message.chat.id, text='➕Введите токен: ', reply_markup=menu.cansel_button)
            bot.register_next_step_handler(msg, add_qiwi2)

    def add_qiwi2(message):
        if func.is_adm(message.chat.id):
            qiwi.token = message.text
            db.add_replenish('qiwi', qiwi.number, qiwi.token)
            bot.send_message(chat_id=message.chat.id, text='✅Добавил QiwiMoney',
                             reply_markup=menu.add_remove_payments)

    def sending_msg1(message):
        qiwi.number = message.text
        msg = bot.send_message(chat_id=message.chat.id,
                               text=f'Вы хотите разослать:\n"{qiwi.number}"\nЕсли да, то отправьте 010110',
                               reply_markup=menu.cansel_button)
        bot.register_next_step_handler(msg, sending_msg2)

    def sending_msg2(message):
        if message.text == '010110':
            for i in db.get_values('user_id', base='users'):
                try:
                    bot.send_message(chat_id=i[0], text=qiwi.number)
                except:
                    pass
        else:
            if func.is_adm(message.chat.id):
                bot.send_message(chat_id=message.chat.id, text='Ooops.', reply_markup=menu.adm_menu)
            elif func.is_kur(message.chat.id):
                bot.send_message(chat_id=message.chat.id, text='Ooops.', reply_markup=menu.kur_menu)

    def telegram_polling():
        try:
            bot.polling(none_stop=True, timeout=60)  # constantly get messages from Telegram
        except Exception as e:
            print(
                f'\n---------------------------\nВремя ошибки: {datetime.datetime.now()}\n{e}\n-------------------------\n')
            bot.stop_polling()
            time.sleep(10)
            telegram_polling()

    telegram_polling()


start_bot()
