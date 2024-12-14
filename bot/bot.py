from bot.bot_settings import BotSettings
from bot.handlers.command_handlers import BotCommandHandlers
from bot.handlers.message_handler import BotMessageHandlers
from telegram.ext import Application, CallbackQueryHandler
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler

class Bot(object):
    def __init__(self):
        token = self.__get_bot_token()
        self.__application = Application.builder().token(token).build()
        # self.__application.run_polling(timeout=60)
        self.__bot = self.__application.bot

    def run(self):
        self.__create_handlers()
        self.__application.run_polling()

    def __get_bot_token(self):
        bot_settings = BotSettings()
        return bot_settings.get_bot_token()

    def __add_handler(self, handler):
        self.__application.add_handler(handler)

    def __create_handlers(self):
        self.__create_command_handlers()
        self.__create_message_handlers()
        self.__create_error_handlers()

    def __create_command_handlers(self):
        command_handlers = BotCommandHandlers(self.__bot)
        message_handler = BotMessageHandlers(self.__bot)

        # START handler
        start_handler = CommandHandler('start', command_handlers.start)
        self.__add_handler(start_handler)

        # CAPS handler
        caps_handler = CommandHandler('caps', command_handlers.caps)
        self.__add_handler(caps_handler)

        # ADD ALLOWED USERS handler
        add_allowed_user_handler = ConversationHandler(
            entry_points=[CommandHandler('add_allowed_user', command_handlers.add_allowed_user)],
            states={
                0: [MessageHandler(filters.FORWARDED | filters.CONTACT, message_handler.get_user_id)]
            },
            fallbacks=[],
        )
        self.__add_handler(add_allowed_user_handler)

        # REMOVE ALLOWED USERS handler
        remove_users_handler = CommandHandler('remove_allowed_user', command_handlers.remove_allowed_user)
        self.__add_handler(remove_users_handler)
        self.__add_handler(CallbackQueryHandler(command_handlers.handle_remove_account_button, pattern=r"remove_user:\d+"))

        # TURN LEDS ON handler
        rainbow_animation_handler = CommandHandler('rainbow_animation', command_handlers.start_rainbow_animation)
        self.__add_handler(rainbow_animation_handler)

        # TURN LEDS OFF handler
        turn_leds_off_handler = CommandHandler('turn_leds_off', command_handlers.turn_leds_off)
        self.__add_handler(turn_leds_off_handler)

        # SET LEDS BRIGHTNESS handler
        set_brightness_handler = CommandHandler('set_brightness', command_handlers.set_brightness)
        self.__add_handler(set_brightness_handler)
        self.__add_handler(CallbackQueryHandler(command_handlers.slider_callback, pattern=r"^(increase|decrease|current)$"))

        # set_brightness_handler = ConversationHandler(
        #     entry_points=[CommandHandler('set_brightness', command_handlers.set_brightness)],
        #     states={
        #         0: [MessageHandler(filters.TEXT, message_handler.set_brightness)]
        #     },
        #     fallbacks=[],
        # )
        # self.__add_handler(set_brightness_handler)

        # SET LEDS BRIGHTNESS handler
        set_brightness_handler = ConversationHandler(
            entry_points=[CommandHandler('set_brightness', command_handlers.set_brightness)],
            states={
                0: [MessageHandler(filters.TEXT, message_handler.set_brightness)]
            },
            fallbacks=[],
        )
        self.__add_handler(set_brightness_handler)

    def __create_message_handlers(self):
        message_handler = BotMessageHandlers(bot_instance=self.__bot)

        # ECHO handler
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler.echo)
        self.__add_handler(echo_handler)

    def __create_error_handlers(self):
        message_handler = BotMessageHandlers(bot_instance=self.__bot)

        # UNKNOWN MESSAGE handler
        unknown_handler = MessageHandler(filters.COMMAND, message_handler.unknown)
        self.__add_handler(unknown_handler)
