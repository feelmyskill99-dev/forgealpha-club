from aiogram import Router, types
from aiogram.filters import Command

from app.core.config import settings

router = Router()


@router.message(Command("admin"))
async def cmd_admin(message: types.Message) -> None:
    user = message.from_user
    if user is None or user.id != settings.ADMIN_ID:
        return

    parts = (message.text or "").split()
    command = parts[0] if parts else "/admin"

    await message.answer(f"Admin panel is available. Command: {command}")