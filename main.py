import telebot
import botConfig
from datetime import datetime
import time
# from emoji import emojize
# from random import choice
import locale
import calendar
from enum import Enum

locale.setlocale(locale.LC_ALL, "")
bot = telebot.TeleBot(botConfig.TOKEN)
katy_id = botConfig.KATYID
admin_id = botConfig.ADMINID

keyboard_start = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_start.row('/Начать', '/Помощь')

keyboard_signup = telebot.types.InlineKeyboardMarkup()
keyboard_signup.add(telebot.types.InlineKeyboardButton(text='Записаться', callback_data="signup"))

keyboard_back = telebot.types.InlineKeyboardMarkup()
keyboard_back.add(telebot.types.InlineKeyboardButton(text='Вернуться', callback_data="back"))


class Month(Enum):
    JAN = (1, 'января')
    FEB = (2, 'февраля')
    MAR = (3, 'марта')
    APR = (4, 'апреля')
    MAY = (5, 'мая')
    JUN = (6, 'июня')
    JUL = (7, 'июля')
    AUG = (8, 'августа')
    SEP = (9, 'сентября')
    OKT = (10, 'октября')
    NOV = (11, 'ноября')
    DEC = (12, 'декабря')

    def get_number(self, input_param):
        print(self.value[0], self.value[1], self.name, input_param)


# bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot
# bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot  bot

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Приветствую, {user}!\n\n'
        'Для продолжения нажмите «Начать»'.format(user=message.from_user.username),
        reply_markup=keyboard_start)

    print(datetime.now(),
          '// bot started by user', message.from_user.username,
          '( user.id', message.from_user.id,
          ') user.is.bot', message.from_user.is_bot)


@bot.message_handler(commands=['Начать'])
def starting_command(message):
    if message.from_user.id == katy_id or message.from_user.id == admin_id:
        keyboard_signup.add(telebot.types.InlineKeyboardButton(text='Инициализировать', callback_data="month_init"))
        text = ('Привет, {user}!\n'
                'Для возможности записи надо инициальзировать ближайшие два месяца.'
                'Нажми «Инициализировать» и выбери количество месяцев '
                '(1 - текущий, 2 - следующий, 1:2 - сразу оба)'.format(user=message.from_user.username))
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=keyboard_signup)
    else:
        keyboard_signup.add(telebot.types.InlineKeyboardButton(text='Помощь', callback_data="help"))
        text = 'Для выбора даты нажмите «Записаться»'
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=keyboard_signup)


@bot.message_handler(commands=['Помощь'])
def help_command(message):
    if message.from_user.id == admin_id or message.from_user.id == katy_id:
        text = 'Что, не знаешь к кому обратиться чтоль? ;)'
    else:
        text = 'Этот бот поможет Вам записаться на маникюр в любую удобную дату.\n' \
               'Достаточно нажать «Записаться», а затем выбрать дату из ближайших двух месяцев'
    bot.send_message(
        message.chat.id,
        text,
        reply_markup=keyboard_start)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    now = datetime.now()
    days_list_first = load_day_list(now.month)
    first_month_buttons = telebot.types.InlineKeyboardMarkup()
    if len(days_list_first) > 0:
        for i in range(len(days_list_first)):
            split_date = days_list_first[i].split()
            first_month_buttons.add(telebot.types.InlineKeyboardButton(text=days_list_first[i],
                                                                       callback_data="callb_1st_" + split_date[0]))
        first_month_buttons.add(telebot.types.InlineKeyboardButton(text='Следующий месяц',
                                                                   callback_data="next_month"))
        first_month_buttons.add(telebot.types.InlineKeyboardButton(text='Вернуться',
                                                                   callback_data="back_from_month_buttons"))
    else:
        first_month_buttons.add(telebot.types.InlineKeyboardButton(text='Следующий месяц',
                                                                   callback_data="next_month"))
        first_month_buttons.add(telebot.types.InlineKeyboardButton(text='Вернуться',
                                                                   callback_data="back_from_month_buttons"))
    days_list_second = load_day_list(now.month + 1)
    second_month_buttons = telebot.types.InlineKeyboardMarkup()
    for i in range(len(days_list_second)):
        split_date = days_list_second[i].split()
        second_month_buttons.add(telebot.types.InlineKeyboardButton(text=days_list_second[i],
                                                                    callback_data="callb_2nd_" + split_date[0]))
    second_month_buttons.add(telebot.types.InlineKeyboardButton(text='Предыдущий месяц',
                                                                callback_data="prev_month"))
    second_month_buttons.add(telebot.types.InlineKeyboardButton(text='Вернуться',
                                                                callback_data="back_from_month_buttons"))

    if call.data == 'back':
        bot.send_message(
            call.message.chat.id,
            'Какие дальнейшие действия?',
            reply_markup=keyboard_signup)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    elif call.data == 'back_from_month_buttons':
        bot.send_message(
            call.message.chat.id,
            'Может продолжим?',
            reply_markup=keyboard_signup)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    elif call.data == 'help':
        bot.send_message(
            call.message.chat.id,
            'Этот бот поможет записаться на маникюр, просто выберите желаемую дату',
            reply_markup=keyboard_signup)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    elif call.data == 'month_init':
        msg = bot.send_message(
            call.message.chat.id,
            'Выбери параметр инициализации (1 - инициализировать текущий месяц, 2 - следующий, 12 - сразу оба) и '
            'отправь это число боту')
        bot.register_next_step_handler(msg, setup_signup_list)
        bot.send_message(call.message.chat.id, 'Готово!')

    elif call.data == 'signup':
        bot.send_message(
            call.message.chat.id,
            'Выберите желаемую дату',
            reply_markup=first_month_buttons)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    elif call.data == 'next_month':
        bot.send_message(
            call.message.chat.id,
            'Даты следующего месяца, доступные для записи:',
            reply_markup=second_month_buttons)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    elif call.data == 'prev_month':
        if len(days_list_second) > 0:
            bot.send_message(
                call.message.chat.id,
                'Даты текущего месяца, доступные для записи:',
                reply_markup=first_month_buttons)
        else:
            bot.send_message(
                call.message.chat.id,
                'В этом месяце доступных для записи дат не осталось, выбирайте следующий месяц',
                reply_markup=first_month_buttons)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    client = "name:{}___id:{}".format(call.from_user.username,
                                      call.from_user.id)
    callback_text = ["callb_1st_", "callb_2nd_"]
    day_list_variant = [days_list_first, days_list_second]
    for m in range(1):
        for i in range(len(day_list_variant[m])):
            split_date = day_list_variant[m][i].split()
            text = callback_text[m] + split_date[0]
            if call.data == text:
                msg = bot.send_message(call.message.chat.id, day_list_variant[m][i])
                update_file(now.month + m, int(split_date[0]), client)
                time.sleep(0.5)
                bot.send_message(admin_id, 'выбрана дата маникюра: ' + msg.text)
                time.sleep(0.5)
                bot.send_message(call.message.chat.id,
                                 'Вы успешно записаны!\n'
                                 'В скором времени с Вами свяжется администратор для подтверждения даты')
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


# FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS
# FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS  FUNCTIONS

def setup_signup_list(param):
    """
    функция инициализирует месячные расписания в зависимости от param
    :param param: 1-текущий месяц, 2-следующий месяц, 12-оба месяца
    :return: возвращает список дней и название месяца
    """
    now = datetime.now()
    enum_items = [item.value for item in Month]
    # создаётся список из значений перечисления методом перебора циклом for
    year_first_int = int(now.strftime("%Y"))
    month_first_int = now.strftime("%m")
    month_first_str = enum_items[int(month_first_int) - 1][1]
    # month_first_str = list(Month)[int(month_first_int) + 1].value[1]
    # преобразует перечесление в список, берет из этого списка "month_first_int + 1" элемент
    # у элемента получает значение value, так как это кортеж, то выбирает из него нужный элемент
    # пример списка [<Month.JAN: (1, 'января')>, <Month.FEB: (2, 'февраля')>,...]
    # now.strftime("%B") - старый функционал

    if month_first_int.isdigit():
        if month_first_int.find('0') == 0:
            month_first_int.replace("0", "")
        month_first_int = int(month_first_int)
    if month_first_int == 12:
        month_second_int = 1
        year_second_int = year_first_int + 1
    else:
        month_second_int = month_first_int + 1
        year_second_int = year_first_int
    month_second_str = enum_items[month_second_int - 1][1]
    # month_second_str = list(Month)[month_second_int + 1].value[1]
    # (datetime(year_second_int, month_second_int, 1)).strftime("%B") - старый функционал

    if int(param.text) == 1:
        days_list_month_first = make_signup_day_list(year_first_int,
                                                     enum_items[int(month_first_int) - 1][0])
        return days_list_month_first, month_first_str
    elif int(param.text) == 2:
        days_list_month_second = make_signup_day_list(year_second_int,
                                                      enum_items[month_second_int - 1][0])
        return days_list_month_second, month_second_str
    elif int(param.text) == 12:
        days_list_month_first = make_signup_day_list(year_first_int,
                                                     enum_items[int(month_first_int) - 1][0])
        days_list_month_second = make_signup_day_list(year_second_int,
                                                      enum_items[month_second_int - 1][0])
        return days_list_month_first, month_first_str, days_list_month_second, month_second_str
# end setup_signup_list


def make_signup_day_list(year, month):
    """
    функция формирует список дней, доступных клиентам для записи
    :param year: int
    :param month: int
    :return:
    """
    signup_days_list = []
    enum_months = [item for item in Month]  # создание списка из перечисления Month
    days_count_in_month = calendar.monthrange(year, enum_months[month-1].value[0])[1]
    month_str = "{}_{}.{}".format(str(year), enum_months[month-1].value[0], enum_months[month-1].name)

    # создание файла с записью расписания на месяц
    save_file = open("signup/{}.txt".format(month_str), "a")
    # начиная с первого дня и до конца месяца с интервалом в день
    # проходит по циклу и формирует месячное расписание (отсчет с 12.00 каждого дня)
    for d in range(1, days_count_in_month + 1, 1):
        period = datetime(year, enum_months[month-1].value[0], d, 12, 0, 0) - datetime.now()
        # print('period', period)
        if period.total_seconds() > 0:
            signup_days_list.append(d)
            # print('days_list', days_list)
            cur_day = (datetime(year, month, d)).strftime("%A")
            if cur_day == 'Saturday' or cur_day == 'Sunday':
                sign_time = '14:00'
            else:
                sign_time = '18:30'
            try:
                # попытка записи данных в файл
                save_file.write("day {} time {} client {} |\n".format(str(d), sign_time, 'none'))
            except Exception as ex:
                print(datetime.now(), 'save_file write ERROR!!! -', ex)
    save_file.close()
    return signup_days_list
# end make_signup_day_list


def update_file(month, update_day, client):
    """
    функция обновляет данные файла 'расписание на месяц'
    :param month: int
    :param update_day: int
    :param client: str
    :return: none
    """
    # noinspection PyGlobalUndefined
    global string_from_file, day_from_splitted_string
    enum_months = [item for item in Month]  # создание списка из перечисления Month
    now = datetime.now()
    month_str = "{}_{}.{}".format(now.strftime("%Y"), enum_months[month - 1].value[0], enum_months[month - 1].name)
    try:
        with open("signup/{}.txt".format(month_str), "r") as f:
            from_file_list = f.readlines()
            f.close()
        # построковое чтение общего списка
        for cur_string in from_file_list:
            # если строка 'cur_string' содержит текст 'update_day'
            if cur_string.find(str(update_day)) != -1:
                # разбивка строки по пробелам
                splitted_string = cur_string.split()
                day_from_splitted_string = splitted_string[1]
                # если в разбитой строке таже дата, что и выбранная пользователем
                if day_from_splitted_string == str(update_day):
                    # получение индекса текущей строки общего списка
                    index = from_file_list.index(cur_string)
                    # удаление текущей строки из общего списка
                    from_file_list.pop(index)
                    # обновление данных о пользователе
                    cur_string_edited = cur_string.replace('none', client)
                    # вставка обновлённой строки вместо удаленной в общий список
                    from_file_list.insert(index, cur_string_edited)
        # запись обновлённого списка в файл
        try:
            update_file_data = open("signup/{}.txt".format(month_str), "w")
            for i in range(len(from_file_list)):
                update_file_data.write(from_file_list[i])
            update_file_data.close()
        except Exception as ex:
            print('cant overwrite update_file_data | Exception =', ex)
    except Exception as ex:
        print('cant open signup file | Exception =', ex)
# end update_file


def load_day_list(month):
    enum_months = [item for item in Month]  # создание списка из перечисления Month
    now = datetime.now()
    month_str = "{}_{}.{}".format(now.strftime("%Y"), enum_months[month - 1].value[0], enum_months[month - 1].name)
    output_list = []
    output_month = enum_months[month - 1].value[1]
    try:
        with open("signup/{}.txt".format(month_str), "r") as f:
            from_file_list = f.readlines()
            f.close()
            for i in from_file_list:
                if i.find('none') != -1:
                    # разбивка строки по пробелам
                    splitted_string = "{} {}".format(i.split()[1], output_month)
                    output_list.append(splitted_string)
    except Exception as ex:
        print('cant open signup file | Exception =', ex)
    return output_list


if __name__ == '__main__':
    is_running = True

    while is_running:
        bot.polling(none_stop=True)
