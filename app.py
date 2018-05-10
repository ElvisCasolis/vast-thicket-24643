from flask import Flask, request, jsonify
#from models import db
from flask_sqlalchemy import SQLAlchemy
#from geoalchemy import *
from flask_marshmallow import Marshmallow
import psycopg2
from postgis.psycopg import register
import json
import os
from psycopg2.extras import json, Json

app = Flask(__name__)
DATABASE_URL = os.environ['DATABASE_URL']


user= 'tjbguzmfqysfmi'
pw= 'ec212d7962872b24c2ea09897186c914ae20e35c7d0f7c90e61eaecac7a41fb1'
db= 'dft06nn603npvn'
host= 'ec2-54-243-137-182.compute-1.amazonaws.com'
port= '5432'


DB_URL = 'postgres://{user}:{pw}@{url}/{db}'.format(user=user,pw=pw,url=host,db=db)


app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # silence the deprecation warning

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route("/")
def main():
    return 'Hello World !'




class restaurants(db.Model):

    __tablename__ = 'restaurants'
    id = db.Column(db.Text, primary_key=True)
    rating = db.Column(db.Integer)
    name = db.Column(db.Text)
    site = db.Column(db.Text)
    email = db.Column(db.Text)
    phone = db.Column(db.Text)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __init__(self, id, rating,name,site,email,phone,street,city,state,lat,lng):
        self.id = id
        self.rating = rating
        self.name = name
        self.site = site
        self.email = email
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.lat = lat
        self.lng = lng



class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'rating','name','site','email','phone','street','city','state','lat','lng')


user_schema = UserSchema()
users_schema = UserSchema(many=True)



# endpoint to create new user
@app.route("/restaurants", methods=["POST"])
def add_restaurante():
    id = request.json['id']
    rating = request.json['rating']
    name = request.json['name']
    site = request.json['site']
    email = request.json['email']
    phone = request.json['phone']
    street = request.json['street']
    city = request.json['city']
    state = request.json['state']
    lat = request.json['lat']
    lng = request.json['lng']

    
    new_restaurante = restaurants(id,rating,name,site,email,phone,street,city,state,lat,lng)

    db.session.add(new_restaurante)
    db.session.commit()

    return jsonify(str(new_restaurante))



# endpoint to show all users
@app.route("/restaurants", methods=["GET"])
def get_restaurantes():
    all_restaurantes = restaurants.query.all()
    result = users_schema.dump(all_restaurantes)
    return jsonify(result.data)


# endpoint to get user detail by id
@app.route("/restaurants/<id>", methods=["GET"])
def restaurante_detail(id):
    restaurante = restaurants.query.get(id)
    return user_schema.jsonify(restaurante)


# endpoint to update user
@app.route("/restaurants/<id>", methods=["PUT"])
def restaurante_update(id):
    restaurante = restaurants.query.get(id)
    rating = request.json['rating']
    name = request.json['name']
    site = request.json['site']
    email = request.json['email']
    phone = request.json['phone']
    street = request.json['street']
    city = request.json['city']
    state = request.json['state']
    lat = request.json['lat']
    lng = request.json['lng']

    restaurante.rating = rating
    restaurante.name = name
    restaurante.site = site
    restaurante.email = email
    restaurante.phone = phone
    restaurante.street = street
    restaurante.city = city
    restaurante.state = state
    restaurante.lat = lat
    restaurante.lng = lng


    db.session.commit()
    return user_schema.jsonify(restaurante)


# endpoint to delete user
@app.route("/restaurants/<id>", methods=["DELETE"])
def restaurante_delete(id):
    restaurante = restaurants.query.get(id)
    db.session.delete(restaurante)
    db.session.commit()

    return user_schema.jsonify(restaurante)


# endpoint to get statistics
@app.route("/restaurants/statistics")
def statistics():

    class DecimalEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, Decimal):
                    return float(obj)
                return json.JSONEncoder.default(self, obj)


	
	lat1 = request.args['lat']
	lng1 = request.args['lng']
	rad1= request.args['rad']
	#conn_string = "host={h} dbname={db} user={us} password={ps}".format(h=host,db=db,us=user,ps=pw)
	conn = psycopg2.connect(DB_URL)
	conn.set_isolation_level('ISOLATION_LEVEL_AUTOCOMMIT')
	cursor = self.conn.cursor()
	register(conn)

	query="""SELECT COUNT(*) as Count_Inside_Of_Circle, AVG(rating) as Rating_Average,stddev_pop(rating) as Standard_Deviation  from restaurants as A where ST_Point_Inside_Circle(a.geom,{lg},{lt},{rd});""".format(lt=lat1,lg=lng1,rd=rad1)
	cursor.execute(query)
	columns=[column[0] for column in cursor.description]

    obj=Decimal(jsonify(results[0]))
    def dumps(obj):
            return json.dumps(obj, cls=DecimalEncoder)

	


    results=[]
	for row in cursor.fetchall():
		results.append(dict(zip(columns,row)))


	return obj


if __name__ == '__main__':
    app.run()