from flask import Flask, redirect, url_for, flash, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# initialize flask app
app = Flask(__name__)
# connects to sqlite database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# disables unnecessary tracking information to improve performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# keeps session and user data safe
app.config['SECRET_KEY'] = 'HG2tJ89751CAA6251ATcgUp'

# initialize database and login manager 
db = SQLAlchemy(app) # define models (database tables) and interact with the database using Python.
login_manager = LoginManager() # manages user sessions - login, logout, restrict acess
login_manager.init_app(app) # manage user sessions - flasks request/response cycle
login_manager.login_view = 'login' # specifies users to redirected to login page - with login route using login_view function

# User Model
# -- db.Model : base class for SQLAlchemy used to define tables for database
# -- UserMixin : adds default method used for Flask-Login (is_autheticated, get_id)
class User(UserMixin, db.Model):
    # creates a column for id and make it unique for each user
    id = db.Column(db.Integer, primary_key=True)
    # create a column for username which stores string and make it unique for each user and cant be empty
    username = db.Column(db.String(250), unique=True, nullable=False)
    # create a column for password which stores as string and unique and cannot be empty
    password = db.Column(db.String(250), nullable=False)
    
# This initializes the database and creates all tables defined using models 
with app.app_context():
    db.create_all()

# Load user for Flask-login
# -- loads user from the user_id stored in session
@login_manager.user_loader
# function takes user_id and returns current_user object
def load_user(user_id):
    return User.query.get(int(user_id))

# redirect to register page
@app.route('/')
def home():
    return redirect('/register')

# Register route to add user to database and render signup page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # checks if username and password are present
        if not username or not password:
            return render_template('signup.html', error='username and password are required')
        # checks the database if the user has same username
        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error='Username already taken!')
        # hash the password to be secured
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # Creates a new databaser user object and appends it to Database Session and commits it
        new_user = User(username=username, password=hashed_password)          
        db.session.add(new_user)
        db.session.commit()
        # after registration user is redirected to login page
        return redirect(url_for('login'))
    return render_template('signup.html')

# Login route to enable user to login to the system and render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # check if username and password are present
        if not username or not password:
            return render_template('login.html', error='Username and password are required')
        # searches the database for a user with the entered username.
        user = User.query.filter_by(username=username).first()
        # checks whether username exists and check hashed password with entered password are correct
        if user and check_password_hash(user.password, password):
            # calls login_user function and logs the user in
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid Username or Password')
    return render_template('login.html')

# Protected dashboard route
@app.route("/dashboard")
# @login_required: You must be logged in or get redirected to login_view
@login_required
def dashboard():
    # current_user: Flask-Login provides this object globally
    return render_template("dashboard.html", username=current_user.username)

# Logout Route to end the session and redirect to home page/register
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # logout_user() clears the session. The user is no longer considered logged in.
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# | Feature            | Function                                  |
# | ------------------ | ----------------------------------------- |
# | `LoginManager`     | Manages login state, session, redirection |
# | `UserMixin`        | Gives your model required properties      |
# | `login_user(user)` | Logs in the user, stores session          |
# | `logout_user()`    | Logs out the user, clears session         |
# | `@login_required`  | Restricts access to logged-in users       |
# | `current_user`     | Gives access to the current user object   |


