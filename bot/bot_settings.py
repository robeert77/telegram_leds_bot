from settings.settings import Settings

class BotSettings(Settings):
    __instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(BotSettings, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, json_file='bot/config.json'):
        if not hasattr(self, 'initialized'):
            super().__init__(json_file)
            self.initialized = True

    def add_allowed_user(self, user):
        allowed_users = self.get_allowed_users()

        if user['id'] in allowed_users:
            return False

        self.append_to_array('allowed_users_id', user['id'])
        return True

    def get_allowed_users(self):
        allowed_users = self._get_from_json_file_by_key('allowed_users_id')
        return [] if allowed_users is None else allowed_users

    def remove_allowed_user(self, user_id, user_id_to_remove):
        allowed_users = self.get_allowed_users()

        if user_id_to_remove not in allowed_users:
            return False

        self.remove_from_array('allowed_users_id', user_id_to_remove)
        return True
