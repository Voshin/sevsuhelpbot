from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
from keyboards import webinfo as wi

# Клавиатура
kb_reply = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
kb_sos = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_form_btn = ReplyKeyboardMarkup(resize_keyboard=True)

sos_button = KeyboardButton("🆘❗ МНЕ НУЖНА ПОМОЩЬ! ❗🆘")
send_locate = KeyboardButton("Отправить местоположение 🗺", request_location=True)
form_button = KeyboardButton("Редактирование формы 📨", web_app=wi.web_edit_form)
back_button = KeyboardButton("Назад 🔙")

kb_form_btn.add(KeyboardButton(text="Заполнить форму", web_app=wi.web_app))
kb_reply.add(sos_button, form_button)
kb_sos.add(send_locate, back_button)
