from .base_handlers import BaseHandlers
from led_strip.strip_animations import StripAnimations
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from rpi_ws281x import *
import time

class BotCommandHandlers(BaseHandlers):
    def __init__(self, bot_instance=None):
        super().__init__(bot_instance)
        self._strip_animations = StripAnimations()

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

    async def remove_allowed_user(self, update: Update, context: CallbackContext):
        if not await self.can_respond(update):
            return
        
        users_arr = await self._user_service.get_allowed_users_list()
        keyboard = [[InlineKeyboardButton(user['full_name'], callback_data=f"remove_user:{user['id']}")] for user in users_arr]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Select the account you want to remove from \'Allowed Users\':', reply_markup=reply_markup)

    async def handle_remove_account_button(self, update: Update, context: CallbackContext):
        if not await self.can_respond(update):
            return
        
        query = update.callback_query
        await update.callback_query.answer() 

        user_id = query.from_user.id
        user_id_to_remove = int(query.data.split(":")[1])

        if self._bot_settings.remove_allowed_user(user_id, user_id_to_remove):
            message = 'User was removed successfully!'
        else:
            message = 'There was an error. Please try again!'

        await self.send_response_message(message, update, context)

    async def set_brightness(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return
        
        current_brightness = self._strip_animations.get_brightness()

        buttons = [
            [InlineKeyboardButton("➖", callback_data="decrease"),
            InlineKeyboardButton(f"{current_brightness}", callback_data="current"),
            InlineKeyboardButton("➕", callback_data="increase")]
        ]

        slider = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(f"Current brightness: {current_brightness}", reply_markup=slider)

    async def slider_callback(self, update: Update, context: CallbackContext):
        if not await self.can_respond(update):
            return
        
        query = update.callback_query
        await query.answer()

        current_brightness = self._strip_animations.get_brightness()
        query = update.callback_query
        adjustment = 20 if current_brightness >= 100 else (10 if current_brightness >= 20 else 5)

        if query.data == "increase" and current_brightness + adjustment <= 255:
            current_brightness += adjustment
        elif query.data == "decrease" and current_brightness - adjustment > 0:
            current_brightness -= adjustment

        await self._strip_animations.change_brightness(current_brightness, 20)
        
        buttons = [
            [InlineKeyboardButton("➖", callback_data="decrease"),
            InlineKeyboardButton(f"{current_brightness}", callback_data="current"),
            InlineKeyboardButton("➕", callback_data="increase")]
        ]

        slider = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(f"Adjust brightness: {current_brightness}", reply_markup=slider)

    async def start_rainbow_animation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return

        await self._strip_animations.rainbow_animation()

        message = 'Rainbow animation started.'
        await self.send_response_message(message, update, context)

    async def turn_leds_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.can_respond(update):
            return

        await self._strip_animations.fade_out(20)

        message = 'The LEDs were turned OFF.'
        await self.send_response_message(message, update, context)
        