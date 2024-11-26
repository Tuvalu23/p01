'''
Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development
2024-11-26
Time Spent: .2
'''

#imports
from flask inmport Flask
import os

class Config:
    # secret key for securely handling sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TopherBrown'
    DATABASE_PATH = os.path.join(os.getcwd(), 'site.db') # set db path
    
# flask app
app = Flask(__name__)
app.config.from_object(Config)

if __name__ == "__main__":
    app.run(debug=True)
    
