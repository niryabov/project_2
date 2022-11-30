from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


basic_keyboard = ReplyKeyboardMarkup()

weekday_keyboard = ReplyKeyboardMarkup()

classes_keyboard = ReplyKeyboardMarkup()

button_insert = KeyboardButton('Добавить занятие')
button_show = KeyboardButton('Показать расписание')
button_delete = KeyboardButton('Удалить занятие')

basic_keyboard.insert(button_insert).insert(button_show).insert(button_delete)


button_mond = KeyboardButton('Понедельник')
button_tues = KeyboardButton('Вторник')
button_wednes = KeyboardButton('Среда')
button_thur = KeyboardButton('Четверг')
button_fri = KeyboardButton('Пятница')
button_satur = KeyboardButton('Суббота')

button_back = KeyboardButton('Назад')


weekday_keyboard.insert(button_mond).insert(button_tues).insert(button_wednes).insert(
    button_thur).insert(button_fri).insert(button_satur).insert(button_back)

button_1 = KeyboardButton("1. 9:00 - 10:25")
button_2 = KeyboardButton("2. 10:45 - 12:10")
button_3 = KeyboardButton("3. 12:20 - 13:45")
button_4 = KeyboardButton("4. 13:55 - 15:20")
button_5 = KeyboardButton("5. 15:30 - 16:55")
button_6 = KeyboardButton("6. 17:05 - 18:30")
button_7 = KeyboardButton("7. 18:35 - 20:00")

classes_keyboard.insert(button_1).insert(button_2).insert(button_3).insert(
    button_4).insert(button_5).insert(button_6).insert(button_7).insert(button_back)
