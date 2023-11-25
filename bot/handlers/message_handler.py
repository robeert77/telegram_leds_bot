from .base_handlers import BaseHandlers
from telegram import Update
from telegram.ext import ContextTypes

class BotMessageHandlers(BaseHandlers):
    def __init__(self, bot_instance=None):
        super().__init__(bot_instance)

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.message.text
        )

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Sorry, I didn\'t understand that command.'
        )
