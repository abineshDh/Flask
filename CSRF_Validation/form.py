# CSRF PROTECTION
# =====================

# CSRF (Cross-Site Request Forgery) is a web security vulnerability that allows an attacker to trick a user into performing unintended actions on a 
# web app where they are authenticated (like changing passwords, sending money, etc.).

# using Flask-WTF, which provides automatic CSRF protection for forms. 

from flask import Flask, flash, redirect, url_for, render_template, request
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

# require csrf protection
app.secret_key = 'mysecretkey'

# enable csrf protection
CSRF = CSRFProtect(app)

# create FlaskForm to manage csrf
class  NameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
@app.route('/', methods=['GET', 'POST'])
def index():
    # instantiating NameForm class
    form = NameForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            flash(f'Hello {name} from Protected Form!', 'success')
        else:
            flash('CSRF Token Missing or Invalid', 'danger')
    return render_template('form.html', form=form)

@app.route('/form', methods=['POST'])
def unprotected_form():
    name = request.form.get('Name', '').strip()
    if not name:
        return f"<h2> [ERROR] Name is Required! </h2>", 400
    return f'Hello from {name} Un-Protected Form!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)