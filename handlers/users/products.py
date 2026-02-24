from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from keyboards.default.main import main_menu_kb, get_cancel_keyboard
from keyboards.inline.product import get_products_keyboard, get_product_actions_keyboard
from states.product import ProductState
from services.db_api.models import Database
from config.config import load_config

router = Router()
config = load_config()
db = Database(config.db.db_path)


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Start komandasi"""
    await message.answer(
        "Assalomu alaykum! Mahsulotlar boshqaruvi botiga xush kelibsiz.\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=main_menu_kb()
    )


@router.message(F.text == "📋 Mahsulotlarni ko'rish")
async def show_products(message: Message):
    """Barcha mahsulotlarni ko'rsatish"""
    products = db.get_all_products()

    if not products:
        await message.answer(
            "Hozircha hech qanday mahsulot mavjud emas.",
            reply_markup=main_menu_kb()
        )
        return

    text = "📋 Mahsulotlar ro'yxati:\n\n"
    for product in products:
        product_id, name, description, price = product
        text += f"🆔 {product_id}. {name}\n"
        text += f"   📝 {description if description else 'Tavsif mavjud emas'}\n"
        text += f"   💰 {price} so'm\n\n"

    await message.answer(text, reply_markup=main_menu_kb())


@router.message(F.text == "➕ Mahsulot qo'shish")
async def add_product_start(message: Message, state: FSMContext):
    """Mahsulot qo'shishni boshlash"""
    await state.set_state(ProductState.waiting_for_name)
    await message.answer(
        "Mahsulot nomini kiriting:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(ProductState.waiting_for_name)
async def process_product_name(message: Message, state: FSMContext):
    """Mahsulot nomini qabul qilish"""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(
            "Amal bekor qilindi.",
            reply_markup=main_menu_kb()
        )
        return

    await state.update_data(product_name=message.text)
    await state.set_state(ProductState.waiting_for_description)
    await message.answer(
        "Mahsulot tavsifini kiriting (agar kerak bo'lmasa, '-' belgisini yuboring):",
        reply_markup=get_cancel_keyboard()
    )


@router.message(ProductState.waiting_for_description)
async def process_product_description(message: Message, state: FSMContext):
    """Mahsulot tavsifini qabul qilish"""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(
            "Amal bekor qilindi.",
            reply_markup=main_menu_kb()
        )
        return

    description = "" if message.text == "-" else message.text
    await state.update_data(product_description=description)
    await state.set_state(ProductState.waiting_for_price)
    await message.answer(
        "Mahsulot narxini kiriting (faqat son):",
        reply_markup=get_cancel_keyboard()
    )


@router.message(ProductState.waiting_for_price)
async def process_product_price(message: Message, state: FSMContext):
    """Mahsulot narxini qabul qilish"""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(
            "Amal bekor qilindi.",
            reply_markup=main_menu_kb()
        )
        return

    try:
        price = float(message.text.replace(',', '.'))
        data = await state.get_data()

        # Mahsulotni databasega qo'shish
        product_id = db.add_product(
            name=data['product_name'],
            description=data.get('product_description', ''),
            price=price
        )

        await state.clear()
        await message.answer(
            f"✅ Mahsulot muvaffaqiyatli qo'shildi!\n"
            f"ID: {product_id}\n"
            f"Nomi: {data['product_name']}\n"
            f"Tavsif: {data.get('product_description', '')}\n"
            f"Narxi: {price} so'm",
            reply_markup=main_menu_kb()
        )
    except ValueError:
        await message.answer(
            "❌ Noto'g'ri format. Iltimos, faqat son kiriting (masalan: 50000 yoki 50000.50):",
            reply_markup=get_cancel_keyboard()
        )


@router.message(F.text == "❌ Mahsulotni o'chirish")
async def delete_product_start(message: Message):
    """Mahsulot o'chirishni boshlash"""
    products = db.get_all_products()

    if not products:
        await message.answer(
            "Hozircha hech qanday mahsulot mavjud emas.",
            reply_markup=main_menu_kb()
        )
        return

    await message.answer(
        "O'chirmoqchi bo'lgan mahsulotingizni tanlang:",
        reply_markup=get_products_keyboard(products)
    )


@router.callback_query(lambda c: c.data and c.data.startswith('select_product:'))
async def select_product_for_delete(callback: CallbackQuery):
    """O'chirish uchun mahsulot tanlash"""
    product_id = int(callback.data.split(':')[1])
    product = db.get_product(product_id)

    if not product:
        await callback.message.edit_text("❌ Mahsulot topilmadi.")
        await callback.answer()
        return

    _, name, description, price = product

    await callback.message.edit_text(
        f"🆔 ID: {product_id}\n"
        f"📝 Nomi: {name}\n"
        f"📋 Tavsif: {description if description else 'Tavsif mavjud emas'}\n"
        f"💰 Narxi: {price} so'm\n\n"
        f"Ushbu mahsulotni o'chirishni tasdiqlaysizmi?",
        reply_markup=get_product_actions_keyboard(product_id)
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith('confirm_delete:'))
async def confirm_delete_product(callback: CallbackQuery):
    """Mahsulot o'chirishni tasdiqlash"""
    product_id = int(callback.data.split(':')[1])

    if db.delete_product(product_id):
        await callback.message.edit_text(
            f"✅ Mahsulot muvaffaqiyatli o'chirildi!"
        )
    else:
        await callback.message.edit_text(
            f"❌ Mahsulot o'chirishda xatolik yuz berdi."
        )

    # Asosiy menyuga qaytish
    await callback.message.answer(
        "Asosiy menyu:",
        reply_markup=main_menu_kb()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data == "cancel_delete")
async def cancel_delete_product(callback: CallbackQuery):
    """Mahsulot o'chirishni bekor qilish"""
    await callback.message.edit_text("🚫 Amal bekor qilindi.")
    await callback.message.answer(
        "Asosiy menyu:",
        reply_markup=main_menu_kb()
    )
    await callback.answer()