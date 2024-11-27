import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TopherBrown'

    # path to keys directory
    KEYS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'keys')

    # read the keys from text files
    @staticmethod
    def read_key(file_name):
        key_path = os.path.join(Config.KEYS_DIR, file_name)
        try:
            with open(key_path, 'r') as key_file:
                return key_file.read().strip()
        except FileNotFoundError:
            print(f"Oh No! {file_name} not found in {Config.KEYS_DIR}.") # error msg if not found
            return None
    
    # api keys
    CALENDARIFIC_API_KEY = read_key('key_calendarific.txt')
    SPOONACULAR_API_KEY = read_key('key_spoonacular.txt')
    UNSPLASH_API_KEY = read_key('key_unsplash.txt')
    # GOOGLE_MAPS_KEY = read_key('key_googlemaps.txt') (still have to get)

     # db config
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'site.db')