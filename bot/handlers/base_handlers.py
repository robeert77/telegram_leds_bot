from telegram import Update
from telegram.ext import ContextTypes

from ..bot_settings import BotSettings
from ..user_service import UserService

class BaseHandlers(object):
    _bot_settings = None
    _user_service = None

    def __init__(self, bot_instance=None):
        if BaseHandlers._bot_settings is None:
            BaseHandlers._bot_settings = BotSettings()

        if BaseHandlers._user_service is None:
            BaseHandlers._user_service = UserService(bot=bot_instance)

    async def can_respond(self, update: Update):
        if BaseHandlers._user_service is None:
            return False
        return await BaseHandlers._user_service.is_user_allowed(update)

    async def send_response_message(self, message, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
