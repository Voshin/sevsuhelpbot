from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import webinfo as wi

# Клавиатура
kb_reply = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_sos = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_form_btn = InlineKeyboardMarkup()

sos_button = KeyboardButton("🆘❗ МНЕ НУЖНА ПОМОЩЬ! ❗🆘")
send_locate = KeyboardButton("Отправить местоположение 🗺", request_location=True)
form_button = KeyboardButton("Редактирование формы 📨", web_app=wi.web_edit_form)
back_button = KeyboardButton("Назад 🔙")

kb_form_btn.add(InlineKeyboardButton(text="Заполнить форму", web_app=wi.web_app))
kb_reply.add(sos_button).add(form_button)
kb_sos.add(send_locate, back_button)