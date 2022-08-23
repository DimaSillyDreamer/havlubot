import telebot
from telebot import types
from config import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def get_hello(message):
    bot.send_message(message.chat.id,
                     f'Здравствуйте, {message.from_user.first_name}! Мы рады, что Вы остановили свой выбор на нашем полотенце. Благодарим Вас за заказ и дарим шанс ВЫИГРАТЬ ХАЛАТ. За подробностями переходите в\n⬇️МЕНЮ')

@bot.message_handler(commands=['question'])
def question(message):
    bot.send_message(message.chat.id,
                     'Если у Вас возникли вопросы по нашему полотенцу, мы всегда с радостью готовы на них ответить здесь⬇️')
    
    @bot.message_handler(content_types=['text'])
    def get_answer(message):
        if message.content_type == 'text' and sum(map(lambda x:1 if x.isdigit() else 0, message.text)) > 9:
            bot.send_message(message.chat.id, 'Спасибо за участие в розыгрыше!')
        else:
            bot.send_message(222758196, f'вопрос от {message.from_user.username}:{message.text}')
            bot.send_message(message.chat.id, 'Скоро Вам ответим!')

@bot.message_handler(commands=['recommendations'])
def get_hello(message):
    bot.send_message(message.chat.id,
                     '<b>РЕКОМЕНДАЦИИ ПО УХОДУ</b>\n⬇️\n1. СТИРАТЬ ПРИ ТЕМПЕРАТУРЕ НЕ ВЫШЕ 30С.\n2. НЕ ИСПОЛЬЗОВАТЬ КОНДИЦИОНЕРЫ ДЛЯ ПОЛОСКАНИЯ. ТКАНЬ ОТ ЭТОГО ХУЖЕ  ВПИТЫВАЕТ ВЛАГУ.\n3. СУШИТЬ ПЕШТЕМАЛЬ ВАЖНО В ДАЛИ ОТ ОТОПИТЕЛЬНЫХ ПРИБОРОВ (ПОЛОТЕНЦЕСУШИТЕЛЯ, БАТАРЕИ) ЭТО ОСТАВИТ ВАШЕ ПОЛОТЕНЦЕ МЯГКИМ И НЕЖНЫМ.',
                     parse_mode='HTML')

@bot.message_handler(commands=['lottery'])
def lottery(message):
    start_keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_1 = types.InlineKeyboardButton(text='УСЛОВИЯ РОЗЫГРЫША', callback_data='ok')
    button_2 = types.InlineKeyboardButton(text='ПРИНЯТЬ УЧАСТИЕ', callback_data='not_ok')
    start_keyboard.add(button_1, button_2)
    bot.send_message(message.chat.id, 'РОЗЫГРЫШ ХАЛАТА', reply_markup=start_keyboard)

@bot.callback_query_handler(func=lambda c: c.data)
def answer_callback(callback):
    if callback.data == 'ok':
        bot.send_message(callback.message.chat.id,
                         text='<b>УСЛОВИЯ РОЗЫГРЫША</b>\nРозыгрыш халата проходит каждое 1 число нового месяца.\nДля участия необходимо:\n1. Оставить положительный отзыв на полотенце на сайте Wildberries.\n\n2. Выслать скриншот своего положительного отзыва.\n\n3. Выслать Ваше имя и телефон для обратной связи.\n\nПобедитель выбирается рандомно автоматическим способом из всего числа участников в розыгрыше за текущий месяц.',
                         parse_mode='HTML')


    elif callback.data == 'not_ok':
        bot.send_message(callback.message.chat.id, text="<b>ПРИНЯТЬ УЧАСТИЕ</b>\n1. Для участия оставьте положительный отзыв о полотенце на сайте Wildberries.\n2. Вышлите скриншот положительного отзыва.\n3. Вышлите Ваше имя и телефон для обратной связи.\n\nСКРИНШОТ Отзыва и телефон\nперекреплять в это окошко⬇️",
                         parse_mode="HTML")

    @bot.message_handler(content_types=['photo'])
    def get_answer(message):
        if message.content_type == 'photo':
            bot.send_photo(222758196, message.photo[0].file_id,
                            f'Отзыв от\nID:{message.from_user.id}\nИмя:{message.from_user.first_name}\nФамилия:{message.from_user.last_name}\nПсевдоним:{message.from_user.username}\ntelefon{message.contact.phone_number}')
            bot.send_message(message.chat.id,
                            f'Отзыв получен, теперь отправьте Ваше имя и номер телефона')
            @bot.message_handler(content_types='text')
            def get_answer(message):
                if sum(map(lambda x:1 if x.isdigit() else 0, message.text)) > 9:       
                    bot.send_message(message.chat.id, 'Спасибо за участие в розыгрыше!')
                else:
                    bot.send_message(222758196, f'вопрос от {message.from_user.username}:{message.text}')
                    bot.send_message(message.chat.id, 'Скоро Вам ответим!')

        else:
            bot.send_message(message.chat.id, 'Отправьте пожалуйста ФОТО')


@bot.message_handler(commands=['website'])
def get_website(message):
    bot.send_message(message.chat.id,
                     f'Жми ссылку:\nhttps://www.wildberries.ru/seller/846359')


bot.polling()
