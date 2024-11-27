'''
Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development
2024-11-26
Time Spent: .5
'''

#imports
from flask import Flask
from .config import Config
    
# flask app
app = Flask(__name__)
app.config.from_object(Config)

from . import routes 

if __name__ == "__main__":
    app.run(debug=True)
    
