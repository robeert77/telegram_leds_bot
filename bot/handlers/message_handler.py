from .base_handlers import BaseHandlers
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext


class BotMessageHandlers(BaseHandlers):
    def __init__(self, bot_instance=None):
        super().__init__(bot_instance)

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return

        await self.send_response_message(update.message.text, update, context)

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return

        message = 'Sorry, I didn\'t understand that command.'
        await self.send_response_message(message, update, context)

    async def get_user_id(self, update: Update, context: CallbackContext):
        if not await self.can_respond(update):
            return

        forwarded_message = update.message.forward_from
        contact = update.message.contact

        user = None
        if forwarded_message is not None and hasattr(forwarded_message, 'id'):
            user = await self._user_service.get_user_object(forwarded_message['id'])
        elif contact is not None and hasattr(contact, 'user_id'):
            user = await self._user_service.get_user_object(contact['user_id'])

        if user is None:
            message = 'Invalid user. Please try again!'
            await self.send_response_message(message, update, context)

            return

        if self._settings.add_allowed_user(user):
            message = 'User has been added with success!'
        else:
            message = 'User already has been allowed to chat!'

        await self.send_response_message(message, update, context)

        return ConversationHandler.END

    async def set_brightness(self, update: Update, context: CallbackContext):
        if not await self.can_respond(update):
            return

        brightness_value = update.message.text
        if brightness_value.isdigit() and 0 <= int(brightness_value) <= 255:
            brightness_value = int(brightness_value)
        else:
            message = 'Please enter a number between 0 and 255!'
            await self.send_response_message(message, update, context)
            return 0

        # TODO
        # Send brightness_value to the led module

        message = f'Brightness was set to {brightness_value}'
        await self.send_response_message(message, update, context)

        return ConversationHandler.END

