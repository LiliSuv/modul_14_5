from aiogram import Bot, Dispatcher, executor, types
from aiogram. contrib. fsm_storage. memory import MemoryStorage
from aiogram. dispatcher. filters. state import State, StatesGroup
from aiogram. dispatcher import FSMContext
from aiogram. types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from aiogram. types import InlineKeyboardMarkup, InlineKeyboardButton
import prige_list
from crud_functions import get_all_products
from crud_functions import is_included
from crud_functions import all_user

api = '8................yc'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.row(button, button2)

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3=KeyboardButton(text="Перечень товаров")
button4=KeyboardButton(text="Регистрация")
kb1.row(button, button2,button3,button4)

kb2=InlineKeyboardMarkup()
b = InlineKeyboardButton(text='Product1', callback_data="product_bu")
b1 = InlineKeyboardButton(text='Product2', callback_data="product_bu")
b2 = InlineKeyboardButton(text='Product3', callback_data="product_bu")
b3 = InlineKeyboardButton(text='Product4', callback_data="product_bu")
b4=InlineKeyboardButton(text="Назад", callback_data='back_to_catalog')
kb2.row( b,b1, b2,b3,b4)


kb3=InlineKeyboardMarkup()
button=InlineKeyboardButton(text="Название продукта",callback_data="product")
button2=InlineKeyboardButton(text="Описание", callback_data='product_o')
button3=InlineKeyboardButton(text="Цена", callback_data='product_c')
kb3.row( button,button2,button3)


class UserState(StatesGroup):
    age=State()
    growth=State()
    weight= State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
i=0


@dp.message_handler (text='Информация')
async def inform(message):
    await message. answer ( 'Я бот, помогающий твоему здоровью')


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(us=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(em=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(ag=message.text)
    data = await state.get_data()
    try:
         str(data['em'])+"fff"
    except:
        pass
    else:
        if '@' in data['em']:
            pass

        else:
                await message.answer ('Вы не правильно ввели свой электронный адрес,попробуйте заново начать регистрацию')
                await message.answer ("Введите имя пользователя (только латинский алфавит):")
                await RegistrationState.username.set ()
                data['em'] = 'fff'
                data['em'] + 1

    try:
        int(data['ag'])
    except Exception:
        await message.answer ('Вы не правильно ввели свой возраст,попробуйте еще раз')
        data['ag'] = 'fff'
        data['ag'] + 1
        await message.answer ("Введите свой возраст:")
        await RegistrationState.age.set ()
    else:
        if  int(data['ag']) > 0 and  int(data['ag']) < 120:
            int(data['ag'])
        else:
            await message.answer ('Вы не правильно ввели свой возраст,попробуйте еще раз')
            data['ag'] = 'fff'
            data['ag']+1
            await message.answer ("Введите свой возраст:")
            await RegistrationState.age.set ()
    all_user(data['us'], data['em'], data['ag'])
    await message.answer ('Регистрация прошла успешно.')
    await state.finish ()
    await message.answer ("Выберите то, что Вас интересует.", reply_markup=kb1)


@dp.message_handler (text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию',reply_markup = kb)


@dp.message_handler (text='Перечень товаров')
async def get_buying_list(message):
    global  i
    if i<4:
        await message.answer(f'Витаминные добавки',reply_markup=kb3)
        with open(get_all_products()[i][3], 'rb') as img:
            await message.answer_photo(img)
        i=i+1
        await message.answer (f'Для продолжения просмотра нажмите кнопку "Перечень товаров"')
    else:
        await message.answer ('Просмотр закончен.Выберите продукт для покупки:', reply_markup=kb2)
        i=0
        await message.answer ('Если Вы еще не готовы совершить покупку, нажмите кнопку назад и Вы попадете в основное меню.')


@dp.callback_query_handler(text = "product_bu")
async def product_bu(call):
    await call. message. answer ('Вы успешно приобрели продукт. Спасибо за покупку.')
    await call. answer()


@dp.callback_query_handler(text = "product")
async def product(call):
    await call.message.answer(get_all_products()[i-1][0])
    await call.answer ()


@dp.callback_query_handler (text="product_o")
async def pr_o(call):
    await call.message.answer (get_all_products ()[i - 1][1])
    await call.answer ()


@dp.callback_query_handler (text="product_c")
async def pr_c(call):
    await call.message.answer (get_all_products ()[i - 1][2])
    await call.answer ()


@dp.callback_query_handler(text = "back_to_catalog")
async def back_to_catalog(call):
    await call.message.answer ("Привет!  Что Вас интересует?",reply_markup = kb1)
    await call. answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.answer ("Введите свой возраст")
    await UserState.age.set ()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer ('Введите свой рост:')
    await UserState.growth.set ()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data (growth=message.text)
    await message.answer ('Введите свой вес:')
    await UserState.weight.set ()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data (weight=message.text)
    data=await state.get_data ()
    try:
        int(data['weight'])
    except Exception:
        await message.answer ('Вы не правильно ввели свой вес')
        await state.finish ()
    else:
        if int (data['weight']) > 0 and int (data['weight']) < 350:
            int (data['weight'])
        else:
            data['weight'] = 'fff'
            await message.answer ('Вы не правильно ввели свой вес')
            await state.finish ()
    try:
        int(data['age'])
    except Exception:
        await message.answer ('Вы не правильно ввели свой возраст')
        await state.finish ()
    else:
        if  int(data['age']) > 0 and  int(data['age']) < 120:
            int(data['age'])
        else:
            data['age'] = 'fff'
            await message.answer ('Вы не правильно ввели свой возраст')
            await state.finish ()
    try:
        int(data['growth'])
    except Exception:
        await message.answer ('Вы не правильно ввели свой рост')
        await state.finish ()
    else:
        if  int(data['growth']) > 50 and  int(data['growth']) < 210:
            int(data['growth'])
        else:
            data['growth'] = 'fff'
            await message.answer ('Вы не правильно ввели свой рост')
            await state.finish ()
    a=10*int(data['weight'])+6.25 * int(data['growth'])-5*int(data['age'])-161
    await message.answer(f'Ваша норма каллорий {a}')
    await state.finish ()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула расчета калорий для женщины:\n 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer ("Привет!  Что Вас интересует?",reply_markup = kb1)


@dp.message_handler()
async def all_message(message):
    await message.answer ("Введите команду /start, чтобы начать общение")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
