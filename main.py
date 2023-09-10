from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from functionsSchedule import printing_schedule, updating_schedule

API_TOKEN = '6459347226:AAHdwlZJK65OU8loNvZ9-IN74PElKKkQKbw'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)  # default - False
b1 = KeyboardButton('/help')
b2 = KeyboardButton('/schedule')
b3 = KeyboardButton('/start')
kb.add(b1).insert(b2).insert(b3)

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>старт бота</em>
<b>/schedule</b> - <em>отправка вашего расписания</em>"""


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_COMMAND,
                           parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Добро пожаловать в наш Бот!",
                           parse_mode="HTML",
                           reply_markup=kb)
    await message.delete()


@dp.message_handler(commands=['schedule'])
async def desc_command2(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=printing_schedule(),
                           parse_mode="HTML")
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
