import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from handlers import start
import config
from middlewares import DbSessionMiddleware


async def main():
    engine = create_async_engine(url=config.DB_URL, echo=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(config.BOT_TOKEN)#, parse_mode="HTML")
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(start.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())