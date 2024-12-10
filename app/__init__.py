'''
Team Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development - Global Bites
2024-11-27
Time Spent: 3
'''

# imports
import os, sys

# adding config.py to search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
from functools import wraps
from models import User  # import User model from models.py
import urllib.parse  # for URL decoding
import sqlite3
import requests

# flask app initializing
app = Flask(__name__)
app.config.from_object(Config)

COUNTRY_INGREDIENT_MAP = {
    "Italy": ["San Marzano tomatoes", "buffalo mozzarella", "parmigiano-reggiano", "arborio rice", "pancetta", "basil", "extra virgin olive oil", "balsamic vinegar"],
    "France": ["truffles", "foie gras", "camembert", "baguette", "dijon mustard", "herbes de Provence", "cognac", "crème fraîche"],
    "China": ["Sichuan peppercorns", "dried shiitake mushrooms", "Shaoxing wine", "Chinese chives", "dried tangerine peel", "fermented black beans", "star anise", "Pixian doubanjiang"],
    "Japan": ["kombu", "bonito flakes", "miso paste", "yuzu", "sake", "rice koji", "natto", "shiso leaves", "wakame seaweed"],
    "India": ["kashmiri red chili", "turmeric", "mustard seeds", "curry leaves", "asafoetida", "ghee", "cardamom", "tamarind", "urad dal"],
    "Mexico": ["dried ancho chiles", "epazote", "Mexican oregano", "piloncillo", "achiote paste", "nopales", "Mexican chocolate", "masa harina"],
    "Thailand": ["kaffir lime leaves", "Thai bird's eye chili", "galangal", "palm sugar", "fish sauce", "holy basil", "lemongrass", "shrimp paste"],
    "Spain": ["saffron", "pimentón", "manchego cheese", "jamón ibérico", "chorizo", "espelette pepper", "marcona almonds", "sherry vinegar"],
    "Greece": ["feta PDO", "kalamata olives", "oregano", "ouzo", "Greek yogurt", "phyllo pastry", "sumac", "mastiha"],
    "USA": ["maple syrup", "bourbon", "wild rice", "sourdough starter", "dried cranberries", "pecans", "blue crab", "cornmeal"],
    "Brazil": ["cassava flour", "dendê oil", "cachaça", "guaraná", "hearts of palm", "pequi fruit", "urucum", "açaí"],
    "Vietnam": ["fish sauce", "rice paper", "Vietnamese cinnamon", "perilla leaves", "bird's eye chili", "Vietnamese mint", "palm sugar", "rice paddy herb"],
    "Turkey": ["sumac", "urfa biber", "pomegranate molasses", "bulgur wheat", "tahini", "Turkish pepper", "grape leaves", "nigella seeds"],
    "Germany": ["speck", "rye flour", "quark", "juniper berries", "caraway seeds", "lebkuchen spices", "German mustard", "white asparagus"],
    "Morocco": ["preserved lemons", "ras el hanout", "harissa", "argan oil", "dried rose petals", "filo pastry", "baharat spice blend", "orange blossom water"],
    "South Korea": ["gochugaru", "gochujang", "doenjang", "kimchi", "perilla oil", "Korean pear", "Korean red pepper paste", "gim (seaweed)"],
    "Peru": ["aji amarillo", "pisco", "quinoa", "purple corn", "lucuma", "huacatay", "coca leaves", "cancha (corn nuts)"],
    "Argentina": ["yerba mate", "chimichurri spices", "dulce de leche", "Argentine beef", "quince paste", "Argentine wine", "chili pepper", "Argentine oregano"],
    "Nigeria": ["palm oil", "egusi seeds", "kola nuts", "scotch bonnet peppers", "suya spice", "locust beans", "yam flour", "ogbono seeds"],
    "Ethiopia": ["berbere spice", "teff flour", "wat spice blend", "injera sourdough", "shiro powder", "mitmita spice", "gesho leaves", "korarima"],
    "Albania": ["raki", "white cheese", "olive oil", "mountain herbs", "bean paste", "cornmeal", "walnuts", "sage"]
}

CUISINE_MAP = {
    "India": "Indian curry,North Indian,South Indian,Punjabi",
    "USA": "American,Southern American,Midwest American,BBQ",
    "Italy": "Tuscan,Sicilian,Northern Italian,Roman,Italian regional",
    "France": "Provençal,Burgundian,Parisian,French regional cuisine",
    "China": "Sichuan,Cantonese,Hunan,Beijing,Shanghai,Xinjiang cuisine",
    "Japan": "Kaiseki,Washoku,Okinawan,Hokkaido regional",
    "Mexico": "Yucatan,Oaxacan,Pueblan,Mexican regional",
    "Thailand": "Thai street food,Northeastern Thai,Southern Thai,Bangkok cuisine",
    "Spain": "Catalan,Basque,Andalusian,Valencian",
    "Greece": "Cretan,Macedonian,Ionian,Greek island cuisine",
    "Brazil": "Bahian,Amazonian,Minas Gerais,Gaucho cuisine",
    "Vietnam": "Northern Vietnamese,Southern Vietnamese,Central Vietnamese",
    "Turkey": "Ottoman,Anatolian,Mediterranean Turkish,Black Sea cuisine",
    "Germany": "Bavarian,Swabian,Saxon,Rhineland cuisine",
    "Morocco": "Berber,Coastal Moroccan,Imperial city cuisine",
    "South Korea": "Korean BBQ,Jeju Island,Pyongyang-style,Temple cuisine",
    "Peru": "Andean,Coastal Peruvian,Amazonian Peruvian",
    "Argentina": "Patagonian,Buenos Aires,Northwest Argentine",
    "Nigeria": "Yoruba,Igbo,Northern Nigerian,Lagos street food",
    "Ethiopia": "Amhara,Oromo,Ethiopian Orthodox cuisine",
    "Albania": "Northern Albanian,Southern Albanian,Coastal Albanian"
}

# connect to db
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'thread.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#recipe stuff

#make sure recipe is in tables if not exist
def ensure_recipe_in_db(recipe):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT recipe_id FROM Recipes WHERE recipe_id = ?", (recipe['id'],))
    row = cur.fetchone()
    
    if not row:
        # insert basic info now, instructions can be fetched on recipe detail page if needed
        cur.execute("""
            INSERT INTO Recipes (recipe_id, title, image_url)
            VALUES (?, ?, ?)
        """, (recipe['id'], recipe['title'], recipe['image']))
        # also create entry in RecipeVotes sql table
        cur.execute("""
            INSERT INTO RecipeVotes (recipe_id) VALUES (?)
        """, (recipe['id'],))
        conn.commit()
    conn.close() # clse our beautiful db
    

# fetch spoonacular by searching a key ingredient/proxy
def get_country_recipes(country_name):
    api_key = app.config['SPOONACULAR_API_KEY']
    if not api_key:
        print("Error: SPOONACULAR_API_KEY not found.")
        return []
    
    # map country to cuisine
    cuisines = CUISINE_MAP.get(country_name, None)
    if not cuisines:
        cuisines = country_name  # fallback to country name if mapping not found
    
    cuisine = cuisines.split(",")[0] if "," in cuisines else cuisines
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        'cuisine': cuisine,
        'number': 10,
        'apiKey': api_key,
        'addRecipeInformation': True,
        'ranking': 1  # prefer relevance
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        results = data.get('results', [])
        
        recipes = []
        for recipe in results:
            ensure_recipe_in_db(recipe)
            upvotes, downvotes = get_recipe_votes(recipe['id'])
            recipes.append({
                "id": recipe['id'],
                "title": recipe['title'],
                "image": recipe.get('image'),
                "upvotes": upvotes,
                "downvotes": downvotes
            })
        
        # sort recipes by (upvotes - downvotes) descending
        recipes.sort(key=lambda r: r['upvotes'] - r['downvotes'], reverse=True)
        return recipes
    except Exception as e:
        print(f"Error fetching recipes: {e}")
        return []

    
# detailed recipe info
def get_recipe_details(recipe_id):
    api_key = app.config['SPOONACULAR_API_KEY']
    
    if not api_key:
        # fallback: just return from DB if we have it
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Recipes WHERE recipe_id = ?", (recipe_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                'id': row['recipe_id'],
                'title': row['title'],
                'image': row['image_url'],
                'instructions': row['instructions'],
                'ingredients': row['ingredients']
            }
        return None

    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {'apiKey': api_key}
    try:
        r = requests.get(url, params=params)
        data = r.json()

        # ubdate DB with instructions and ingredients if available
        instructions = data.get('instructions', '')
        # ingredients: join ingredient names
        ing_list = [ing['original'] for ing in data.get('extendedIngredients', []) if 'original' in ing]
        ingredients = '\n'.join(ing_list)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Recipes SET instructions = ?, ingredients = ?, title = ?, image_url = ?
            WHERE recipe_id = ?
        """, (instructions, ingredients, data.get('title', ''), data.get('image', ''), recipe_id))
        conn.commit()
        conn.close()

        return {
            'id': data['id'],
            'title': data['title'],
            'image': data['image'],
            'instructions': instructions,
            'ingredients': ingredients
        }
    except:
        return None
    
# fetc unsplash image based on country name
def get_country_image(country_name):
    api_key = app.config['UNSPLASH_API_KEY']
    if not api_key:
        # no key
        return None
    
    url = "https://api.unsplash.com/search/photos"
    params = {
        'query': country_name,
        'per_page': 1,
        'client_id': api_key
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['urls']['regular']
        else:
            return None
    except:
        return None
    
# get updvotes/downvotes for each recipe
def get_recipe_votes(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT upvotes, downvotes FROM RecipeVotes WHERE recipe_id = ?", (recipe_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0], row[1]
    return (0,0)

# see what a user votes
def get_user_vote_for_recipe(user_id, recipe_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT vote FROM UserRecipeVotes WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0] # 1 for upvote, -1 for downvote
    return 0

def set_user_vote(user_id, recipe_id, vote):
    # vote = 1 (up), -1 (down), 0 (remove)
    conn = get_db_connection()
    cur = conn.cursor()
    # check if user has a vote
    cur.execute("SELECT vote FROM UserRecipeVotes WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
    existing = cur.fetchone()
    if existing:
        if vote == 0:
            cur.execute("DELETE FROM UserRecipeVotes WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
        else:
            cur.execute("UPDATE UserRecipeVotes SET vote = ? WHERE user_id = ? AND recipe_id = ?", (vote, user_id, recipe_id))
    else:
        if vote != 0:
            cur.execute("INSERT INTO UserRecipeVotes (user_id, recipe_id, vote) VALUES (?, ?, ?)", (user_id, recipe_id, vote))
    conn.commit()
    conn.close()

def update_recipe_votes(recipe_id, upvote_change=0, downvote_change=0):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT upvotes, downvotes FROM RecipeVotes WHERE recipe_id = ?", (recipe_id,))
    row = cur.fetchone()
    if row:
        upvotes = row[0] + upvote_change
        downvotes = row[1] + downvote_change
        cur.execute("UPDATE RecipeVotes SET upvotes = ?, downvotes = ? WHERE recipe_id = ?", (upvotes, downvotes, recipe_id))
        conn.commit()
    conn.close()

# routes
@app.route('/') # home page route
def home():
    user = None
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
    #maps api key
    google_maps_api_key = app.config['GOOGLE_MAPS_API_KEY']
    return render_template('home.html', google_maps_api_key=google_maps_api_key)

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        if user and user.verify_password(user.password_hash, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # password validation (server-side)
        errors = []
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if len(password) < 12:
            errors.append("Password must be at least 12 characters long.")
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter.")
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number.")
        if not any(c.isalpha() for c in password):
            errors.append("Password must contain at least one letter.")

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('register'))

        if User.get_by_username(username):
            flash("Username already exists.", 'danger')
            return redirect(url_for('register'))

        User.create(username, password)
        flash("Account created! Log in now.", 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", 'info')
    return redirect(url_for('home'))

# profile route
@login_required
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile.', 'warning')
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    return render_template('profile.html', user=user)

# profile settings
@login_required
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user = User.get_by_id(session['user_id'])
    
    if request.method == 'POST':
        # get form data
        current_password = request.form.get('currentPassword')
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')

        # validate current password
        if not user.verify_password(user.password_hash, current_password):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('settings'))

        #if new pw = current pw
        if new_password == current_password:
            flash('New password is the same as the old one.', 'error')
            return redirect(url_for('settings'))

        # validate new password and confirmation
        if new_password != confirm_password:
            flash('New password and confirmation do not match.', 'error')
            return redirect(url_for('settings'))

        # update the password securely
        user.set_password(new_password) 
        flash('Your password has been successfully updated.', 'success')
        return redirect(url_for('settings'))

    return render_template('settings.html', user=user)

# reauthentication for settings page
@app.route('/reauthenticate', methods=['GET', 'POST'])
def reauthenticate():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        if user and user.verify_password(user.password_hash, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('settings'))
        else:
            flash("Invalid username or password.", "danger")
    return render_template('reauthenticate.html')

# countries
@app.route('/country/<country_name>')
def country_page(country_name):
    country_name = urllib.parse.unquote(country_name)
    recipes = get_country_recipes(country_name)
    top_two = recipes[:2] # display top two recipes on country page
    country_image = get_country_image(country_name) # add pngs for countries maybe??
    
    # here we will fetch data for country
    # like: (when db is set up and modesl)
    # traditions = get_traditions_by_country(country_name)
    # badges = get_badges_by_country(country_name)
    # forums = get_forums_by_country(country_name)
    
    # placeholders for now
    traditions = []
    badges = []
    forums = []
    
    return render_template('country.html', 
                          country_name=country_name, recipes=top_two, traditions=traditions, badges=badges, forums=forums, country_image=country_image, has_more_recipes=(len(recipes)>2))

# route for viewing all recipes for country
@app.route('/country/<country_name>/recipes')
def country_recipes_all(country_name):
    country_name = urllib.parse.unquote(country_name)
    recipes = get_country_recipes(country_name)
    return render_template('country_recipes_all.html', country_name=country_name, recipes=recipes)
    
@app.route('/country/<country_name>/recipe/<int:recipe_id>')
def recipe_page(country_name, recipe_id):
    country_name = urllib.parse.unquote(country_name)
    recipe_details = get_recipe_details(recipe_id)
    if not recipe_details: # cannt find stuff
        flash("Could not fetch recipe details.", "warning")
        return redirect(url_for('country_page', country_name=country_name))

    upvotes, downvotes = get_recipe_votes(recipe_id)
    current_vote = None
    if 'user_id' in session:
        user_vote = get_user_vote_for_recipe(session['user_id'], recipe_id)
        if user_vote == 1:
            current_vote = 'up'
        elif user_vote == -1:
            current_vote = 'down'
    
    return render_template('recipe.html', country_name=country_name, recipe=recipe_details,upvotes=upvotes,downvotes=downvotes, current_vote=current_vote)

@app.route('/country/<country_name>/recipe/<int:recipe_id>/vote', methods=['POST'])
def vote_recipe(country_name, recipe_id):
    action = request.form.get('action')
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to access this page.", "warning")
        return jsonify({"error": "User not authenticated"}), 403
    
    current_vote = get_user_vote_for_recipe(user_id, recipe_id)
    # current_vote: 0=no vote, 1=upvoted, -1=downvoted
        
    if not action:
        return {"error": "No action provided."}, 400
    
    if action == 'upvote':
        # if currently no vote, add an upvote
        if current_vote == 0:
            update_recipe_votes(recipe_id, upvote_change=1)
            set_user_vote(user_id, recipe_id, 1)
            current_vote = 1
        # if currently upvote, remove it
        elif current_vote == 1:
            update_recipe_votes(recipe_id, upvote_change=-1)
            set_user_vote(user_id, recipe_id, 0)
            current_vote = 0
        # if currently downvote, remove downvote and add upvote
        elif current_vote == -1:
            update_recipe_votes(recipe_id, upvote_change=1, downvote_change=-1)
            set_user_vote(user_id, recipe_id, 1)
            current_vote = 1
            
            
    elif action == 'downvote':
        # if currently no vote, add a downvote
        if current_vote == 0:
            update_recipe_votes(recipe_id, downvote_change=1)
            set_user_vote(user_id, recipe_id, -1)
            current_vote = -1
        # if currently downvote, remove it
        elif current_vote == -1:
            update_recipe_votes(recipe_id, downvote_change=-1)
            set_user_vote(user_id, recipe_id, 0)
            current_vote = 0
        # if currently upvote, remove upvote and add downvote
        elif current_vote == 1:
            update_recipe_votes(recipe_id, upvote_change=-1, downvote_change=1)
            set_user_vote(user_id, recipe_id, -1)
            current_vote = -1
    else:
        return {"error": "Invalid action."}, 400
    upvotes, downvotes = get_recipe_votes(recipe_id)  # fetch updated counts
    return jsonify({
        "upvotes": upvotes,
        "downvotes": downvotes,
        "current_vote": "up" if current_vote == 1 else ("down" if current_vote == -1 else None)
    }), 200

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)