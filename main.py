from asyncio import run
from logging import basicConfig, INFO

from aiogram import Bot, Dispatcher

from config_data.config import load_config


async def bot_initialization() -> None:
    basicConfig(level=INFO, format='[%(asctime)s][%(levelname)s]: file = %(filename)s | message =  %(message)s')

    config = load_config()
    bot = Bot(token=config.bot.token, parse_mode='HTML', disable_web_page_preview=True)
    dp = Dispatcher()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    run(bot_initialization())
