'''
Team Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development - Global Bites
2024-11-27
Time Spent: 2
'''

# imports
import os, sys

# adding config.py to search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from functools import wraps
from models import User  # import User model from models.py
import urllib.parse  # for URL decoding

# flask app initializing
app = Flask(__name__)
app.config.from_object(Config)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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
            flash("Username already exists.", 'warning')
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


@app.route('/recipes/<int:recipe_id>')
def user_pages(user_id):
    if 'user_id' not in session:
        flash("You must be logged in to view user pages.")
        return redirect(url_for('login'))

    conn = get_db_connection()
# need code here
    conn.close()
    return render_template('recipes.html', pages=pages)

# countries
@app.route('/country/<country_name>')
def country_page(country_name):
    # decode country from URL
    country_name = urllib.parse.unquote(country_name)
    
    # here we will fetch data for country
    # like: (when db is set up and modesl)
    # recipes = get_recipes_by_country(country_name)
    # traditions = get_traditions_by_country(country_name)
    # badges = get_badges_by_country(country_name)
    # forums = get_forums_by_country(country_name)
    
    # placeholders for now
    recipes = []
    traditions = []
    badges = []
    forums = []
    
    return render_template('country.html', country_name=country_name, recipes=recipes, traditions=traditions, badges=badges, forums=forums)

if __name__ == "__main__":
    app.run(debug=True)