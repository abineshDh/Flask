# TEMPLATE INHERITANCE
# ========================

# Flask. It allows us to define a common structure for web pages, such as headers, footers, and navigation bars, in a base template. This prevents redundant code and makes managing multiple pages easier.Flask. It allows us to define a common structure for web pages, such as headers, footers, and navigation bars, in a base template. This prevents redundant code and makes managing multiple pages easier.
    # Code Reusability: Write common HTML structure once and reuse it across multiple pages.
    # Better Maintainability: Updating the base template updates all inherited templates automatically.
    # Separation of Concerns: Keeps the structure and content of web pages separate for better organization.
    # Scalability: Easily add new pages without duplicating code.
    
# from flask import Flask, url_for, request, render_template

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
    
# | Concept                     | Meaning                                                                    |
# | --------------------------- | -------------------------------------------------------------------------- |
# | `{% block content %}`       | A **named section** of the base template that child templates can override |
# | `{% endblock %}`            | Marks the end of that block                                                |
# | `{% extends 'base.html' %}` | Tells Flask that the file inherits from `base.html`                        |
# | Used for                    | Reusing common layout while customizing parts of it                        |

    # When you visit different routes (/, /about, /contact), Flask dynamically renders the appropriate template.
    # The common structure from base.html is reused.
    # The {% block content %} placeholder is replaced with each page’s specific content.
    # This ensures a consistent layout across multiple pages.
    
# FLASH MESSAGES
# ===================

# Flash messages in Flask are used to provide feedback to the user—like success, warning, or error messages—usually 
# after form submissions or user actions like login, logout, etc

# {% with messages = get_flashed_messages() %}
#   {% if messages %}
#     {% for message in messages %}
#       <p>{{ message }}</p>
#     {% endfor %}
#   {% endif %}
# {% endwith %}

# <!-- Display flash messages -->
# {% with messages = get_flashed_messages(with_categories=true) %}
#   {% if messages %}
#     {% for category, message in messages %}
#       <p class="{{ category }}">{{ message }}</p>
#     {% endfor %}
#   {% endif %}
# {% endwith %}

# Login with Flash message

from flask import Flask, request, redirect, render_template, flash, url_for

app = Flask(__name__)

app.secret_key = 'my_secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('username') != 'admin' or request.form.get('password') != 'admin':
            flash('Invalid username or Password!', 'error')
            return redirect(url_for('home'))
        else:
            flash('Login Successful!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)




    
