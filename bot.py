
"""
This is a echo bot.
It echoes any incoming text messages.
"""
from datetime import datetime, date, time

import logging
import constants
import keyboards
import backend
import states
import aioschedule
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types


from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=constants.token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
db = backend.db()


async def background_proccess(user, ):
    await()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):

    await message.reply("Привет! Выберите, что сделать!", reply_markup=keyboards.basic_keyboard)


@dp.message_handler(lambda message: message.text in constants.basic_commands, state='*')
async def command_choice(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == 'Добавить занятие':
        await message.answer("Выберите день недели",  reply_markup=keyboards.weekday_keyboard)
        await state.set_state(states.CurStates.ADDSTATE)

    if message.text == 'Удалить занятие':
        await message.answer("Выберите день недели",  reply_markup=keyboards.weekday_keyboard)
        await state.set_state(states.CurStates.DELETESTATE)

    if message.text == 'Показать расписание':
        await message.answer("Выберите день недели",  reply_markup=keyboards.weekday_keyboard)
        await state.set_state(states.CurStates.SHOWSTATE)


#------------------------------------CHOOSING DAY-----------------------------------------

@dp.message_handler(lambda message: message.text in constants.days, state=states.CurStates.SHOWSTATE)
async def day_choice(message: types.Message):
    day = backend.choose_day(message)
    state = dp.current_state(user=message.from_user.id)
    async with state.proxy() as data:
        data['day'] = day
    data = await db.get_classes(message.from_user.id, day)
    if len(data) == 0:
        await message.answer("В этот день нет добавленных занятий", reply_markup=keyboards.basic_keyboard)
        await state.reset_state()
    else:

        text = backend.make_msg(data, day)

        await message.answer(text, reply_markup=keyboards.basic_keyboard)
        await state.reset_state()


@dp.message_handler(lambda message: message.text in constants.days, state='*')
async def day_choice(message: types.Message):
    day = backend.choose_day(message)
    state = dp.current_state(user=message.from_user.id)
    async with state.proxy() as data:
        data['day'] = day
    await message.answer("Выберите пару", reply_markup=keyboards.classes_keyboard)


#------------------------------choosing a pair---------------------------------------------


@dp.message_handler(lambda message: message.text in constants.classes, state=states.CurStates.ADDSTATE)
async def class_choice(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    lesson = constants.classes.index(message.text)
    async with state.proxy() as data:
        data['lesson'] = lesson
    await message.answer("Напишите информацию о занятии", reply_markup=None)


@dp.message_handler(lambda message: message.text in constants.classes, state=states.CurStates.DELETESTATE)
async def class_choice(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    lesson = constants.classes.index(message.text)
    async with state.proxy() as data:
        day = data['day']
    await db.delete_class(message.from_user.id, day, lesson)
    await message.answer("Информация о занятии удалена", reply_markup=keyboards.basic_keyboard)
    state.reset_state()


#-------------------------------------other options----------------------------------------


@dp.message_handler(state=states.CurStates.ADDSTATE)
async def class_choice(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    async with state.proxy() as data:
        day = data['day']
        lesson = data['lesson']
    await db.add_class(message.from_user.id, day, message.text, lesson)
    await message.answer("Заняте добавлено", reply_markup=keyboards.basic_keyboard)
    state.reset_state()


@dp.message_handler(lambda message: message.text == 'Назад', state='*')
async def back(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    await message.answer("Выберите действие", reply_markup=keyboards.basic_keyboard)
    state.reset_state()


async def check_events():
    time = f"{datetime.now():%H:%M}"
    day = datetime.now().weekday()
    data = await db.get_users(time, day)
    for i in data:
        await bot.send_message(i[0], f"{i[1]} через 10 минут")


async def scheduler():
    aioschedule.every().day.at("08:50").do(check_events)
    aioschedule.every().day.at("10:35").do(check_events)
    aioschedule.every().day.at("12:10").do(check_events)
    aioschedule.every().day.at("13:45").do(check_events)
    aioschedule.every().day.at("15:20").do(check_events)
    aioschedule.every().day.at("16:55").do(check_events)
    aioschedule.every().day.at("18:25").do(check_events)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
