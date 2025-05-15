from flask import Flask, url_for, redirect, request, render_template

app = Flask(__name__)


# FLASK RENDERING TEMPLATE
# ============================

# homepage
@app.route('/')
def home(name='Abinesh'):
    return f"<h2> Welcome to Flask Application, {name} </h2>"

# dynamic variable passing in html template
@app.route('/user/<username>')
def user(username):
    # pass the variables in the function and mention the variables in the redirect function as the arguments
    # use {{...}} in the html template to access the variables 
    return render_template('base.html', username=username)

# control flow, 
@app.route('/status/<role>')
def status(role):
    return render_template('base.html', role=role)

# for loop using list 
@app.route('/hobbies')
def hobbies():
    hobbies = ['coding', 'gaming', 'webseries', 'movies', 'sketching', 'driving', 'Swimming']
    # pass hobbies_list as argument to the html template to render 
    return render_template('base.html', hobbies=hobbies)

@app.route('/details')
def user_profile():
    details = {
        'name' : 'Abinesh',
        'age'  : 24,
        'job'  : 'python developer'
    }
    return render_template('base.html', details=details) # function() = variables{}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
# Note:
# Not every route passes all variables (username, role, hobbies, details)
# Wrapping each section with {% if variable %} ensures Jinja2 only tries to access the variable if it exists — avoiding UndefinedError.
# Template assumes all variables always exist	|Use {% if variable %} to guard each block
# Crashes on missing variable (e.g., details)	|Prevented by conditional blocks


    