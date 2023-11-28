from telegram import Chat, Update
from .bot_settings import BotSettings

class UserService(object):
    __bot = None
    __settings = None

    def __init__(self, bot=None):
        if UserService.__bot is None and bot is not None:
            UserService.__bot = bot

        if UserService.__settings is None:
            UserService.__settings = BotSettings()

    async def __get_user_details(self, user_id):
        if not user_id or UserService.__bot is None:
            return None

        user = await UserService.__bot.get_chat(user_id)
        return user

    async def __get_user_dictionary(self, user_data):
        if not (user_object := await self.get_user_object(user_data)):
            return False

        full_name = user_object.first_name
        if user_object.last_name:
            full_name += ' ' + str(user_object.last_name)

        return {
            'id':           user_object.id,
            'first_name':   user_object.first_name.title(),
            'last_name':    str(user_object.last_name).title(),
            'full_name':    full_name.title(),
            'username':     user_object.username,
        }

    async def is_user_allowed(self, user_data):
        if not (user_object := await self.get_user_object(user_data)):
            return False

        user_id = user_object['id']
        allowed_users = UserService.__settings.get_allowed_users()

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

    async def get_allowed_users_list(self):
        allowed_users_id = UserService.__settings.get_allowed_users()
        allowed_users_arr = []
        for user_id in allowed_users_id:
            user_object = await self.__get_user_dictionary(user_id)
            allowed_users_arr.append(user_object)

        return allowed_users_arr
