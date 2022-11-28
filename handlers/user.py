# Файл, содержащий пользовательские обработчики

from json import dumps, loads
from aiohttp import ClientSession
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from geopy.geocoders import Nominatim

from keyboards import user

HEADERS = {"Content-Type": "application/json"}

CREATE_USER_API_URL = "http://localhost:8000/api/v1/users/create"
UPDATE_USER_API_URL = "http://localhost:8000/api/v1/users/update"
GET_USER_API_URL = "http://localhost:8000/api/v1/users/get/"
ADD_USER_TO_SOS_API_URL = "http://localhost:8000/api/v1/users/add-sos"


async def start_command_handler(message: types.Message):
    """ Обработчик команды /start """

    # Проверяем, есть ли уже пользователь в базе
    async with ClientSession() as session:
        async with session.get(GET_USER_API_URL +
                               str(message.from_user.id)) as response:
            data = await response.json()
            if data:
                await message.answer("Выберите, что вас интересует:",
                                     reply_markup=user.kb_reply)
            else:
                await message.answer(
                    f"Здравствуйте, {message.from_user.full_name}!\n"
                    "Заполните форму для дальнейшего использования бота.",
                    reply_markup=user.kb_form_btn,
                )


async def after_form_handler(web_app_message: types.WebAppData):
    # Данные приходят в виде JSON строки
    # C помощью функции loads форматируем строку в словарь Python
    web_app_data = loads(web_app_message.web_app_data.data)

    if web_app_data["user_group"] == "Другая":
        web_app_data["user_group"] = web_app_data["user_extra_group"]

    if web_app_data["user_location"] == "Другое":
        web_app_data["user_location"] = web_app_data["user_extra_location"]

    # Формируем данные для запроса на создание/изменение пользователя
    user_data = {
        "tg_id": web_app_message.from_user.id,
        "user_university": web_app_data["user_university"],
        "user_group": web_app_data["user_group"],
        "user_first_name": web_app_data["user_first_name"],
        "user_second_name": web_app_data["user_second_name"],
        "user_last_name": web_app_data["user_last_name"],
        "user_location": web_app_data["user_location"],
    }
    async with ClientSession() as session:
        async with session.get(GET_USER_API_URL +
                               str(web_app_message.from_user.id)) as response:
            data = await response.json()

    params = {"tg_id": web_app_message.from_user.id}

    if data:
        del user_data["tg_id"]
        async with ClientSession() as session:
            async with session.put(UPDATE_USER_API_URL,
                                   data=dumps(user_data),
                                   params=params,
                                   headers=HEADERS) as response:
                pass
    else:
        async with ClientSession() as session:
            async with session.post(CREATE_USER_API_URL,
                                    data=dumps(user_data),
                                    headers=HEADERS) as response:
                pass

    await web_app_message.answer("Выберите, что вас интересует:",
                                 reply_markup=user.kb_reply)


async def sos_command_handler(message: types.Message):
    """Обработчик команды "SOS" """
    await message.answer("Выберите, что вас интересует:",
                         reply_markup=user.kb_sos)


async def profile_command_handler(message: types.Message):
    """ Обработчик личного кабинета """
    await message.answer("Выберите, что вас интересует:",
                         reply_markup=user.kb_profile)


async def user_info_command_handler(message: types.Message):
    """ Вывод личных данных пользователя """
    async with ClientSession() as session:
        async with session.get(GET_USER_API_URL +
                               str(message.from_user.id)) as response:
            data = await response.json()

    await message.answer(
        f"ФИО: {data['user_second_name']} "
        f"{data['user_first_name']} "
        f"{data['user_last_name']}\n\n"
        f"Институт: {data['user_university']}\n\n"
        f"Группа: {data['user_group']}\n\n"
        f"Местоположение: {data['user_location']}",
        reply_markup=user.kb_profile)


async def locate_command_handler(message: types.Message):
    """ Обработка адреса по отправленной геолокации """
    loc = Nominatim(user_agent="user")
    lat = message.location.latitude  # Широта
    lon = message.location.longitude  # Долгота

    coordinates = f"{lat}, {lon}"  # Координаты
    cur_loc = loc.reverse(coordinates, language="ru")

    async with ClientSession() as session:
        async with session.get(GET_USER_API_URL +
                               str(message.from_user.id)) as response:
            data = await response.json()

    user_data = {
        "user_university": data["user_university"],
        "user_group": data["user_group"],
        "user_first_name": data["user_first_name"],
        "user_second_name": data["user_second_name"],
        "user_last_name": data["user_last_name"],
        "user_location": str(cur_loc),
    }

    params = {"tg_id": message.from_user.id}

    async with ClientSession() as session:
        async with session.put(UPDATE_USER_API_URL,
                               data=dumps(user_data),
                               params=params,
                               headers=HEADERS) as response:
            pass

    async with ClientSession() as session:
        async with session.post(ADD_USER_TO_SOS_API_URL,
                                params=params,
                                headers=HEADERS) as response:
            pass

    await message.answer(
        "Местоположение успешно отправлено!\n"
        "Выберите, что вас интересует:",
        reply_markup=user.kb_reply)


async def back_handler(message: types.Message):
    """Обработчик возврата в основное меню"""
    await message.answer("Выберите, что вас интересует:",
                         reply_markup=user.kb_reply)


def register_handlers(dp: Dispatcher) -> None:
    """Функция для регистрации всех обработчиков"""

    dp.register_message_handler(start_command_handler, commands=["start"])
    dp.register_message_handler(after_form_handler,
                                content_types=["web_app_data"])
    dp.register_message_handler(locate_command_handler,
                                content_types=["location"])
    dp.register_message_handler(sos_command_handler,
                                Text(equals="🆘❗ МНЕ НУЖНА ПОМОЩЬ! ❗🆘"))
    dp.register_message_handler(profile_command_handler,
                                Text(equals="Личный кабинет"))
    dp.register_message_handler(user_info_command_handler,
                                Text(equals="Мои данные"))
    dp.register_message_handler(back_handler, Text(equals="Назад 🔙"))
