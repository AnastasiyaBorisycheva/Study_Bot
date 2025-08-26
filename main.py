import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from database.init_db import create_tables

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(), debug=False)
