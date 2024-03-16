import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from goole_sheets import get_google_sheets_data, check, generate_pie_chart
from state import UserDate
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


API_TOKEN = 'Your bot token'


storage = MemoryStorage()
bot =Bot(token=API_TOKEN)
dp=Dispatcher(bot, storage=storage)


logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)

btn = InlineKeyboardMarkup(row_width=2)
btn.insert(InlineKeyboardButton(text='Ha', callback_data='ha'))
btn.insert(InlineKeyboardButton(text='Yoq', callback_data='yoq'))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Ma'lumotingizni bilish uchun ismingizni kiriting")
    await UserDate.photo.set()

@dp.message_handler(state=UserDate.photo)
async def exo(message: types.Message,state:FSMContext):
    data1 = get_google_sheets_data()
    data1 = data1[0]
    
    
    data = check(message.text)
    if data:
        await message.answer(f"Name: {data[0]}")
        await message.answer(f"Group: {data[1]}")
        for i in range(2,len(data)-1):
            text = f"""{data1[i]}: {'✔️' if data[i] == '1' else '❌'}"""
            await message.answer(text)
            new = data[3:]
            absent = new.count('0')
            present = new.count('1')
            image = generate_pie_chart(present, absent)
        await state.update_data(photo = image)
        await message.answer("Davomatingizni sxemada korishni hohlaysizmi", reply_markup=btn)
        await UserDate.check.set()
    else:
        await message.answer("Ismingiz hato kiritilgan yoki siz bazada yo'qsiz")
        await UserDate.check.set()
@dp.callback_query_handler(state=UserDate.check)
async def exo(call: types.CallbackQuery,state:FSMContext):  
    if call.data == 'ha':
        data = await state.get_data()
        image = data.get('photo')
        await call.message.answer_photo(photo=open(image, 'rb'), caption="Your chart")
        await call.message.delete()
        await state.finish()
        await state.reset_data()
        await call.message.answer("Ma'lumotingizni bilish uchun ismingizni kiriting ")
        await UserDate.photo.set()
    elif call.data == 'yoq':
        await call.message.answer("Ma'lumotingizni bilish uchun ismingizni kiriting ")
        await state.finish()
        await state.reset_data()
        await UserDate.photo.set()
        await call.message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)