from aiogram.types import (InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,
                           MenuButtonWebApp, WebAppInfo)
from aiogram.types.web_app_info import WebAppInfo

kb_share_phone_number = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[
    KeyboardButton(text='📱Поделиться номером телефона', request_contact=True)
]])


def kb_registration_page(phone_number):
    url = 'https://usich-github-io.vercel.app/register.html'
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[
        KeyboardButton(text='Открыть форму регистрации',
                            web_app=WebAppInfo(url=f'{url}?phone_number={phone_number}'))
    ]])
    return kb


def menu_button_personal_page(**kwargs):
    url = 'https://usich-github-io.vercel.app/profile.html'
    url_params = '&'.join('{}={}'.format(key, val) for key, val in sorted(kwargs.items()))
    menu_button = MenuButtonWebApp(text="Показать карту",
                                   # web_app=WebAppInfo(url='https://bagira-zoo.club/catalog/stock/'))
                                   web_app=WebAppInfo(url=f"{url}?{url_params}"))
    return menu_button

# def registration_user():
#
#     ikb = InlineKeyboardButton(text="Поделиться номером телефона", request_contact=True)
#     # ikbwa = KeyboardButton(text="site", web_app=WebAppInfo(url='https://usich-github-io.vercel.app/register.html?'))
#
#     kb = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[ikb]])
#     return kb