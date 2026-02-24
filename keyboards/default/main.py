from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_kb() -> ReplyKeyboardMarkup:
    """Asosiy menyu keyboard"""
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text="📋 Mahsulotlarni ko'rish"),
        KeyboardButton(text="➕ Mahsulot qo'shish"),
        KeyboardButton(text="❌ Mahsulotni o'chirish")
    )

    builder.adjust(1)  # Har bir tugmani yangi qatorga joylashtirish
    return builder.as_markup(resize_keyboard=True)


# get_main_keyboard funksiyasini qo'shamiz (main_menu_kb ga alias)
get_main_keyboard = main_menu_kb


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Bekor qilish tugmasi"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🚫 Bekor qilish"))
    return builder.as_markup(resize_keyboard=True)