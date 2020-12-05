from keyboards import *

def auth(bot, update):
    ulist = users_list()
    user_name = None
    phone_number = bot.message.contact.phone_number[1:]
    if phone_number[0] != '7':
        phone_number = '7' + phone_number
    for row in ulist:
        if row[1] == phone_number:
            user_name = row[0]
            push_phone(row[0], bot.message.chat.id)
    if user_name != None:
        start_menu(bot, update)
    else:
        bot.message.reply_text('Номер телефона не найден, обратитесь к руководителю.', reply_markup=auth_keyboard())


def start_menu(bot, update):
    user_list = users_list()
    user_name = None
    for row in user_list:
        if row[2] == bot.message.chat.id:
            user_name = row[0]
            user_phone = row[1]
            user_role = row[3]
            user_area = row[4]
            user_com1 = row[5]
            user_com2 = row[6]
            user_com3 = row[7]
            user_com4 = row[8]
    set_command(1, "Начало", bot.message.chat.id)
    set_command(2, '', bot.message.chat.id)
    set_command(3, '', bot.message.chat.id)
    set_command(4, '', bot.message.chat.id)
    if user_name == None:
        bot.message.reply_text(f'Необходимо пройти авторизацию', reply_markup=auth_keyboard())
    else:
        bot.message.reply_text(f'Привет {user_name}, роль - {user_role}, телефон {user_phone}, ГКС {user_area}',
                               reply_markup=start_keyboard(user_role))


def take_equip_si(bot, update, area):
    bot.message.reply_text('Выберите получателя', reply_markup=make_si_keyboard(area))


def big_handler(bot, update):
    row = find_user_by_id(str(bot.message.chat.id))
    user_name = row[0]
    user_phone = row[1]
    user_role = row[3]
    user_area = row[4]
    user_com1 = row[5]
    user_com2 = row[6]
    user_com3 = row[7]
    user_com4 = row[8]
    # Прилетело "Внести АО"
    if (user_com1 == "Начало") \
            and (bot.message.text == "Внести АО на склад"):
        bot.message.reply_text('Выберите тип оборудования', reply_markup=types_keyboard())
        set_command(1, "Внести АО на склад", bot.message.chat.id)
    # Прилетел существующий тип АО
    if (user_com1 == "Внести АО на склад") \
            and (find_type(bot.message.text) == 'Yes') \
            and (user_com2 == '') \
            and (user_role == 'РГ' or user_role == "ВИ"):
        set_command(2, bot.message.text, bot.message.chat.id)
        bot.message.reply_text('Введите серийные номера в поле ввода \nНажмите "Сменить тип" для внесения '
                               'оборудования другого типа \nНажмите "Закончить" после ввода',
                               reply_markup=end_change_type_keyboard())
    # Прилетел серийник при внесении на склад
    if (user_com1 == "Внести АО на склад") \
            and (find_type(user_com2) == "Yes") \
            and (user_role == 'РГ' or user_role == 'ВИ') \
            and bot.message.text != "Закончить" \
            and bot.message.text != "Сменить тип":
        add_sn(user_com2, to_eng_and_up(bot.message.text), user_area)
        bot.message.reply_text(f'Оборудование с серийным номером {to_eng_and_up(bot.message.text)} '
                               f'внесено на склад. Введите ещё серийник или нажмите "Закончить"')
    # Прилетело "Сменить тип"
    if (user_com1 == "Внести АО на склад") \
            and (find_type(user_com2) == "Yes") \
            and (user_role == 'РГ' or user_role == 'ВИ') \
            and bot.message.text == "Сменить тип":
        set_command(2, '', bot.message.chat.id)
        bot.message.reply_text('Выберите тип оборудования', reply_markup=types_keyboard())
        set_command(1, "Внести АО на склад", bot.message.chat.id)
    # Прилетело "Выдать АО"
    if (user_com1 == "Начало") \
            and (user_role == 'РГ' or user_role == 'ВИ') \
            and bot.message.text == "Выдать АО":
        set_command(1, "Выдать АО", bot.message.chat.id)
        take_equip_si(bot, update, user_area)
    # Прилетело реально ФИО СИ
    if (user_com1 == "Выдать АО") \
            and (user_role == 'РГ' or user_role == 'ВИ') \
            and (find_si(bot.message.text) == 'Yes') \
            and (user_com2 == ''):
        set_command(2, bot.message.text, bot.message.chat.id)
        bot.message.reply_text(get_si_remains(user_area, bot.message.text), reply_markup=end_change_si_keyboard())
    # Прилетело "Внести АО"
    if (user_com1 == "Выдать АО") \
            and (user_role == 'РГ' or user_role == 'ВИ') \
            and (find_si(user_com2) == 'Yes') \
            and (bot.message.text == 'Сменить получателя'):
        set_command(2, '', bot.message.chat.id)
        take_equip_si(bot, update, user_area)
    # Прилетел серийник при выдаче СИ
    if (user_com1 == "Выдать АО") \
            and (user_role == 'РГ' or user_role == 'ВИ') \
            and (find_si(user_com2) == 'Yes') \
            and (find_si(bot.message.text) != 'Yes') \
            and bot.message.text != 'Закончить' \
            and bot.message.text != 'Сменить получателя':
        set_command(3, to_eng_and_up(bot.message.text), bot.message.chat.id)
        take_to_si(user_area, user_com2, to_eng_and_up(bot.message.text), bot, update)
    # Прилетело "Посмотреть остатки" от РГКС
    if (user_com1 == "Начало") \
            and (user_role == 'РГ' or user_role == 'ВИ') \
            and ((bot.message.text == 'Посмотреть остатки') \
                 or (bot.message.text == 'Общие остатки')):
        bot.message.reply_text(get_area_remains(user_area), reply_markup=start_keyboard(user_role))


def chose_type(bot, update):
    bot.message.reply_text('Выберирири', reply_markup=end_keyboard())
    return "SN"


def get_anecdote(bot, update):
    recive = requests.get('http://anekdotme.ru/random')
    page = BeautifulSoup(recive.text, "html.parser")
    find = page.select('.anekdot_text')
    for text in find:
        page = (text.getText().strip())
    bot.message.reply_text(page)


def to_eng_and_up(text):
    layout = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                               'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                      "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                      "QWERTYUIOP{}ASDFGHJKL:'ZXCVBNM<>?~"))
    return text.translate(layout).upper()
