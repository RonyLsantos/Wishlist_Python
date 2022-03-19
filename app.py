import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import random

# Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Wish Class/Model
class Wish(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=True)
	description = db.Column(db.String(200))
	link = db.Column(db.String(200))
	picturebase64 = db.Column(db.String(2000))

	def __init__(self, title, description, link, picturebase64):
		self.title = title
		self.description = description
		self.link = link
		self.picturebase64 = picturebase64

# Wish Schema
class WishSchema(ma.Schema):
	class Meta:
		fields = ('id', 'title', 'description', 'link', 'picturebase64')

# Init schema
wish_schema = WishSchema()
wishes_schema = WishSchema(many=True)

# Create 
@app.route('/wish', methods=['POST'])
def add_wish():
	title = request.json['title']
	description = request.json['description']
	link = request.json['link']
	picturebase64 = request.json['picturebase64']

	new_wish = Wish(title, description, link, picturebase64)

	db.session.add(new_wish)
	db.session.commit()

	return wish_schema.jsonify(new_wish)

# Get Wishes
@app.route('/allwishes', methods=['GET'])
def get_wishes():
	all_wishes = Wish.query.all()
	result = wishes_schema.dump(all_wishes)
	return jsonify(result)

# Get Single Wish
@app.route('/wish/<id>', methods=['GET'])
def get_wish_by_id(id):
	wish = Wish.query.get(id)
	return wish_schema.jsonify(wish)

# Get a random Wish
@app.route('/randomwish', methods=['GET'])
def get_random_wish():

	possibleids = Wish.query.with_entities(Wish.id).all()
	id = random.choice(possibleids)
	wish = Wish.query.get(id)
	return wish_schema.jsonify(wish)

# Update a wish
@app.route('/updatewish/<id>', methods=['PUT'])
def update_wish(id):
	wish = Wish.query.get(id)
	title = request.json['title']
	description = request.json['description']
	link = request.json['link']
	picturebase64 = request.json['picturebase64']	

	wish.title = title
	wish.description = description
	wish.link = link
	wish.picturebase64 = picturebase64

	db.session.commit()

	return wish_schema.jsonify(wish)

# Delete Wish
@app.route('/deletewish/<id>', methods=['DELETE'])
def delete_wish(id):
	wish = Wish.query.get(id)
	db.session.delete(wish)
	db.session.commit()

	return wish_schema.jsonify(wish)


# Run Server
if __name__ == '__main__':
  app.run(debug=True)