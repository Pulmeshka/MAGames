from aiogram import types
from .. import config

admins = config.admin
moderators = config.moderator
technicals = 0

async def technical_work(message: types.Message):
    global technicals
    user_id = message.from_user.id
    if user_id not in admins and user_id not in moderators:
        return
    if technicals == 0:
        technicals = 1
        return message.reply('✅Тех. работы запущены✅')
    technicals = 0
    await message.reply('❌Тех. работы завершены❌')