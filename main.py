import json

import telebot
from telebot import types

TOKEN = ""

channel_id = ""

bot = telebot.TeleBot(TOKEN)


def report_reserves():
    before_report = read_static_data()
    sh = ye = do = se = ch = pa = 0
    for i in before_report["shanbeh"]:
        sh += 1
    for i in before_report["yeksh"]:
        ye += 1
    for i in before_report["dosh"]:
        do += 1
    for i in before_report["sesh"]:
        se += 1
    for i in before_report["chaharsh"]:
        ch += 1
    for i in before_report["panjsh"]:
        pa += 1

    report_text = f"""
    {before_report["shanbeh"]} {sh}:شنبه
    {before_report["shanbeh"]} {sh}:یک شنبه
    {before_report["shanbeh"]} {sh}:دو شنبه
    {before_report["shanbeh"]} {sh}:سه شنبه
    {before_report["shanbeh"]} {sh}:چهار شنبه
    {before_report["shanbeh"]} {sh}:پنج شنبه
    """

    return report_text


def menu(text: str, username: str) -> bool:
    """
    :param text: chat text from user chat input.
    :param username: username from user chat input.
    :return: boolean depends on username in specific day.
    """
    if text == "شنبه":
        return reserve("shanbeh", username)

    elif text == "یک شنبه":
        return reserve("yeksh", username)

    elif text == "دو شنبه":
        return reserve("dosh", username)

    elif text == "سه شنبه":
        return reserve("sesh", username)

    elif text == "چهار شنبه":
        return reserve("chaharsh", username)

    elif text == "پنج شنبه":
        return reserve("panjsh", username)


def reserve(day: str, user: str) -> bool:
    """"
    :param day: chat text from user chat input
    :param user: username from user chat
    :return: boolean depends on
    """
    before_data = read_db_file()
    before_list = before_data.get("DATA")[day]
    for user_item in before_list:
        if user_item == user:
            return False
    append_to_db_file(day, user)
    return True


def read_db_file() -> dict:
    """"
    :return: dict
    """
    path = "static.json"
    with open(path, "r") as file:
        return json.load(file)


def append_to_db_file(day: str, user: str) -> None:
    """
    :param day: chat text from user chat input
    :param user: username from user chat
    """
    before_data = read_db_file()
    before_data.get("DATA")[day].append("@" + user)
    write_db_file(before_data)


def write_db_file(data) -> None:
    """
    :param data: dict
    """
    path = "static.json"
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def read_static_data() -> dict:
    """
    :return: list of static data
    """
    return read_db_file()["DATA"]


def read_valid_user() -> list:
    """
    :return: list of valid user
    """
    return read_db_file()["USERS"]


def valid_user(username: str) -> bool:
    """
    :param username: username from user chat
    :return: boolean if username is valid
    """
    if username not in read_valid_user():
        return False
    return True


def valid_admin(username: str) -> bool:
    """
        :param username: username from user chat
        :return: boolean if admin is valid
    """
    if username in ["only_smx", "n11228"]:
        return True
    return False


# Define the start command handler
@bot.message_handler(commands=['start'])
def start_command(message):
    print(message.chat.id)
    """Handle the /start command"""
    # Create the reply keyboard
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    # Add the available dates as buttons
    keyboard.add(
        types.KeyboardButton("شنبه"),
        types.KeyboardButton("یک شنبه"),
        types.KeyboardButton("دو شنبه"),
        types.KeyboardButton("سه شنبه"),
        types.KeyboardButton("چهار شنبه"),
        types.KeyboardButton("پنج شنبه")
    )
    # Send the welcome message with the reply keyboard
    bot.send_message(message.chat.id,
                     "سلام، به ربات رزرو غذا خوش آمدید. لطفا روز هایی که می خواهید غذا رزرو کنید، انتخاب کنید.",
                     reply_markup=keyboard)


@bot.message_handler(commands=['send'])
def send_data_to_channel(message):
    if valid_admin(message.from_user.username):
        before_send = report_reserves()
        bot.send_message(channel_id, before_send)


# Define the message handler for date selection
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    """Handle the date selection message"""
    # Check if the message is a valid date
    if valid_user(message.from_user.username):
        if message.text in ["شنبه", "یک شنبه", "دو شنبه", "سه شنبه", "چهار شنبه", "پنج شنبه"]:
            # if read_data_static(message.text, message.from_user.username):
            if menu(message.text, message.from_user.username):
                bot.send_message(message.chat.id, f"غذای شما برای روز {message.text} رزرو شد.")
            else:
                bot.send_message(message.chat.id, "غذای شما رزرو شده است. برای هر روز فقط یکبار رزرو امکان پذیر است.")

        else:
            bot.send_message(message.chat.id, "ورودی نامعتبر است. از صفحه کلید ربات استفاده کنید.")
            return

    else:
        bot.send_message(message.chat.id, "شما دسترسی ندارید برای ارتباط به اکانت زیر پیام دهید: @only_smx")


# run bot
bot.polling()
