from telegram import Chat, Update
from .bot_settings import BotSettings

class UserService(object):
    __bot = None
    __settings = None

    def __init__(self, bot=None):
        if self.__bot is None and bot is not None:
            self.__bot = bot

        if self.__settings is None:
            self.__settings = BotSettings()

    async def __get_user_details(self, user_id):
        if not user_id or self.__bot is None:
            return None

        user = await self.__bot.get_chat(user_id)
        return user

    async def is_user_allowed(self, user_data):
        if not (user_object := await self.get_user_object(user_data)):
            return False

        user_id = user_object['id']
        allowed_users = self.__settings.get_allowed_users()

        return user_id in allowed_users

    async def get_user_object(self, data):
        if isinstance(data, Chat):
            return data
        elif isinstance(data, Update):
            user_id = data.message.from_user.id
            return await self.__get_user_details(user_id)
        elif isinstance(data, int):
            return await self.__get_user_details(data)
        else:
            return None
