from bot.bot_settings import BotSettings
from bot.handlers.command_handlers import BotCommandHandlers
from bot.handlers.message_handler import BotMessageHandlers
from telegram.ext import Application, CallbackQueryHandler
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler

class Bot(object):
    def __init__(self):
        token = self.__get_bot_token()
        self.__application = Application.builder().token(token).build()
        self.__bot = self.__application.bot

    def run(self):
        self.__create_handlers()
        self.__application.run_polling()

    def __get_bot_token(self):
        settings = BotSettings()
        return settings.get_bot_token()

    def __add_handler(self, handler):
        self.__application.add_handler(handler)

    def __create_handlers(self):
        self.__create_command_handlers()
        self.__create_message_handlers()
        self.__create_error_handlers()

    def __create_command_handlers(self):
        command_handlers = BotCommandHandlers(bot_instance=self.__bot)

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
                0: [MessageHandler(filters.FORWARDED | filters.CONTACT, command_handlers.get_user_id)]
            },
            fallbacks=[],
        )
        self.__add_handler(add_allowed_user_handler)

        # REMOVE ALLOWED USERS handler
        remove_users = CommandHandler('remove_allowed_user', command_handlers.remove_allowed_user)
        self.__application.add_handler(remove_users)
        self.__application.add_handler(CallbackQueryHandler(command_handlers.handle_remove_account_button))

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
