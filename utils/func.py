import asyncio
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy import select
from db.models import User, User1C
from keyboards import start


async def create_new_user(message, session, data_1c, bot, phone_number=None, new_user=None):
    if phone_number is None:
        phone_number = data_1c['phone_number']
    user = User(chat_id=message.chat.id, username=message.chat.first_name, phone_number=phone_number)
    await session.merge(user)
    await session.commit()
    text_msg = f"Спасибо {message.chat.first_name}. Ожидайте обработки информации"
    await message.answer(text=text_msg)  # , reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(4)

    user = await session.execute(select(User).where(User.chat_id == int(message.chat.id)))
    user = user.scalar()
    user_1c = User1C(discount_card_number=data_1c['barcode'], description=data_1c['name'],
                     ref_1c=data_1c['ref'], user_id=user.id)
    await session.merge(user_1c)
    await session.commit()
    if new_user is not None:
        text_msg = f'{message.chat.first_name} у вас уже есть карта покупателя! 🤝 \n'
    else:
        text_msg = 'Спасибо что прошли регистрацию \n'
    text_msg += 'Что бы увидеть скидочкую карту ⬇нажмите кнопку⬇'
    await bot.set_chat_menu_button(chat_id=message.chat.id,
                                   menu_button=start.menu_button_personal_page(barcode=user_1c.discount_card_number,
                                                                               user_id=user.chat_id))
    await message.answer(text=text_msg, reply_markup=ReplyKeyboardRemove())