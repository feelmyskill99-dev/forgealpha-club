from aiogram import Router, types
from aiogram.filters import Command

from app.bot.keyboards import main_menu_keyboard
from app.bot.messages import WELCOME_MESSAGE
from app.db.repositories.users import create_or_update_user

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    user = message.from_user
    if user is None:
        return

    await create_or_update_user(user.id, user.username)
    await message.answer(WELCOME_MESSAGE, reply_markup=main_menu_keyboard())