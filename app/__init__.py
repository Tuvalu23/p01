'''
P01 - ArRESTed Development - Global Bites
Team Bareustoph
Members: Ben Rudinski, Tiffany Yang, Tim Ng, Endrit Idrizi
SoftDev
TARGET SHIP DATE: 2024-12-15
'''

from flask import Flask
from .config import Config

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Import routes
from . import routes

if __name__ == "__main__":
    app.run(debug=True)
