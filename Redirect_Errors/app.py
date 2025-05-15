# REDIRECTION IN URL
#=====================================================================
# -- flask app sends the user from one url to another
# Navigating users after form submission.
# Redirecting from an old route to a new one.
# Conditionally sending users to different pages (admin vs guest).    

# redirect(location, code=302)      

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/hello')  

@app.route('/hello')
def hello(name='Abinesh'):
    return f"<h2> Hello {name} from Redirected Page"  

if __name__ == '__main__':
    app.run(debug=True)  
    
    
# url_for() -> instead of hardcoding using url_for() method in flask
# It maps to a function name (not a string path).
# Automatically builds URLs and handles changes easily.                                                     

# url_for('function', **args)

@app.route('/admin')
def admin_login():
    return f"<h2> Hello Admin, You are logged in as Admin! </h2>"

@app.route('/guest/<guest>')
def guest_login(guest):
    return f"<h2> Hello {guest}, You are logged in as Guest!"

@app.route('/user/<user>')
def login_user(user):
    if user == 'admin':
        return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('guest_login', guest=user))
    
if __name__ == '__main__':
    app.run(debug=True)

# | Code | Meaning            | Use Case                                 |
# | ---- | ------------------ | ---------------------------------------- |
# | 301  | Moved Permanently  | Redirect when a page has moved           |
# | 302  | Found (default)    | Temporary redirect (most common)         |
# | 303  | See Other          | For redirects after POST                 |
# | 307  | Temporary Redirect | Same as 302 but with method preservation |

# When to Use Redirects in Flask?
#     ✅ After login, redirect to dashboard.
#     ✅ After form submit, redirect to prevent re-submitting.
#     ✅ Redirect based on roles (admin vs guest).
#     ✅ Redirect to updated URLs for deprecated routes.

#  When to Use Each                                                            
#     🔸 Use url_for() when:                                                            
#         You want to generate internal URLs safely and dynamically.                                                            
#         You don't want to hardcode URLs (safer for refactoring).                                                            
#         You are linking to a route in HTML templates or Python code.                                                            
#     🔸 Use redirect() when:                                                            
#         You want to actually redirect the client (change the browser location).                                                            
#         Usually used after a form submission, login, logout, etc.                                                            

# login using redict and url_for()
@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')       
        if not username:
            return "<h2>[ERROR] Username cannot be empty!</h2>"
        if username.lower() == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('guest_login', username=username))
    return render_template('index.html')      

@app.route('/admin_dashboard')
def admin_dashboard():
    return f"<h2> Welcome, Admin </h2>"

@app.route('/user/<username>')
def guest_login(username):
    return f"<h2> Hello {username}, You are logged in Guest!"

if __name__ == '__main__':
    app.run(debug=True)
    
# | Code    | Name                             | Description                                                                                                                                                               |
# | ------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
# | **300** | `Multiple Choices`               | The request has more than one possible response. The user or browser should choose one (e.g., multiple video formats). Rarely used.                                       |
# | **301** | `Moved Permanently`              | The requested resource has been moved to a new URL permanently. All future requests should use the new URL. Common in SEO and URL restructuring.                          |
# | **302** | `Found` (or `Moved Temporarily`) | Temporarily redirects the client to a different URL. The original URL should still be used for future requests. Used often in login or form redirection.                  |
# | **303** | `See Other`                      | Redirects the client to a different URL, usually after a POST request (e.g., form submission), and tells it to use GET at the new location. Prevents re-submitting forms. |
# | **304** | `Not Modified`                   | The resource hasn't changed since the last request. The client can use the cached version. Saves bandwidth.                                                               |
# | **305** | `Use Proxy`                      | Deprecated. Meant to instruct the client to use a proxy to access the resource. Not used for security reasons.                                                            |
# | **306** | `Reserved`                       | No longer used. It was used in early versions of HTTP but is now reserved for future use.                                                                                 |
# | **307** | `Temporary Redirect`             | Similar to 302, but **guarantees** the same method (e.g., POST stays POST). Safer for preserving request type when redirecting.                                           |


# ===========================================================================================================================================================================================================================

# ERRORS
# ===============

# Errors are raised when something goes wrong or unexpected 
# Unauthorized Access, Missing Pages, Invalid Request, Overload Backend Server, Internal Hardware/Software failure
# Flask uses abort() -func to stop the request processing and return an HTTP error status

# abort(status_code)

# | Code    | Meaning                                     |
# | ------- | ------------------------------------------- |
# | **400** | Bad Request – Invalid data in request       |
# | **401** | Unauthorized – User must log in             |
# | **403** | Forbidden – User doesn’t have permission    |
# | **404** | Not Found – Route or resource doesn’t exist |
# | **406** | Not Acceptable – Data format not supported  |
# | **415** | Unsupported Media Type                      |
# | **429** | Too Many Requests – Rate-limiting           |

# Blocking Usernames that Start with a Number

from flask import Flask, render_template, request, url_for, abort, redirect

app = Flask(__name__)

# @app.route('/user/<username>')
# def index(username):
#     if username[0].isdigit():
#         abort(400) # 400 Bad Request: Invalid username
#     return f"<h2> Good Morning, {username}</h2>"
    
# if __name__ == '__main__':
#     app.run(debug=True)


# Login System (Role-based Access)
# Admin - Guest - Staff

@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':     
        username = request.form.get('username')
        role = request.form.get('role')
        allowed_roles = ['admin', 'guest', 'staff']
        
        if username is None or username[0].isdigit():
            return abort(400) # Bad Request
        elif role.lower() == 'guest':
            return redirect(url_for('guest_login', username=username))
        elif role.lower() == 'staff':
            return redirect(url_for('staff_login', username=username))
        elif role.lower() not in allowed_roles:
            return abort(403) # Forbidden Request
        else:
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))                                             
    return render_template('index.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return f"<h2> Welcome Admin, You are in Admin dashboard! </h2>"

@app.route('/guest/welcome/<username>')
def guest_login(username):
    return f"<h2> Welcome {username}, You are logged in as Guest"

@app.route('/staff/tools/<username>')
def staff_login(username):
    return f"<h2> Welcome {username}, You are logged in as Staff!"

if __name__ == '__main__':
    app.run(debug=True)
    
# Change Port in Flask Application
# ===================================================
# a port which the data enters through or leaves the computer , helps to manage running multiple services on the same machine
#     Your machine (localhost) can run a Flask app on port 5000
#     And a database on port 3306
#     And maybe a different app on port 8000
# Each service listens on its own port.

# | Concept       | Explanation                                                  |
# | ------------- | ------------------------------------------------------------ |
# | **Port**      | A virtual "door" used by apps to listen for incoming traffic |
# | **Default**   | Flask uses `5000` by default                                 |
# | **Change It** | Use `app.run(port=your_port_number)`                         |
# | **Why**       | Avoid conflicts, run multiple apps, or meet system configs   |

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World, from Port: 8080'

if __name__ == '__main__':
    app.run(debug=True, port=8080)
    
# Changing the IP address in a Flask application using the "host" parameter
    app.run(host='192.168.0.105')
    
# Run the Flask app with a custom IP and port:
#     flask run --host=192.168.0.105 --port=5000

