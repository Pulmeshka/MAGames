from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
import sqlite3
from .utils import database_managment
import time
from core.handlers.technical_works import technicals

admin = [1355948406, ]
time_limit = None

class AntiAnonimousMiddleware(BaseMiddleware):
    async def on_process_message(self, *args):
        if technicals == 1:
            message = args[0]
            await message.reply("<b>⚠БОТ НА ТЕХ.РАБОТАХ⚠</b>\n<i>📎После завершения технических работ, наша команда сообщит вас об этом на официальном канале бота - @MAGamesNEWS</i>", parse_mode="HTML")
            raise CancelHandler

class AutoRegistrationMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, *args):
        global time_limit
        connection = sqlite3.connect("core/database/players.db")
        cursor = connection.cursor()
        message = args[0]
        user_id = message.from_user.id
        chat_id = message.chat.id
        if not time_limit:
            time_limit = int(time.time()) + 86400
        if int(time.time()) >= time_limit:
            database_managment.update_limit()
            time_limit = int(time.time()) + 86400
        balance = database_managment.get_balance(user_id)
        if balance is None:
            cursor.execute(
                "INSERT INTO "
                    "players "
                        "("
                            "id, "
                            "balance, "
                            "is_blocked, "
                            "rights_level, "
                            "bank, "
                            "referral, "
                            "invited, "
                            "rating, "
                            "marry, "
                            "awards, "
                            "theft, "
                            "justice, "
                            'transfer_limit, '
                            'uah_balance'
                        ") "
                "VALUES "
                    "("
                        "?, "
                        "100, "
                        "?, "
                        "1, "
                        "0, "
                        "0, "
                        "0, "
                        "0.0, "
                        "0, "
                        "?, "
                        "0, "
                        "0, "
                        "5000, "
                        '0.0'
                    ")",
                (
                    user_id,
                    False,
                    "—"
                )
            )
            connection.commit()
        cursor.execute(
            "SELECT "
                "chat_id "
            "FROM "
                "chats_and_participants "
            "WHERE "
                "chat_id=? and user_id=? ",
            (
            chat_id,
            user_id
            )
        )
        if not cursor.fetchone() and user_id != chat_id:
            cursor.execute(
                "INSERT INTO "
                    "chats_and_participants "
                        "("
                            "chat_id, "
                            "user_id"
                        ") "
                "VALUES "
                    "("
                       "?, "
                       "?"
                    ")",
                (
                    chat_id,
                    user_id
                )
            )
            connection.commit()
        cursor.execute(
            "SELECT "
                "balance "
            "FROM "
                "chats "
            "WHERE "
                "chat_id=?",
            (
            chat_id,
            )
        )
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO "
                    "chats "
                        "("
                            "chat_id, "
                            "balance, "
                            "protection"
                        ") "
                "VALUES "
                    "("
                       "?, "
                       "0, "
                       "0"
                    ")",
                (
                    chat_id,
                )
            )
            connection.commit()