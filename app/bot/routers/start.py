from aiogram import Router, types
from aiogram.filters import Command
from app.bot.keyboards import main_menu_keyboard
from app.bot.messages import WELCOME_TEXT
from app.db.repositories.users import create_user

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await create_user(message.from_user.id, message.from_user.username)
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())