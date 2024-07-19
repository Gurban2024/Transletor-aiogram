from googletrans import Translator
import aiogram
from aiogram import filters, types, Bot, Dispatcher, F
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

bot = Bot(token='7377377394:AAFdxfmD3IH4ji8tpT2REf21ho1lMQmzRuw')
dp = Dispatcher()
translator = Translator()

class wait_words(StatesGroup):
    first_language = State()
    second_language = State()
    text = State()

# your_language = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text='Русский', callback_data='ru'), InlineKeyboardButton(text='English', callback_data='eng'), InlineKeyboardButton(text='Uzbek', callback_data='uz')]
#     ],
#     resize_keyboard=True
# )

translate_language = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='ru'), types.KeyboardButton(text='en'), types.KeyboardButton(text='uz')]
    ],
    resize_keyboard=True
)

@dp.message(filters.Command('start'))
async def start_function(message: types.Message, state: FSMContext):
    await state.set_state(wait_words.first_language)
    await message.answer('Здравствуйте, выберите язык для слов, которые вы будете присылать', reply_markup=translate_language)


@dp.message(wait_words.first_language)
async def first_language_function(message: types.Message, state: FSMContext):
    await state.update_data(first_language=message.text)
    await state.set_state(wait_words.second_language)
    await message.answer("Теперь второй язык", reply_markup=translate_language)


@dp.message(wait_words.second_language)
async def second_language_function(message: types.Message, state: FSMContext):
    await state.update_data(second_language=message.text)
    await state.set_state(wait_words.text)
    await message.answer("Теперь текст", reply_markup=types.ReplyKeyboardRemove())


@dp.message(wait_words.text)
async def text_function(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    first_language = data['first_language']
    second_language = data['second_language']
    text = data['text']
    translated_text = translator.translate(text=text, src=first_language, dest=second_language).text
    await message.answer(f"Вот ваш перевод: {translated_text}")
    await state.clear()


# @dp.callback_query(F.data == 'ru')
# async def first_ru(call: types.CallbackQuery):
#     await call.message.answer('Отлично, теперь выберите язык, на который вы хотите перевести', reply_markup=translate_language)

# @dp.callback_query(F.data == 'eng')
# async def first_eng(call: types.CallbackQuery):
#     await call.message.answer('Excellent, now choose the language to which you want to translate your words', reply_markup=translate_language)

# @dp.callback_query(F.data == 'uz')
# async def first_uz(call: types.CallbackQuery):
#     await call.message.answer('Yaxshi, endi so‘zlaringizni tarjima qilmoqchi bo‘lgan tilni tanlang', reply_markup=translate_language)

# @dp.callback_query(F.data == 'ru2')
# async def first_ru2(call: types.CallbackQuery, state: FSMContext):
#     await state.set_state(wait_words.ru)
#     await call.message.answer('Отлично, теперь напишите, что вы хотите перевести')

# @dp.callback_query(F.data == 'eng2')
# async def first_eng2(call: types.CallbackQuery, state: FSMContext):
#     await state.set_state(wait_words.eng)
#     await call.message.answer('Excellent, now write your words that you want to translate')

# @dp.callback_query(F.data == 'uz2')
# async def first_uz2(call: types.CallbackQuery, state: FSMContext):
#     await state.set_state(wait_words.uz)
#     await call.message.answer('Yaxshi, tarjima qilmoqchi bo‘lgan so‘zlarni yozing')

# @dp.message(wait_words.ru)
# async def translate_ru(message: types.Message, state: FSMContext):
#     word = message.text
#     translation = translator.translate(word, src='ru', dest='en').text
#     await message.answer(f'Translation: {translation}')
#     await state.clear()

# @dp.message(wait_words.eng)
# async def translate_eng(message: types.Message, state: FSMContext):
#     word = message.text
#     translation = translator.translate(word, src='en', dest='ru').text
#     await message.answer(f'Перевод: {translation}')
#     await state.clear()

# @dp.message(wait_words.uz)
# async def translate_uz(message: types.Message, state: FSMContext):
#     word = message.text
#     translation = translator.translate(word, src='uz', dest='ru').text
#     await message.answer(f'Перевод: {translation}')
#     await state.clear()


# @dp.message(F.dat)
# async def russian_function(message: types.Message, state: FSMContext):
#     await state.set_state(wait_words.language)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
