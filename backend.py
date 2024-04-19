from aiogram import Bot, Dispatcher, executor, types
import constants
import sqlite3 as sq


def choose_day(message):
    day = constants.days.index(message.text)
    return day


def make_msg(data, day):
    data = list(data)
    data.sort(key=lambda x: x[1])
    message = f"{constants.days[day]}\n"
    for i in data:
        message += f"{constants.classes[i[1]]}: {i[0]}\n"
    return message


class db:
    def __init__(self):
        global db
        global cursor

        db = sq.connect("new.db")
        cursor = db.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS profile(user_id VARCHAR, day INTEGER, lesson TEXT, hour INTEGER)")
        db.commit()

    async def add_class(self, user_id, day, lesson, hour):
        cursor.execute("INSERT INTO profile(user_id, day, lesson, hour) VALUES (?, ?, ?, ?)",
                       (user_id, day, lesson, hour))
        db.commit()

    async def get_classes(self, user_id, day):
        data = cursor.execute(
            "SELECT lesson, hour FROM profile WHERE user_id = ? AND day = ?", (user_id, day)).fetchall()
        print(data)
        return data

    async def delete_class(self, user_id, day, hour):
        cursor.execute(
            "DELETE FROM profile WHERE user_id = ? AND day = ? AND hour = ?", (user_id, day, hour))
        db.commit()

    async def get_users(self, time, day):
        time = constants.start_classes.index(time)
        data = cursor.execute(
            "SELECT user_id, lesson FROM profile WHERE hour = ? AND day = ?", (time, day)).fetchall()
        return data
