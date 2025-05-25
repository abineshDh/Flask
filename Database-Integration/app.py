from flask import Flask, redirect, url_for, flash, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'A9Ix7g9MZIDx2uJwDSa6fFCYSX5pUmwx'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"{self.username}, {self.email}, {self.password}"

'''Add Users'''
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        add_user = User(username=username, email=email, password=password)
        db.session.add(add_user)
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)

'''Delete Users'''
@app.route('/<int:id>')
def delete(id): 
    delete_user = User.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)