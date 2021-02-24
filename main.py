import telebot
import botConfig
from datetime import timedelta, datetime
import time
from emoji import emojize
from random import choice
import locale
import calendar

locale.setlocale(locale.LC_ALL, "")

# telebot.apihelper.proxy = {'PROXY'}
bot = telebot.TeleBot(botConfig.TOKEN)
targetID = 1030381477 #1030381477-Katy   1100544423-Polly
targetIDtest = 683022141
adminID = 683022141

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/Начать', '/Помощь')

keyboard2 = telebot.types.InlineKeyboardMarkup()
keyboard2.add(telebot.types.InlineKeyboardButton(text='Воспользоваться', callback_data = "useIt"))
keyboard2.add(telebot.types.InlineKeyboardButton(text='Помощь', callback_data = "help"))

backButton = telebot.types.InlineKeyboardMarkup()
backButton.add(telebot.types.InlineKeyboardButton(text='Вернуться', callback_data = "back"))

STICKERS = ['CAACAgIAAxkBAAEBuxlf7H3QOn-nJnpRjlNcElhfl8iTswACsgEAAjDUnRHOwb3OvDHg8h4E', 'CAACAgIAAxkBAAEBuxtf7H3jjemyO3PDOjKL4zp7gU8SWQACsAEAAjDUnRGkbRgnBeEJix4E', 'CAACAgIAAxkBAAEBux1f7H3vm88rAAFta5scfWN6i0RVsXIAArUBAAIw1J0RU4pzFgFgbjEeBA']
HNY = ['🎁', '🎊', '🎉', '🎄', '☃', '❄', '🎅']
SMILE = ['😉', '😘', '😍', '😜', '😏', '🍕', '🍰', '🍷', '💅', '💃', '🧩', '📺', '📚', '🛀', '🛌', '👩‍❤️‍👨', '🍾', '👇', '❗']
#         0     1      2     3     4     5      6     7     8     9      10    11    12    13     14    15    16    17    18



# bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot
# bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot


@bot.message_handler(commands=['start'])
def start_command(message):
    smile = emojize(choice(HNY))
    stick = choice(STICKERS)

    newYear = datetime(2021, 1, 1, 0, 0, 1)
    period = newYear - datetime.now()
    # print("{} секунд / {} period".format(period.total_seconds(), period))

    bot.send_sticker(message.chat.id, '{sticker}'.format(sticker = stick))
    time.sleep(0.5)
    if period.total_seconds() > 0:
        bot.send_message(
            message.chat.id, #https://trial-sport.ru/goods/1493666.html
            'Привет, {user}! {smile}\nУже интересно что тебя тут ждёт? {wink}\n\nУзнаешь 1 января 2021 года, а пока рано...'.format(user = message.from_user.username, smile = smile, wink = SMILE[0]))
    else:
        bot.send_message(
            message.chat.id, #https://trial-sport.ru/goods/1493666.html
            'Привет, {user}! {smile}\nУже интересно что тебя тут ждёт? {wink}\n\nДля продолжения нажми «Начать»'.format(user = message.from_user.username, smile = smile, wink = SMILE[0]),
            reply_markup = keyboard1)

    print(datetime.now(), '// bot started by user', message.from_user.username,'( user.id', message.from_user.id,') user.is.bot', message.from_user.is_bot)



@bot.message_handler(commands=['Начать'])
def starting_command(message):
    # fileName = message.from_user.id
    # userFile = open("{fName}.txt".format(fName = fileName), "a")
    if message.from_user.id == targetID or message.from_user.id == targetIDtest:
        text = ('Дорогая Катюшенька! {kiss}\n'
        'С Новым 2021 годом тебя! {hny}\n'
        'А это твой подарок {gift}\n\n {voskl}Твои незабываемые выходные{voskl}\n\n'
        'Как ты их проведешь, решать тебе\nХочешь так {party}  Супер!\n'
        'Так {relax}  Ok!\nЯ со своей стороны приложу максимум усилий, чтобы сделать их идеальными\n\n'
        'Подарок, кстати, действует с вечера ПЯТНИЦЫ по вечер ВОСКРЕСЕНЬЯ.\nА ещё к подарку прилагается:\n'
        '{wine} бутылочка хорошего вина (ты его уже увидела {wink1})\n*{sushi} заказ пиццы и/или суши\n*{youme} свидание со мной\n\n'
        'Про детей не волнуйся, мы все будем вместе под присмотром бабушки\n\n'
        'Люблю тебя очень! {love}\n'
        'Как только ты определишься с датой, сообщи этому боту, ну или сразу мне шепни на ушко {kiss}\n* - исключительно по твоему желанию\n\n'
        'Не понятно? Жми «Помощь».'.format(hny = HNY[2] + HNY[3], gift = HNY[0] + SMILE[17], party = SMILE[7] + SMILE[8] + SMILE[9] + SMILE[3], relax = SMILE[7] + SMILE[13] + SMILE[11] + SMILE[12] + SMILE[10] + SMILE[14] + SMILE[14] + SMILE[14], wine = SMILE[16], sushi = SMILE[5], youme = SMILE[15] + SMILE[4] + SMILE[2], wink1 = SMILE[0], kiss = SMILE[1], love = SMILE[1] + SMILE[2] + SMILE[2], voskl = SMILE[18]))
        bot.send_message(
            message.chat.id,
            text,
            reply_markup = keyboard2)
    else:
        text = ('А ты кто вообще и что тут делаешь?!\n'
        'Это всё не для тебя... сорян')
        bot.send_message(
            message.chat.id,
            text)



@bot.message_handler(commands=['Помощь'])
def help_command(message):
    if message.from_user.id == targetID or message.from_user.id == targetIDtest:
        text = 'Этот бот поможет воспользоваться твоим новогодним подарком, давай быстрей нажимай «Начать»'
    else:
        text = 'Этот бот разработан для другого пользователя'
    bot.send_message(
        message.chat.id,
        text,
        reply_markup = keyboard1)



# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     selectedText = message.text
#     # fileName = message.from_user.id
#
#     if selectedText == 'Воспользоваться!':
#         msg = bot.send_message(message.chat.id, 'Катюш, напиши, когда ты хочешь этим заняться {smile}'.format(smile = SMILE[4]), reply_markup = backButton)
#         bot.register_next_step_handler(msg, dateInput)
#     # elif selectedText == 'Вернуться':
#     #     bot.delete_message(message.chat.id, message.message_id)
#     #     bot.send_message(message.chat.id, 'Ну, что делать будем?', reply_markup = keyboard2)
#     else:
#         bot.send_message(message.chat.id, 'Воспользуйся кнопками с командами боту', reply_markup = keyboard1)



@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    fridayTuple = searchFriday()
    monthButtons1 = telebot.types.InlineKeyboardMarkup()
    if len(fridayTuple[0]) > 0:
        for i in range(len(fridayTuple[0])):
            monthButtons1.add(telebot.types.InlineKeyboardButton(text = str(fridayTuple[0][i]) + ' ' + fridayTuple[1], callback_data = "firstMonth" + str(i)))
            # time.sleep(0.5)
        monthButtons1.add(telebot.types.InlineKeyboardButton(text='Следующий месяц', callback_data = "nextMonth"))
        monthButtons1.add(telebot.types.InlineKeyboardButton(text='Вернуться', callback_data = "backFromMonth"))
    else:
        monthButtons1.add(telebot.types.InlineKeyboardButton(text='Следующий месяц', callback_data = "nextMonth"))
        monthButtons1.add(telebot.types.InlineKeyboardButton(text='Вернуться', callback_data = "backFromMonth"))
    monthButtons2 = telebot.types.InlineKeyboardMarkup()
    for i in range(len(fridayTuple[2])):
        monthButtons2.add(telebot.types.InlineKeyboardButton(text = str(fridayTuple[2][i]) + ' ' + fridayTuple[3], callback_data = "secondMonth" + str(i)))
        # time.sleep(0.5)
    monthButtons2.add(telebot.types.InlineKeyboardButton(text='Предыдущий месяц', callback_data = "prevMonth"))
    monthButtons2.add(telebot.types.InlineKeyboardButton(text='Вернуться', callback_data = "backFromMonth"))

    if call.data == 'back':
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        # call.message.text = ''
        bot.send_message(
            call.message.chat.id,
            'Ну, что делать будем?',
            reply_markup = keyboard2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == 'backFromMonth':
        bot.send_message(
            call.message.chat.id,
            'Продолжим?',
            reply_markup = keyboard2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == 'help':
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        # call.message.text = ''
        bot.send_message(
            call.message.chat.id,
            'Этот бот поможет воспользоваться твоим новогодним подарком',
            reply_markup = keyboard2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == 'useIt':
        bot.send_message(
            call.message.chat.id,
            'Катюш, выбери, когда ты хочешь этим заняться {smile}'.format(smile = SMILE[4]),
            reply_markup = monthButtons1)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == 'nextMonth':
        bot.send_message(
            call.message.chat.id,
            'А это список пятниц следующего месяца:',
            reply_markup = monthButtons2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == 'prevMonth':
        if len(fridayTuple[0]) > 0:
            bot.send_message(
                call.message.chat.id,
                'Вот список пятниц этого месяца:',
                reply_markup = monthButtons1)
        else:
            bot.send_message(
                call.message.chat.id,
                'В этом месяце пятниц не осталось, выбирай следующий месяц',
                reply_markup = monthButtons1)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    # elif call.data == 'firstMonth0':
    #     bot.clear_step_handler_by_chat_id(chat_id = call.message.chat.id)
    #     msg = bot.send_message(call.message.chat.id, str(fridayTuple[0][0]) + ' ' + fridayTuple[1])
    #     time.sleep(1)
    #     bot.send_message(683022141, 'выбрана дата: ' + msg.text)
    #     time.sleep(0.5)
    #     bot.send_message(call.message.chat.id, 'Ну всё, готово!\nОжидайте, с вами скоро свяжутся ;)')
    #     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    for i in range(len(fridayTuple[0])):
        text = "firstMonth" + str(i)
        # print('text', text)
        if call.data == text:
            # bot.clear_step_handler_by_chat_id(chat_id = call.message.chat.id)
            msg = bot.send_message(call.message.chat.id, str(fridayTuple[0][i]) + ' ' + fridayTuple[1])
            time.sleep(0.5)
            bot.send_message(adminID, 'выбрана дата: ' + msg.text)
            time.sleep(0.5)
            bot.send_message(call.message.chat.id, 'Ну всё, готово!\nОжидайте, с вами скоро свяжутся ;)')
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    for i in range(len(fridayTuple[2])):
        text = "secondMonth" + str(i)
        # print('text', text)
        if call.data == "secondMonth" + str(i):
            # bot.clear_step_handler_by_chat_id(chat_id = call.message.chat.id)
            msg = bot.send_message(call.message.chat.id, str(fridayTuple[2][i]) + ' ' + fridayTuple[3])
            time.sleep(0.5)
            bot.send_message(adminID, 'выбрана дата: ' + msg.text)
            time.sleep(0.5)
            bot.send_message(call.message.chat.id, 'Ну всё, готово!\nОжидайте, с вами скоро свяжутся ;)')
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)







# FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS
# FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS

# def dateInputFunc(message):
#     dateInput = message.text
#     print('dateInput', dateInput)
#     if len(dateInput) < 15:
#         bot.send_message(message.chat.id, 'Отлично!\nСейчас кое-кому отправлю...' + dateInput)
#         time.sleep(1)
#         now = datetime.now()
#         bot.send_message(683022141, '@ alex:' + now.strftime("%d %B %Y (%A)"))
#         time.sleep(1)
#         bot.send_message(message.chat.id, 'Ну всё, готово!')
#         print('Ну всё, готово!')
#     else:
#         bot.delete_message(message.chat.id, message.message_id)
#         bot.send_message(message.chat.id, 'Попробуй еще раз, что-то пошло не так...', reply_markup = keyboard2)
# end dateInput



def searchFriday():
    now = datetime.now()
    yearFirstInt = int(now.strftime("%Y"))
    monthFirst = now.strftime("%m")
    monthFirstStr = now.strftime("%B")
    # fridayMonthFirst = []
    # fridayMonthSecond = []

    if monthFirst.isdigit():
        if monthFirst.find('0') == 0:
            monthFirst.replace("0", "")
        monthFirstInt = int(monthFirst)
    if monthFirstInt == 12:
        monthSecondInt = 1
        yearSecondInt = yearFirstInt + 1
    else:
        monthSecondInt = monthFirstInt + 1
        yearSecondInt = yearFirstInt
    monthSecondStr = (datetime(yearSecondInt, monthSecondInt, 1)).strftime("%B")

    fridayMonthFirst = calcDays(yearFirstInt, monthFirstInt)
    fridayMonthSecond = calcDays(yearSecondInt, monthSecondInt)

    # print(fridayMonthFirst, fridayMonthSecond)
    return fridayMonthFirst, monthFirstStr, fridayMonthSecond, monthSecondStr
# end searchFriday



def calcDays(year, month):
    searchDay = 0
    days = []
    dayCount = calendar.monthrange(year, month)[1]

    for i in range(1, 7):
        currentDate = datetime(year, month, i)
        # print(currentDate)
        if (currentDate.strftime("%A")).lower() == 'пятница':
            searchDay = i
            break

    for d in range(searchDay, dayCount, 7):
        period = datetime(year, month, d, 19, 00, 00) - datetime.now()
        if ((datetime(year, month, d)).strftime("%A")).lower() == 'пятница':
            if period.total_seconds() > 0:
                days.append(d)
    return days
# end calcDays



while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(datetime.now(), 'ERROR!!! -', e)
        # повторяем через 15 секунд в случае недоступности сервера Telegram
        time.sleep(15)
