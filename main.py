from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from functionsSchedule import printing_schedule


API_TOKEN = ''

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)  # default - False
b1 = KeyboardButton('/help')
b2 = KeyboardButton('/расписание_очное')
b3 = KeyboardButton('/start')
b4 = KeyboardButton('/расписание_очно-заочное')
kb.add(b1).insert(b2).insert(b3).insert(b4)

HELP_COMMAND = ("\n"
                "<b>/help</b> - <em>список команд</em>\n"
                "<b>/start</b> - <em>старт бота</em>\n"
                "<b>/расписание_очное</b> - <em>отправка вашего расписания для  очного обучения</em>\n"
                "<b>/расписание_очно-заочное</b> - <em>отправка вашего расписания для  очно-заочного обучения</em>")


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


@dp.message_handler(commands=['расписание_очное'])
async def desc_command2(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=printing_schedule('очное'),
                           parse_mode="HTML")
    await message.delete()

@dp.message_handler(commands=['расписание_очно-заочное'])
async def desc_command2(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=printing_schedule('очно-заочное'),
                           parse_mode="HTML")
    await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
