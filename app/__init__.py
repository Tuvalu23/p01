'''
Team Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development - Global Bites
2024-11-27
Time Spent: 0.5
'''

# imports
import os, sys

# adding config.py to search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template
from config import Config

# flask app initializing
app = Flask(__name__)
app.config.from_object(Config)

# routes
@app.route('/') # home page route
def home():
    #maps api key
    google_maps_api_key = app.config['GOOGLE_MAPS_API_KEY']
    return render_template('home.html', google_maps_api_key=google_maps_api_key)

if __name__ == "__main__":
    app.run(debug=True)
