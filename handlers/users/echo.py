from aiogram import Router
from aiogram.types import Message
from services.db_api.sqllite import DB
router = Router()

@router.message()
async def bot_echo(message: Message):
    await DB.execute(
        sql="INSERT or REPLACE INTO users_chat values(?,?)",
        parameters=(message.from_user.id,
                    message.text
                    ),
        commit=True
    )
    await message.answer(message.text)
