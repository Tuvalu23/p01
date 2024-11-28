'''
Team Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development - Global Bites
2024-11-27
Time Spent: 0.5
'''

# imports
from flask import Flask
from .config import Config

# flask app initializing
app = Flask(__name__)
app.config.from_object(Config)

# routes
from . import routes

if __name__ == "__main__":
    app.run(debug=True)
