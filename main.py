from logging import basicConfig, INFO
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.menu_button import MenuButtonWebApp

import config
from handlers import user
from keyboards import webinfo as wi

mem_storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=mem_storage)

# Включение логирования
basicConfig(level=INFO)


async def on_startup(_) -> None:
    """ Функция, срабатывающая при старте бота """
    # Метод, создающий кнопку сбоку от ввода
    await bot.set_chat_menu_button(menu_button=MenuButtonWebApp(text="Форма", web_app=wi.web_app))


async def on_shutdown(_) -> None:
    """ Функция, срабатывающая при завершении бота """
    pass


def main() -> None:
    """ Точка входа """
    user.register_handlers(dp)  # Регистрируем обработчики из файла user
    executor.start_polling(
        dp, skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown)


if __name__ == "__main__":
    main()
