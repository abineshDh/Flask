
# BASICS
# ====================================================================================================================================

# an object of Flask Class is our flask application
from flask import Flask

# Flask constructor takes the name current module (__name__) as an argument
# “Create a new Flask app, using the current file’s name as the reference point for locating templates and static files.”
app = Flask(__name__)


# ROUTE decorator
#==================

# Flask route decorator that tells Flask what URL should trigger a specific function. 
# # ‘/’ URL is bound with hello_world() function.
@app.route('/')
def home():
    return 'Hello World'

# /hello path binds hello function
@app.route("/hello")
def hello(name='Abinesh'):
    return f"Hello Mr. {name}"


# The add_url_rule() method in Flask is an alternative way to define a route, just like using the @app.route() decorator. 
# It lets you register a URL rule (route) manually.
# app.add_url_rule(rule, endpoint=None, view_func=None, **options)
# def home():
#     return 'Hello, World'
# app.add_url_rule('/', 'home', home)

# Dynamic variables in the decorator arguments
#==============================================

# Adding variables helps to create dynamic routes - based on different inputs,URLs, IDs
# instead of hardcoding use variable rules for dynamic contents
 
@app.route('/post/<int:id>') # int
def show_post(id): 
    # Shows the post with given id. 
    return f'This post has the id {id}'
  
@app.route('/user/<username>') # string
def show_user(username): 
    # Greet the user 
    return f'Hello {username} !'
  
# Pass the required route to the decorator. 
@app.route("/hello") # path
def hello(): 
    return "Hello, Welcome to WebApp"
    
@app.route("/") # index page
def index(): 
    return "Homepage of Flask WebApp"


# | Converter | Description                 | Example URL              |
# | --------- | --------------------------- | ------------------------ |
# | `string`  | (default) text              | `/user/<string:name>`    |
# | `int`     | Integers only               | `/post/<int:id>`         |
# | `float`   | Decimal numbers             | `/price/<float:amt>`     |
# | `path`    | Like string, allows slashes | `/files/<path:filename>` |
# | `uuid`    | UUID strings                | `/item/<uuid:uid>`       |

# Main function to run the flask app
#========================================

# main driver method - “Only run the following block if this file is being run directly — not imported as a module in another file.”
if __name__ == '__main__':
    app.run(debug=True) # to run in a debugger mode 
    
# HTTP - Methods
#============================================================================================================================

# HTTP is the data communication of the app, defines how the CLIENT(app browser) and SERVERS communicates
# using REQUESTS and RESPONSES
# Method – What action to perform (e.g., GET, POST)
# URL – What resource to access (/home, /user/1)
# Headers – Metadata (e.g., authentication, content type)
# Body – Data sent with the request (used with POST/PUT)

# GET -> to request a data from the server - used for READ the data
# POST -> to submit the data to the server - used to CREATE the resource for the data
# PUT -> replaces the entire resource with new data. If it doesn’t exist, a new one is created.- UPDATE the data 
# PATCH -> updates only the partial resource without altering the whole data - PARTIAL UPDATE the resource in the data
# DELETE -> deletes the data in the server at a specified location. - DELETE a data
 
# GET – Get blog posts, pages, or user info (safe & cacheable)
# POST – Sending forms or login info
# PUT – Updating profile or settings
# DELETE – Deleting posts or users
# HEAD – Check if resource exists before downloading

# GET - to get the data from server
from flask import Flask, request
app = Flask(__name__)

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    return f"Profile Page: {username}"

# POST - to send the data to server
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form['name']
    return f"Received submission from {data}"

# PUT - alters the data in the specified url
@app.route('/update/<username>', methods=['PUT'])
def update_user(username):
    new_name = request.form['Abinesh']
    return f"{username} updated to {new_name}"  

# DELETE - deletes the data in the specified url
@app.route('/delete/<username>', methods=['DELETE'])
def delete_user(username):
    return f"{username} has been deleted!"

# HEAD - checks the resource exists
@app.route('/check', methods=['HEAD'])
def check_header():
    return '', 200

# ============================================================================================================================
# The GET method 
# ========================
# GET methods is used to request data from a server. 
# It ends data to the URL in a name-value pair format. 
# GET should not be used for sensitive data since URLs are visible in browser history.

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/index", methods=['GET'])
def greet_user():
    name = request.args.get('username')
    if name:
        return f"<h2> Hello {name} </h2>"
    else:
        print('[INFO] No Name found!')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# Celcius to fahrenheit
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/index", methods=['GET'])
def calculate_temp():
    celcius = request.args.get('temp')
    if celcius is None:
        return render_template('index.html')
    elif celcius.strip() == "":
        return "<h2>Invalid input. Please enter a number.</h2>"
    try:
        celcius = float(celcius)
        fahrenheit = (celcius * 9 / 5) + 32
        return f"<h2>{celcius}°C = {fahrenheit}°F</h2>"
    except ValueError:
        return "<h2>Invalid input. Please enter a valid number.</h2>"
    
if __name__ == '__main__':
    app.run(debug=True)

# Simple Age Calculator
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/index", methods=['GET'])
def calculate_age():
    #get user input
    user_name = request.args.get('name')
    birth_year = request.args.get('year')
    # check if the value is empty
    if not user_name or not birth_year:
        return render_template("index.html")
    # check if the values are empty strings
    elif user_name.strip() == "" or birth_year.strip() == "":
        return f"<h2> Empty values, Please enter the value</h2>"
    # check username is alphabets
    elif not user_name.isalpha():
        return f"<h2> Username should be only alphabets"
    try:
        if birth_year:
            birth_year = int(birth_year)
            current_year = int(2025)
            age = current_year - birth_year
            return f"<h2> Hi, {user_name} ! Your Current Age is : {age}"
    except ValueError:
        return f"<h2> Invalid Input, Please Enter Numerical values"  
    
if __name__ == '__main__':
    app.run(debug=True)

# | Feature                 | GET Method                           |
# | ----------------------- | ------------------------------------ |
# | Data in URL             | ✅ Yes (query string)                 |
# | Safe for sensitive data | ❌ No                                 |
# | Length Limit            | ✅ Yes (URL length limit)             |
# | Server-side effects     | ❌ Should not modify data             |
# | Caching/Bookmarking     | ✅ Supported                          |
# | Used for                | ✅ Reading, searching, simple actions |

# ==========================================================================================================================
# POST Method
# =================

# POST method is used to send the data to the server for processing. 
# unlike GET method, it doesnot end data in the url.
# it sends data in the  request body for sensitive and large data for processing
# Use POST for: Login forms, Registration, Form submissions with private or large data

# | Feature    | GET                  | POST                   |
# | ---------- | -------------------- | ---------------------- |
# | Data type  | ended in URL         | Sent in request body   |
# | Visibility | Visible in URL       | Hidden from URL        |
# | Security   | Less secure          | More secure            |
# | Data size  | Limited (URL length) | Larger amounts allowed |
# | Use case   | Retrieve data        | Submit/update data     |

# Simple Login form
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/index", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password is None:
            return render_template('index.html')
        else:
            try:
                if username == "Admin" and password == "Admin123":
                    return f"<h2> Welcome {username} !</h2>"
                else:
                    return f"<h2>Invalid Credentials</h2>"
            except ValueError:
                return f"<h2> Username must be Strings and Numbers!"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

# Contact form 
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/contact', methods=['GET','POST'])
def contact_form():
    #check if the method is in post
    if request.method == 'POST':
        # capture all the user inputs
        fullname = request.form.get('fullname').strip().capitalize()
        email = request.form.get('email').strip()
        message = request.form.get('message').strip()
        # print inputs for debugging
        print([fullname])
        print([email])
        print([message])
        # check if the fields are not empty
        if fullname == "":
            return f"<h2> [ERROR] FullName Fields should not be Empty!"
        elif not fullname.replace(" ", "").isalpha():
            return "<h2>[ERROR] Full Name must contain only letters.</h2>"
        elif email == "":
            return f"<h2> [ERROR] Email Fields should not be Empty!"
        elif message == "":
            return f"<h2> [ERROR] Message Fields should not be Empty!"
        elif '@' not in email and '.' not in email:
            return f"<h2> [ERROR] Email should be in a valid format"
        elif len(message) <= 10:
            return f"<h2> [ERROR] Message should be 10 characters long"
        try: 
            if fullname and email and message:
                return f"<h2> Thanks, {fullname}! Your message has been sent. </h2>"
        except ValueError:
            return f"<h2>Invalid Input, Please Enter a valid Input </h2>"
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)


# ============================================================================================================
# PUT Method
# =========================
# Put method is used to change or replace the existing resource/data in the server
# send data in the body of the requests in formats like json, formdata

# updating whole resources(replacing all-data)
# ensuring updates are consistent
# REST API design

# update user profile
from flask import Flask, request, jsonify
app = Flask(__name__)

# Simulated database
users = {
    1: {"name": "Alice", "email": "alice@example.com"}
}

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Missing fields"}), 400

    users[user_id] = {"name": name, "email": email}
    return jsonify({"message": "User updated", "user": users[user_id]})

if __name__ == '__main__':
    app.run(debug=True)
    
# update a book title
from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

books = {
    1: {"title": "Old Man and the Sea"},
    2: {"title": "1984"}
}

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_title(book_id):
    # check if the book id exists
    if book_id not in books:
        return jsonify({"error" : 'book_id not found'}), 404
    # captures data in json using request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request must be in JSON format"}), 400
    title = data.get('title')
    # check if the title exits
    if not title:
        return jsonify({"error" : "Missing fields"}), 400
    try:
        books[book_id][title] = title
        return jsonify({'message' : 'books title updated'}), 200
    except:
        return jsonify({'error' : 'data not found'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)

# ==========================================================================================================================================
# PATCH method
# ============================

# PATCH - unlike PUT method, PATCH only updates partial resource in an existing resource

# partial update userId in users
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

users = {
    1: {"name": "Alice", "email": "alice@example.com"}
}

@app.route('/users/<int:user_id>')
def patch_user(user_id):
    if user_id not in users:
        return jsonify({'error' : 'user not found'}), 404
    data = request.get_json()
    users[user_id].update(data)
    return jsonify({ 'message' : 'user updated', 'user' : users[user_id]})

if __name__ == '__main__':
    app.run(debug=True)

# ==========================================================================================================================================
# DELETE method
# ============================

# DELETE method usually deletes a resource in the specified url

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

users = {
    1: {"name": "Alice", "email": "alice@example.com"}
}

@app.route('/user/<int:user_id>')
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error' : 'user not found'}), 404 
    data = request.get_json()
    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
    

# ==========================================================================================================================================
# HEAD method
# ============================ 

# HEAD is like a GET request, but it returns only the headers, not the response body.
# Useful for checking if a resource exists or for caching.

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/users/<int:user_id>', methods=['HEAD'])
def head_user(user_id):
    if user_id not in users:
        return "", 404
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)

# | Method   | Purpose                 | Returns Body? | Typical Use                   |
# | -------- | ----------------------- | ------------- | ----------------------------- |
# | `GET`    | Read resource           | Yes           | Display data                  |
# | `POST`   | Create new resource     | Yes           | Form submissions, new entries |
# | `PUT`    | Replace full resource   | Yes           | Update all fields             |
# | `PATCH`  | Update part of resource | Yes           | Update only certain fields    |
# | `DELETE` | Delete resource         | Optional      | Delete a user, item, etc.     |
# | `HEAD`   | Fetch headers only      | No            | Check existence, metadata     |
