from settings.settings import Settings

class BotSettings(Settings):
    def __init__(self):
        super().__init__('bot/config.json')

    def add_allowed_user(self, user):
        allowed_users = self.get_allowed_users()

        if user['id'] in allowed_users:
            return False

        allowed_users.append(user['id'])
        self._set_json_data_by_key('allowed_users_id', allowed_users)
        return True

    def get_allowed_users(self):
        allowed_users = self._get_from_json_file_by_key('allowed_users_id')
        return [] if allowed_users is None else allowed_users

    def remove_allowed_user(self, user_id, user_id_to_remove):
        allowed_users = self.get_allowed_users()

        if user_id_to_remove not in allowed_users:
            return False

        allowed_users.remove(user_id_to_remove)
        self._set_json_data_by_key('allowed_users_id', allowed_users)
        return True
