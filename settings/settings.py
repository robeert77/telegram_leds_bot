from dotenv import load_dotenv, dotenv_values
import json

class Settings(object):
    __env_variables = None
    
    _instance = None

    def __init__(self, json_file=None):
        self._json_file = json_file
        self.__json_data = self._load_json_file_content()

        if not self.__env_variables:
            self.__env_variables = self.__load_env_file_content()

    ''' ENV FILE - START '''

    def get_bot_token(self):
        return self._get_from_env_file_by_key('BOT_API_KEY')

    def _get_from_env_file_by_key(self, key):
        env_value = self.__env_variables.get(key)
        if not env_value:
            return None
        return env_value

    def __load_env_file_content(self):
        load_dotenv('../settings/.env')
        return dotenv_values()

    ''' ENV FILE - END '''

    ''' JSON FILE - START '''

    def _get_from_json_file_by_key(self, key):
        if key not in self.__json_data:
            return None
        else:
            return self.__json_data[key]

    def append_to_array(self, key, value):
        if key not in self.__json_data:
            self.__json_data[key] = []

        self.__json_data[key].append(value)
        self.__update_json_file_content()

    def add_to_key(self, key, value):
        self.__json_data[key] = value
        self.__update_json_file_content()

    def remove_from_key(self, key): 
        if key not in self.__json_data:
            return True
    
        del self.__json_data[key]

    def remove_from_array(self, key, value):
        if key not in self.__json_data:
            return True
        
        if value not in self.__json_data[key]:
            return True
            
        self.__json_data[key].remove(value)
        self.__update_json_file_content()

    def _set_json_data_by_key(self, key, value):
        self.__json_data[key] = value
        self.__update_json_file_content()

    def _load_json_file_content(self):
        try:
            with open(self._json_file, 'r') as file:
                file_content = file.read()
                if not file_content:
                    print(f"Warning: File '{self._json_file}' is empty.")
                    return {}
                else:
                    return json.loads(file_content)
        except FileNotFoundError:
            print(f"Error: File '{self._json_file}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: File '{self._json_file}' contains invalid JSON.")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred while loading the JSON file: {e}")
            return {}

    def __update_json_file_content(self):
        with open(self._json_file, 'w') as file:
            json.dump(self.__json_data, file, indent=2)

    ''' JSON FILE - END '''
