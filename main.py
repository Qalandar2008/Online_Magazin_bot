import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties  # Yangi import
from aiogram.enums import ParseMode  # Yangi import

from config.config import load_config
from handlers.users import products
from keyboards.default.main import main_menu_kb
from services.db_api.models import Database
from middlewares.throttling import ThrottlingMiddleware
from services.notify_admins import on_startup_notify
from services.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.info("Bot ishga tushmoqda...")

    # Konfiguratsiyani yuklash
    config = load_config()

    # Bot va dispatcher yaratish (yangilangan format)
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # parse_mode ni shu yerda sozlaymiz
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Middleware
    dp.message.middleware(ThrottlingMiddleware())

    # Routerlarni ulash
    dp.include_router(products.router)

    # Database ni yaratish
    db = Database(config.db.db_path)

    # Bot ishga tushganda bajariladigan amallar
    await on_startup_notify(bot, config.bot.admin_ids)
    await set_default_commands(bot)

    # Botni polling rejimida ishga tushirish
    try:
        logger.info("Bot polling boshlanmoqda...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot to'xtatildi")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi")