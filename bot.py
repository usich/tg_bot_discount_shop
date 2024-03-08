import asyncio
import logging
import sys

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers import start
import config
from middlewares import DbSessionMiddleware

from webapps.test import index


WEBHOOK_SECRET = "my-secret"


async def on_startup(bot: Bot) -> None:
    # If you have a self-signed SSL certificate, then you will need to send a public
    # certificate to Telegram
    logging.info("Bot has been started")
    await bot.set_webhook(f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}", drop_pending_updates=True)
    logging.info("Webhook has been set up")


async def main():
    engine = create_async_engine(url=config.DB_URL, echo=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(start.router)
    dp.startup.register(on_startup)

    app = web.Application()
    app.router.add_get("/", index)
    app["bot"]: Bot = bot
    app["session"]: AsyncSession

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        # secret_token=WEBHOOK_SECRET
    )
    webhook_requests_handler.register(app, path=f'{config.WEBHOOK_PATH}')

    setup_application(app, dp, bot=bot)
    # await bot.delete_webhook(drop_pending_updates=True)

    await web._run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)
                       # ssl_context=context


    # await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.getLogger('aiogram').setLevel(logging.DEBUG)
    asyncio.run(main())