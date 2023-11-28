from .base_handlers import BaseHandlers
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler

class BotCommandHandlers(BaseHandlers):
    def __init__(self, bot_instance=None):
        super().__init__(bot_instance)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return

        message = 'I\'m your bot, please talk to me!'
        await self.send_response_message(message, update, context)

    async def caps(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return

        if not context.args:
            message = 'Please write a message after /caps!'
            await self.send_response_message(message, update, context)

            return

        text_caps = ' '.join(context.args).upper()
        await self.send_response_message(text_caps, update, context)

    async def add_allowed_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return

        message = 'To add a user, please forward a message from the user or send their contact.'
        await self.send_response_message(message, update, context)

        return 0

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

    async def remove_allowed_user(self, update: Update, context: CallbackContext):
        users_arr = await self._user_service.get_allowed_users_list()
        keyboard = [[InlineKeyboardButton(user['full_name'], callback_data=str(user['id']))] for user in users_arr]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Select the account you want to remove from \'Allowed Users\':', reply_markup=reply_markup)

    async def handle_remove_account_button(self, update: Update, context: CallbackContext):
        query = update.callback_query
        user_id = query.from_user.id
        user_id_to_remove = int(query.data)

        if self._settings.remove_allowed_user(user_id, user_id_to_remove):
            message = 'User was removed successfully!'
        else:
            message = 'There was an error. Please try again!'

        await self.send_response_message(message, update, context)
