import json

from aiogram import Router, F, types, Bot, enums
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ContentType, MenuButtonDefault
from sqlalchemy import select
from keyboards import start
from db.models import User, User1C
from sqlalchemy.ext.asyncio import AsyncSession
from utils.exchange_1c import get_user_data_1c, create_user_discount
from utils.func import create_new_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, bot: Bot):
    await bot.set_chat_menu_button(chat_id=message.chat.id, menu_button=MenuButtonDefault())
    result = await session.execute(select(User).where(User.chat_id == int(message.chat.id)))
    user = result.scalar()
    if user is None:
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAIBOmXMkvFuHFDsLIACIdO_tPOYcwFEAAI5AAOtZbwUdHz8lasybOo0BA')
        text_msg = 'Добро пожаловать. \n'
        text_msg += 'Для того что бы продолжить работу \n'
        text_msg += '⬇️поделитесь номером телефона ⬇️'
        await message.answer(text=text_msg, reply_markup=start.kb_share_phone_number, parse_mode=enums.ParseMode.HTML)
        await bot.set_chat_menu_button(chat_id=message.chat.id, menu_button=MenuButtonDefault())
    else:
        sql = select(User1C).where(User1C.user_id == int(user.id))
        result = await session.execute(sql)
        user_1c = result.scalar()
        text_msg = f'С возвращением {user.username} \n'
        text_msg += 'Что бы увидеть скидочкую карту \n'
        text_msg += 'нажмите кнопку \n'
        text_msg += '⬇⬇⬇⬇⬇⬇⬇⬇'
        await message.answer(text=text_msg)
        await bot.set_chat_menu_button(chat_id=message.chat.id,
                                       menu_button=start.menu_button_personal_page(
                                           barcode=user_1c.discount_card_number,
                                           user_id=message.chat.id))


@router.message(F.contact)
async def process_contact(message: types.Message, session: AsyncSession, bot: Bot):
    if message.chat.id != message.contact.user_id:
        await message.answer('Вы отправили не свой номер телефона')
        return
    await bot.delete_message(message.chat.id, message.message_id)
    phone_number_current = message.contact.phone_number
    phone_number = '+{}.({}).{}-{}-{}'.format(phone_number_current[0], phone_number_current[1:4],
                                              phone_number_current[4:7],phone_number_current[7:9],
                                              phone_number_current[9:])

    data_1c = await get_user_data_1c(phone_number=phone_number)
    if data_1c['find_user']:
        await create_new_user(message, session, data_1c, bot, phone_number_current, new_user=True)
    else:
        await message.answer(text='Не нашли Вашей карты по вашему номеру телефона')
        text_msg = 'Если желаете получить бонусную карту \n'
        text_msg += 'Пройдите регистрацию \n'
        text_msg += '⬇⬇⬇⬇⬇⬇⬇⬇'
        await message.answer(text=text_msg, reply_markup=start.kb_registration_page(phone_number))


@router.message(F.content_type.in_(ContentType.WEB_APP_DATA, ))
async def get_web_app_data(message: types.Message, session: AsyncSession, bot: Bot):
    wa_data = message.web_app_data.data
    wa_data = json.loads(wa_data)
    print(wa_data)
    description = f"{wa_data['firstName']} {wa_data['lastName']} {wa_data['middleName']}"
    create_user_disc = await create_user_discount(description, wa_data['phone_number'], wa_data['email'])
    if not create_user_disc['error']:
        await create_new_user(message, session, create_user_disc, bot)


@router.message(Command('images'))
async def send_photo(message: Message):
    print('sadasd')


@router.message(F.sticker)
async def stick(message: types.Message, session: AsyncSession):
    sql = select(User).where(User.chat_id == int(message.chat.id))
    res = await session.execute(sql)
    s = res.scalar()
