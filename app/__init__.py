'''
Team Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development - Global Bites
2024-11-27
Time Spent: 3
'''
# imports
import os, sys

import urllib.parse  # for URL decoding
import sqlite3
import requests
import datetime # for calendarific dates
import calendar  # for month/calendar operations

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dateutil.parser import parse  # import for ISO 8601 parsing (for dates)
from functools import wraps
from models import User  # import User model from models.py
from calendar import monthrange, day_name

from config import Config

# adding config.py to search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# flask app initializing
app = Flask(__name__)
app.config.from_object(Config)

COUNTRY_INGREDIENT_MAP = {
    "Italy": ["pasta", "tomatoes", "basil", "parmesan", "olive oil", "risotto"],
    "France": ["baguette", "cheese", "wine", "herbs de Provence", "butter", "truffles"],
    "China": ["dumplings", "soy sauce", "ginger", "bok choy", "Sichuan peppercorn", "hoisin sauce"],
    "Japan": ["miso", "sushi", "wasabi", "soy sauce", "matcha", "nori", "dashi"],
    "India": ["curry", "cumin", "turmeric", "cardamom", "lentils", "ghee", "paneer"],
    "Mexico": ["adobo", "tortilla", "chili peppers", "avocado", "cilantro", "lime", "cacao"],
    "Thailand": ["lemongrass", "coconut milk", "chili", "fish sauce", "kaffir lime leaves", "galangal"],
    "Spain": ["paella", "saffron", "chorizo", "manchego cheese", "jamón ibérico", "olive oil"],
    "Greece": ["feta", "olives", "lemon", "oregano", "yogurt", "honey", "lamb"],
    "USA": ["hamburger", "barbecue sauce", "maple syrup", "corn", "potatoes", "apple pie"],
    "Brazil": ["cassava", "black beans", "palm oil", "picanha", "passion fruit"],
    "Vietnam": ["pho", "fish sauce", "rice noodles", "mint", "lemongrass", "banh mi"],
    "Turkey": ["kebab", "eggplant", "sumac", "pomegranate", "yogurt"],
    "Germany": ["bratwurst", "sauerkraut", "beer", "mustard", "pretzels", "potatoes"],
    "Morocco": ["couscous", "preserved lemon", "harissa", "ras el hanout", "mint", "dates"],
    "South Korea": ["kimchi", "gochujang", "sesame oil", "rice", "bulgogi", "seaweed"],
    "Peru": ["ceviche", "potatoes", "aji peppers", "corn", "lime", "quinoa"],
    "Argentina": ["chimichurri", "malbec wine", "dulce de leche", "empanadas", "asado", "mate"],
    "Nigeria": ["yam", "plantain", "egusi", "pepper soup", "palm oil", "okra"],
    "Ethiopia": ["berbere spice", "chickpeas", "teff", "lentils", "doro wat"],
    "Albania": ["feta cheese", "honey", "olive oil", "grape raki"]
}

CUISINE_MAP = {
    "India": "Indian",
    "USA": "American",
    "Italy": "Italian",
    "France": "French",
    "China": "Chinese",
    "Japan": "Japanese",
    "Mexico": "Mexican",
    "Thailand": "Thai",
    "Spain": "Spanish",
    "Greece": "Greek",
    "Brazil": "Latin American",
    "Vietnam": "Vietnamese",
    "Turkey": "Mediterranean",
    "Germany": "German",
    "Morocco": "Moroccan",
    "South Korea": "Korean",
    "Peru": "Latin American", 
    "Argentina": "Latin American",
    "Nigeria": "African",
    "Ethiopia": "African",
    "Albania": "Mediterranean"
}

# map of country names to Calendarific country codes:
COUNTRY_CODE_MAP = {
    "Italy": "IT",
    "France": "FR",
    "China": "CN",
    "Japan": "JP",
    "India": "IN",
    "Mexico": "MX",
    "Thailand": "TH",
    "Spain": "ES",
    "Greece": "GR",
    "USA": "US",
    "Brazil": "BR",
    "Vietnam": "VN",
    "Turkey": "TR",
    "Germany": "DE",
    "Morocco": "MA",
    "South Korea": "KR",
    "Peru": "PE",
    "Argentina": "AR",
    "Nigeria": "NG",
    "Ethiopia": "ET",
    "Albania": "AL"
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
    cuisine = CUISINE_MAP.get(country_name, None)
    if not cuisine:
        cuisine = country_name  # fallback to country name if mapping not found
    
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
    
# holiday section

def get_upcoming_holidays(country_name):
    api_key = app.config.get('CALENDARIFIC_API_KEY')
    if not api_key:
        # no key
        return []
    
    country_code = COUNTRY_CODE_MAP.get(country_name)
    # get current date and the next 2 months maybe
    today = datetime.date.today()
    current_year = today.year
    
    # fetch holidays for current year and next year
    holidays = []
    for year in [current_year, current_year+1]:
        url = "https://calendarific.com/api/v2/holidays"
        params = {
            'api_key': api_key,
            'country': country_code,
            'year': year
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                for hol in data.get('response', {}).get('holidays', []):
                    # parse date
                    date_str = hol['date']['iso']
                    hol_date = datetime.date.fromisoformat(date_str)
                    # only upcoming holidays
                    if hol_date >= today:
                        holidays.append({
                            'name': hol['name'],
                            'description': hol.get('description', ''),
                            'date': hol_date.isoformat()
                        })
        except Exception as e:
            print("Error fetching holidays:", e)
            
    # sort holidays by date
    holidays.sort(key=lambda h: h['date'])
    return holidays

# get all rcipes for current monrth globally (for home calendar)
def get_holidays_this_month():
    api_key = app.config.get('CALENDARIFIC_API_KEY')
    if not api_key:
        print("Error: Calendarific API key not configured.")
        return {}, None, None, None

    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    month_name = calendar.month_name[current_month]

    # find first and last day of the current month
    first_day = datetime.date(current_year, current_month, 1)
    _, num_days = calendar.monthrange(current_year, current_month)
    last_day = datetime.date(current_year, current_month, num_days)

    holidays_by_date = {}

    # loop thru all countries
    for country_name, country_code in COUNTRY_CODE_MAP.items():
        url = "https://calendarific.com/api/v2/holidays"
        params = {
            "api_key": api_key,
            "country": country_code,
            "year": current_year,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # parsin/using params
            if isinstance(data, dict) and "response" in data and "holidays" in data["response"]:
                for holiday in data["response"]["holidays"]:
                    holiday_date = holiday["date"]["iso"]  # ISO 8601 string
                    try:
                        d = parse(holiday_date).date()  # use dateutil to parse date
                        if first_day <= d <= last_day:
                            name = holiday["name"]
                            if d.isoformat() not in holidays_by_date:
                                holidays_by_date[d.isoformat()] = []
                            holidays_by_date[d.isoformat()].append(f"{name} ({country_name})")
                    except ValueError as ve:
                        print(f"Invalid date format for {holiday_date}: {ve}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching holidays for {country_name}: {e}")

    return holidays_by_date, current_year, current_month, month_name

# routes
@app.route('/') # home page route
def home():
    user = None
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
    #maps api key
    google_maps_api_key = app.config['GOOGLE_MAPS_API_KEY']
    calendarific_api_key = app.config['CALENDARIFIC_API_KEY']
    
    holidays_by_date, current_year, current_month, month_name = get_holidays_this_month()
    
    # generate calendar data
    days_in_month = monthrange(current_year, current_month)[1]  # total days in the month
    first_day_of_month = monthrange(current_year, current_month)[0]  # day of the week (0 = Monday)
    
    return render_template(
        'home.html',
        google_maps_api_key=google_maps_api_key,
        holidays_by_date=holidays_by_date,
        current_year=current_year,
        current_month=current_month,
        month_name=month_name,
        days_in_month=days_in_month,
        first_day_of_month=first_day_of_month
    )

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
    
    # fetch upcoming holidays
    holidays = get_upcoming_holidays(country_name)
    top_two_holidays = holidays[:2]
    
    # badges = get_badges_by_country(country_name)
    # forums = get_forums_by_country(country_name)
    
    # placeholders for now
    traditions = []
    badges = []
    forums = []
    
    return render_template('country.html', 
                          country_name=country_name, recipes=top_two, traditions=traditions, badges=badges, forums=forums, country_image=country_image, holidays=top_two_holidays, has_more_recipes=(len(recipes)>2),  has_more_holidays=(len(holidays)>2))

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
    
# view all holidays for a country
@app.route('/country/<country_name>/holidays')
def country_holidays_all(country_name):
    country_name = urllib.parse.unquote(country_name)
    holidays = get_upcoming_holidays(country_name)
    return render_template('country_holidays_all.html', country_name=country_name, holidays=holidays)

# view single holiday
@app.route('/country/<country_name>/holiday/<int:holiday_index>')
def holiday_page(country_name, holiday_index):
    country_name = urllib.parse.unquote(country_name)
    holidays = get_upcoming_holidays(country_name)
    if holiday_index < 0 or holiday_index >= len(holidays):
        flash("Holiday not found.", "warning")
        return redirect(url_for('country_page', country_name=country_name))
    holiday = holidays[holiday_index]
    return render_template('holiday.html', country_name=country_name, holiday=holiday)

@app.route('/recipes')
def allRecipes():
    CountryList = ['India', 'USA', 'Italy', 'France', 'China', 'Japan', 'Mexico', 'Thailand', 'Spain', 'Greece', 'Brazil', 'Vietnam', 'Turkey', 'Germany', 'Morocco', 'South Korea', 'Peru', 'Argentina', 'Nigeria', 'Ethopia', 'Albania']
    AllRecipesList = []
    for x in CountryList:
        AllRecipesList = AllRecipesList + (get_country_recipes(x))
    return render_template('all_recipes.html', recipes = AllRecipesList)

@app.route('/holidays')
def allHolidays():
    today = datetime.date.today()
    api_key = app.config.get('CALENDARIFIC_API_KEY')
    if not api_key:
        flash("Calendarific API key not configured.", "danger")
        return render_template('all_holidays.html', holidays=[])

    all_holidays = []
    for country_name, country_code in COUNTRY_CODE_MAP.items():
        url = "https://calendarific.com/api/v2/holidays"
        params = {
            'api_key': api_key,
            'country': country_code,
            'year': today.year
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # checks for HTTP errors
            data = response.json()
            for hol in data.get('response', {}).get('holidays', []):
                hol_date = datetime.date.fromisoformat(hol['date']['iso'])
                if hol_date >= today:  # only include upcoming holidays
                    all_holidays.append({
                        'name': hol['name'],
                        'country': country_name,
                        'date': hol_date
                    })
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching holidays for {country_name}: {e}")
        except Exception as e:
            print(f"Unexpected error fetching holidays for {country_name}: {e}")

    # sort holidays by date
    all_holidays.sort(key=lambda h: h['date'])
    return render_template('all_holidays.html', holidays=all_holidays)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


def limited_flash(message, category=""):
    if "flashed_messages" not in session:
        session["flashed_messages"] = []
    if len(session["flashed_messages"]) < 3:
        session["flashed_messages"].append((message, category))
    else:
        session["flashed_messages"].pop(0)
        session["flashed_messages"].append((message, category))
    for msg, cat in session["flashed_messages"]:
        flash(msg, cat)



if __name__ == "__main__":
    app.run(debug=True)
