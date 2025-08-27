from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllChatAdministrators
from aiogram import Bot


commands = [
    BotCommand(command="start", description="Запуск бота"),
    BotCommand(command="list", description="Показать последние 10 записей Активности"),
    BotCommand(command="add", description="Добавить новую запись в Активность"),
    BotCommand(command="edit", description="Внести изменения в существующую запись"),
    BotCommand(command="delete", description="Удалить существующую запись об Активности"),
    BotCommand(command="cancel", description="Галя, у нас отмена!"),
    BotCommand(command="help", description="Помощь")
]


admin_commands = [
    BotCommand(command="iamadmin", description="Команда администратора"),
]


async def set_common_commands(bot: Bot):
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )


async def set_admin_commands(bot: Bot):
    await bot.set_my_commands(
        commands=admin_commands,
        scope=BotCommandScopeAllChatAdministrators()
    )
