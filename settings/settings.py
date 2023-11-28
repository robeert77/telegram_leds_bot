from dotenv import load_dotenv, dotenv_values
import json

class Settings(object):
    __env_variables = None
    __json_data = None

    def __init__(self, json_file):
        if self.__env_variables is None:
            self.__load_env_file_content()

        self._json_file = json_file
        if Settings.__json_data is None:
            self._load_json_file_content()

    ''' ENV FILE - START '''

    def get_bot_token(self):
        return self._get_from_env_file_by_key('BOT_API_KEY')

    def _get_from_env_file_by_key(self, key):
        env_value = Settings.__env_variables.get(key)
        if not env_value:
            return None
        return env_value

    def __load_env_file_content(self):
        load_dotenv('../settings/.env')
        Settings.__env_variables = dotenv_values()

    ''' ENV FILE - END '''

    ''' JSON FILE - START '''

    def _get_from_json_file_by_key(self, key):
        if key not in Settings.__json_data:
            return None
        else:
            return Settings.__json_data[key]

    def _set_json_data_by_key(self, key, value):
        Settings.__json_data[key] = value
        self.__update_json_file_content()

    def _load_json_file_content(self):
        try:
            with open(self._json_file, 'r') as file:
                file_content = file.read()
                if not file_content:
                    print(f"Warning: File '{self._json_file}' is empty.")
                    Settings.__json_data = {}
                else:
                    Settings.__json_data = json.loads(file_content)
        except FileNotFoundError:
            print(f"Error: File '{self._json_file}' not found.")
            Settings.__json_data = {}
        except json.JSONDecodeError:
            print(f"Error: File '{self._json_file}' contains invalid JSON.")
            Settings.__json_data = {}

    def __update_json_file_content(self):
        with open(self._json_file, 'w') as file:
            json.dump(Settings.__json_data, file, indent=2)

    ''' JSON FILE - END '''
