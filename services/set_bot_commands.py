from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    """Bot komandalarini o'rnatish"""
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())