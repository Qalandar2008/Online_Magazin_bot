from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Tuple


def get_products_keyboard(products: List[Tuple]) -> InlineKeyboardMarkup:
    """Mahsulotlar ro'yxatini inline keyboard ko'rinishida qaytaradi"""
    builder = InlineKeyboardBuilder()

    for product in products:
        product_id, name, description, price = product
        button_text = f"{name} - {price} so'm"
        builder.add(InlineKeyboardButton(
            text=button_text,
            callback_data=f"select_product:{product_id}"
        ))

    builder.adjust(1)  # Har bir mahsulotni yangi qatorga joylashtirish
    return builder.as_markup()


def get_product_actions_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """Mahsulot uchun amallar keyboardi"""
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="✅ O'chirish",
            callback_data=f"confirm_delete:{product_id}"
        ),
        InlineKeyboardButton(
            text="🚫 Bekor qilish",
            callback_data="cancel_delete"
        )
    )

    builder.adjust(1)
    return builder.as_markup()