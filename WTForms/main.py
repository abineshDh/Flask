from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
# from email import email_validator

app = Flask(__name__)

Bootstrap(app)

app.secret_key = 'mysecretkey'

class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()]) 
    # Email(granular_message=True)
    message = StringField(label='Message')
    submit = SubmitField(label='Log In')
    
@app.route('/', methods=['GET', 'POST'])
def home():
    cform = ContactForm()
    if cform.validate_on_submit():
        print(
            f"Name: {cform.name.data}, Email: {cform.email.data}, Message: {cform.message.data}"
        )
    return render_template('contact.html', form=cform)

if __name__ == '__main__':
    app.run(debug=True, port=5000)