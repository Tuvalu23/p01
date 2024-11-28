'''
Team Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development - Global Bites
2024-11-27
Time Spent: 0.5
'''

import os

def read_key(keys_dir, file_name):
    key_path = os.path.join(keys_dir, file_name)
    try:
        with open(key_path, 'r') as key_file:
            return key_file.read().strip()
    except FileNotFoundError:
        print(f"Oh no! {file_name} not found in {keys_dir}.")  # displays error message if not found
        return None

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TopherSecret' # we might change later

    # keys directory
    KEYS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'keys')

    # API keys
    CALENDARIFIC_API_KEY = read_key(KEYS_DIR, 'key_calendarific.txt')
    SPOONACULAR_API_KEY = read_key(KEYS_DIR, 'key_spoonacular.txt')
    UNSPLASH_API_KEY = read_key(KEYS_DIR, 'key_unsplash.txt')
    GOOGLE_MAPS_API_KEY = read_key(KEYS_DIR, 'key_googlemaps.txt')

    # db configuration
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'site.db')
