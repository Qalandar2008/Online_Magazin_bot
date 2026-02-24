import logging
from aiogram import Bot


async def on_startup_notify(bot: Bot, admin_ids: list[int]):
    """Bot ishga tushgani haqida adminlarga xabar berish"""
    for admin_id in admin_ids:
        try:
            await bot.send_message(
                admin_id,
                "✅ Bot ishga tushdi!\n\n"
                "Barcha funksiyalar ishlamoqda."
            )
        except Exception as e:
            logging.exception(f"Admin {admin_id} ga xabar yuborib bo'lmadi: {e}")