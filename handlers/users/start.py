from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from services.db_api.sqllite import DB
from keyboards.default import main_menu_kb
router = Router()

@router.message(CommandStart())
async def bot_start(message: Message):
    await DB.execute(
        sql="INSERT or IGNORE INTO users values( ?, ?, ?, ?, NULL, NULL)",
        parameters=(message.from_user.id,
                    message.from_user.first_name,
                    message.from_user.last_name,
                    message.from_user.username,),
        commit=True
    )

    await message.answer(
        "Salom 👋\nQuyidagi menyudan birini tanlang:",
        reply_markup=main_menu_kb,
    )
