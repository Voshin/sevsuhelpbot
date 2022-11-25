# Файл, содержащий пользовательские обработчики

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from geopy.geocoders import Nominatim

from keyboards import user


async def start_command_handler(message: types.Message):
    """ Обработчик команды /start"""
    # TODO Сделать проверку на наличие tg_id в базе
    """ tg_id_temp = None
        tg_id_base = []
        if tg_id_temp in tg_id_base:
            pass
        else:
            await message.answer(f"Выберите, что вас интересует:", reply_markup=user.kb_reply)
    """
    await message.answer(f"Здравствуйте, {message.from_user.full_name}!\n"
                         "Для заполнения формы, нажмите на кнопку ниже:", reply_markup=user.kb_form_btn)


async def after_form_handler(web_app_message):
    await web_app_message.answer("Выберите, что вас интересует:", reply_markup=user.kb_reply)


async def sos_command_handler(message: types.Message):
    """ Обработчик команды "SOS" """
    await message.answer("Выберите, что вас интересует:", reply_markup=user.kb_sos)


async def locate_command_handler(message: types.Message):
    """ Обработка адреса по отправленной геолокации """
    # TODO Переделать с вывода на экран, в вывод на сайт
    loc = Nominatim(user_agent="user")
    lat = message.location.latitude  # Широта
    lon = message.location.longitude  # Долгота

    coordinates = f"{lat}, {lon}"  # Координаты

    await message.answer(loc.reverse(coordinates, language="ru"), reply_markup=user.kb_sos)


async def back_handler(message: types.Message):
    """ Обработчик возврата в основное меню """
    await message.answer("Выберите, что вас интересует:", reply_markup=user.kb_reply)


def register_handlers(dp: Dispatcher) -> None:
    """ Функция для регистрации всех обработчиков """

    dp.register_message_handler(start_command_handler, commands=["start"])
    dp.register_message_handler(locate_command_handler, content_types=['location'])
    dp.register_message_handler(after_form_handler, content_types=['web_app_data'])
    dp.register_message_handler(sos_command_handler, Text(equals="🆘 ❗МНЕ НУЖНА ПОМОЩЬ!❗🆘"))
    dp.register_message_handler(back_handler, Text(equals="Назад 🔙"))
