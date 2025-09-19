import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.commands import set_admin_commands, set_common_commands
from bot.handlers.delete_activity_handler import router as delete_router
from bot.handlers.fsm_add_messages import router as add_router
from bot.handlers.list_handler import router as list_router
from bot.handlers.start_handler import router as start_router
from bot.middlewares import DbSessionMiddleware
from database.init_db import create_tables

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def on_startup(bot: Bot):
    await set_admin_commands(bot)
    await set_common_commands(bot)
    print("Команды настроены!")


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp.update.outer_middleware(DbSessionMiddleware())

    await create_tables()
    dp.startup.register(on_startup)

    dp.include_router(router=start_router)
    dp.include_router(router=add_router)
    dp.include_router(router=list_router)
    dp.include_router(router=delete_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(), debug=False)
