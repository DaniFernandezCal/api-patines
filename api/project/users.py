import pika
import json
import requests

from flask import Flask, request, jsonify, Blueprint
from bson.json_util import dumps
from flask_bcrypt import Bcrypt
from mongo_utils import users, patines, slots
from api import flask_bcrypt
import config

users_api = Blueprint('users', __name__)

class User():
    name = ""
    password = ""
    
    def __init__(self, name, password):
        self.name = name
        self.password = password

def send_message(msg):
    
    credentials = pika.PlainCredentials(config.rabbit_user, config.rabbit_pass)
    parameters = pika.ConnectionParameters('rabbitmq', 5672, "/", credentials)
    connection = pika.BlockingConnection(parameters)
    
    # connection = (pika.BlockingConnection(
    #               pika.ConnectionParameters(host='rabbitmq')))
    channel = connection.channel()

    channel.queue_declare(queue="alquiler", durable=True)

    message = msg
    channel.basic_publish(exchange='',
                          routing_key="alquiler",
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=2))
    print(" [x] Sent message to rent patin: %r" % message)
    connection.close()


@users_api.route("/api/users/add", methods=['POST'])
def add_user():
    # Endpoint para crear usuario
    name = request.json['name']
    password = request.json['password']
    password = flask_bcrypt.generate_password_hash(password)
    user = User(name, password)
    user_exist = users.find_one({
		'name': user.name
	})
    if user_exist == None:
        users.insert_one({
			'name': user.name,
			'password': user.password
		})
        return jsonify({
			'ok': True,
			'message': 'User created successfully'
		}), 200
    else:
        return jsonify({
		    'ok': False,
		    'message': 'User already exist'
	}), 409

@users_api.route("/api/users/coger_patin", methods=['POST'])
def coger_patin():
    # Endpoint para coger patin
    name = request.headers.get('name')
    password = request.headers.get('password')
    validation = validate_user(name, password)
    if validation:
        slot_ocupado = slots.find_one({
			'_id': request.json['slot']
		})
        if slot_ocupado == None:
            return jsonify({
				'ok': False,
				'message': 'The slot specified doesnt exist'
			}), 404
        else:
            if slot_ocupado['patin'] == 0:
                return jsonify({
				    'ok': False,
				    'message': 'The slot specified doesnt have a patin'
			    }), 400
            else:
                data = {
					"user": name,
					"slot": request.json["slot"],
					"patin": slot_ocupado["patin"]
				}
                msg_to_send = json.dumps(data)
                send_message(msg_to_send)
                return jsonify({
	         	    'ok': True
		        }), 200
    else:
        return jsonify({
			'ok': False,
			'message': 'Invalid username or password'
		}), 401


@users_api.route("/api/users/login",methods=['POST'])
def login():
    name = request.json['name']
    password = request.json['password']
    user_correcto = validate_user(name, password)
    if user_correcto:
        return jsonify({
	        'ok': True
        }), 200
    else:
        return jsonify({
	        'ok': False,
			'message': 'Invalid username or password'
        }), 401


def validate_user(name, password):
    user = users.find_one({
		'name': name
	})
    if user != None:
        if flask_bcrypt.check_password_hash(user['password'], password):
            return True
        else:
            return False
    else:
        return False