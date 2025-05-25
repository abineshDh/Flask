from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = '8weq787f384c4343cc43yc943rc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the db
db = SQLAlchemy(app)

# create destination model for row
class Destination(db.Model):
    # create attributes for columns
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False) 
    # convert db model into dict for changing into json
    def to_dict(self):
        return {
            'id' : self.id,
            'destination' : self.destination,
            'country' : self.country,
            'rating' : self.rating
        }
    
# --- ROUTES ---
# GET - Receives Data from Server
# index route
# www.rest_api/
@app.route('/')
def index():
    return jsonify(
        {'status' : 200,
         'message' : 'Travel Destination API'}
    ) 
    
# destination route
# www.rest_api/destinations
@app.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

# unique destination route by id
# www.rest_api/destinations/1
@app.route('/destinations/<int:destination_id>', methods=['GET'])
def get_specific_destination(destination_id): 
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({'error' : 'Destination not found'}), 404
    
# POST - Sends the data to the server
@app.route('/destinations', methods=['POST'])
def add_destination():
    data = request.get_json() # used to read the json data in py. dict to access values
    new_destination = Destination(destination=data['destination'], 
                                  country=data['country'],
                                  rating=data['rating'])
    # insert the new record object into the database model
    db.session.add(new_destination)
    db.session.commit()
    return jsonify(new_destination.to_dict()), 201    

# PUT - Update the data in server
@app.route('/destinations/<int:destination_id>', methods=['PUT'])
def update_destination(destination_id):
    data = request.get_json()
    destination = Destination.query.get(destination_id) 
    if destination:
        destination.destination = data.get('destination', destination.destination)
        destination.country = data.get('country', destination.country)
        destination.rating = data.get('rating', destination.rating)
        db.session.commit()
        return jsonify(destination.to_dict())
    else:
        return jsonify({'error' : 'Destination not found'}), 404
    
# DELETE - Delete a data in the server
@app.route('/destinations/<int:destination_id>', methods=['DELETE'])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({'message' : 'destination has been deleted'})
    else:
        return jsonify({'error' : 'destination not found'}), 404
    
if __name__ == '__main__':
    # create database
    with app.app_context():
        db.create_all()    
    app.run(debug=True)